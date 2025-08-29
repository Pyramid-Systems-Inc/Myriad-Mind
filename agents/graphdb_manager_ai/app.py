import os
from flask import Flask, request, jsonify
from neo4j import GraphDatabase, exceptions

app = Flask(__name__)

# --- Neo4j Connection ---
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")

try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    driver.verify_connectivity()
    print("✅ Successfully connected to Neo4j database.")
except exceptions.AuthError as e:
    print(f"❌ Neo4j Authentication Error: {e}. Check NEO4J_USER and NEO4J_PASSWORD.")
    driver = None
except exceptions.ServiceUnavailable as e:
    print(f"❌ Neo4j Connection Error: {e}. Is the database running and accessible at {NEO4J_URI}?")
    driver = None
except Exception as e:
    print(f"❌ An unexpected error occurred when connecting to Neo4j: {e}")
    driver = None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the GraphDB Manager."""
    if not driver:
        return jsonify({"status": "unhealthy", "reason": "Neo4j driver not initialized"}), 503
    try:
        driver.verify_connectivity()
        return jsonify({
            "status": "healthy",
            "service": "GraphDB Manager AI",
            "version": "1.0.0",
            "neo4j_connection": "connected"
        })
    except Exception as e:
        return jsonify({"status": "unhealthy", "reason": str(e)}), 503

@app.route('/create_node', methods=['POST'])
def create_node():
    """Creates a new node in the graph."""
    if not driver:
        return jsonify({"status": "error", "message": "Database not connected"}), 503
    
    data = request.get_json()
    if not data or 'label' not in data or 'properties' not in data:
        return jsonify({"status": "error", "message": "Request must include 'label' and 'properties'"}), 400
    
    label = data['label']
    properties = data['properties']
    
    # Basic validation to prevent Cypher injection issues
    if not label.isalnum():
        return jsonify({"status": "error", "message": "Label must be alphanumeric"}), 400

    try:
        with driver.session() as session:
            # Using parameters to prevent Cypher injection
            query = f"CREATE (n:{label} $props) RETURN elementId(n) AS id"
            result = session.run(query, props=properties)
            node_id = result.single()['id']
            return jsonify({"status": "success", "node_id": node_id, "label": label, "properties": properties}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/create_relationship', methods=['POST'])
def create_relationship():
    """Creates a relationship between two existing nodes."""
    if not driver:
        return jsonify({"status": "error", "message": "Database not connected"}), 503
        
    data = request.get_json()
    required_fields = ['source_label', 'source_properties', 'target_label', 'target_properties', 'type']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": f"Request must include {required_fields}"}), 400

    rel_type = data['type']
    rel_props = data.get('properties', {})
    
    # Fix: Corrected validation to allow underscores
    if not rel_type.isupper() or not rel_type.replace('_', '').isalpha():
         return jsonify({"status": "error", "message": "Relationship type must be uppercase and contain only letters and underscores."}), 400

    try:
        with driver.session() as session:
            # Fix: Dynamically build WHERE clauses for robust property matching.
            # This is the correct and safe way to match nodes by a subset of properties.
            source_where_clause = " AND ".join([f"a.{key} = $source_props.{key}" for key in data['source_properties']])
            target_where_clause = " AND ".join([f"b.{key} = $target_props.{key}" for key in data['target_properties']])

            query = (
                f"MATCH (a:{data['source_label']}) WHERE {source_where_clause} "
                f"MATCH (b:{data['target_label']}) WHERE {target_where_clause} "
                f"CREATE (a)-[r:{rel_type} $rel_props]->(b) "
                "RETURN elementId(r) AS id"
            )
            
            # Combine all parameters into a single dictionary for the driver
            params = {
                "source_props": data['source_properties'],
                "target_props": data['target_properties'],
                "rel_props": rel_props
            }

            result = session.run(query, params)
            rel_id = result.single()
            
            if rel_id:
                return jsonify({"status": "success", "relationship_id": rel_id['id']}), 201
            else:
                return jsonify({"status": "error", "message": "One or both nodes not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/find_connected_nodes', methods=['POST'])
def find_connected_nodes():
    """Finds nodes connected to a start node by a specific relationship."""
    if not driver:
        return jsonify({"status": "error", "message": "Database not connected"}), 503
        
    data = request.get_json()
    required_fields = ['start_node_label', 'start_node_properties', 'relationship_type']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": f"Request must include {required_fields}"}), 400
    
    start_label = data['start_node_label']
    start_props = data['start_node_properties']
    rel_type = data['relationship_type']
    target_label = data.get('target_node_label', '') # Optional: filter by target label
    direction = data.get('relationship_direction', 'out') # 'out' or 'in'

    # Build the relationship pattern based on direction
    if direction == 'in':
        rel_pattern = f"<-[r:{rel_type}]-"
    else:
        rel_pattern = f"-[r:{rel_type}]->"

    try:
        with driver.session() as session:
            start_where_clause = " AND ".join([f"a.{key} = $start_props.{key}" for key in start_props])
            
            query = (
                f"MATCH (a:{start_label}) WHERE {start_where_clause} "
                f"MATCH (a){rel_pattern}(b:{target_label}) "
                "RETURN b"
            )

            result = session.run(query, start_props=start_props)
            nodes = [record["b"]._properties for record in result]
            
            return jsonify({"status": "success", "nodes": nodes})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def close_driver():
    if driver:
        driver.close()

if __name__ == '__main__':
    import atexit
    atexit.register(close_driver)
    app.run(host='0.0.0.0', port=5008, debug=True)