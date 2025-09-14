import os
import time
import threading
from datetime import datetime
from flask import Flask, request, jsonify
from neo4j import GraphDatabase, exceptions

app = Flask(__name__)

# --- Neo4j Connection ---
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")

# Hebbian learning configuration
HEBBIAN_REL_TYPE = os.environ.get("HEBBIAN_REL_TYPE", "HANDLES_CONCEPT")
HEBBIAN_DELTA_SUCCESS = float(os.environ.get("HEBBIAN_DELTA_SUCCESS", "0.05"))
HEBBIAN_DELTA_FAILURE = float(os.environ.get("HEBBIAN_DELTA_FAILURE", "0.02"))
HEBBIAN_DECAY_RATE = float(os.environ.get("HEBBIAN_DECAY_RATE", "0.01"))  # per-interval multiplicative decay
HEBBIAN_DECAY_INTERVAL_SEC = int(os.environ.get("HEBBIAN_DECAY_INTERVAL_SEC", "900"))  # 15 minutes
ENABLE_HEBBIAN_DECAY = os.environ.get("ENABLE_HEBBIAN_DECAY", "true").lower() == "true"

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
            "version": "1.1.0",
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
    # Allow creation via ID for one node, and properties for the other.
    # This is more efficient after creating a node and getting its ID back.
    by_id = 'start_node_id' in data or 'end_node_id' in data
    
    if by_id:
        # At least one of the nodes must be specified by ID
        if 'start_node_id' not in data and 'end_node_id' not in data:
            return jsonify({"status": "error", "message": "If creating by ID, 'start_node_id' or 'end_node_id' must be provided."}), 400
    else:
        # Legacy support: if not using IDs, all property fields are required
        required_fields = ['start_node_label', 'start_node_properties', 'end_node_label', 'end_node_properties', 'relationship_type']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"status": "error", "message": f"Request must include {required_fields} or specify nodes by ID"}), 400

    rel_type = data['relationship_type']
    rel_props = data.get('relationship_properties', {})

    # Basic validation
    if not rel_type.isupper() or not rel_type.replace('_', '').isalpha():
        return jsonify({"status": "error", "message": "Relationship type must be uppercase and contain only letters and underscores."}), 400

    try:
        with driver.session() as session:
            params = {"rel_props": rel_props}

            # Build MATCH clause for the start node
            if 'start_node_id' in data:
                match_a = "MATCH (a) WHERE elementId(a) = $start_node_id"
                params['start_node_id'] = data['start_node_id']
            else:
                start_where = " AND ".join([f"a.{k} = $start_props.{k}" for k in data['start_node_properties']])
                match_a = f"MATCH (a:{data['start_node_label']}) WHERE {start_where}"
                params['start_props'] = data['start_node_properties']

            # Build MATCH clause for the end node
            if 'end_node_id' in data:
                match_b = "MATCH (b) WHERE elementId(b) = $end_node_id"
                params['end_node_id'] = data['end_node_id']
            else:
                end_where = " AND ".join([f"b.{k} = $end_props.{k}" for k in data['end_node_properties']])
                match_b = f"MATCH (b:{data['end_node_label']}) WHERE {end_where}"
                params['end_props'] = data['end_node_properties']

            query = (
                f"{match_a} "
                f"{match_b} "
                f"CREATE (a)-[r:{rel_type} $rel_props]->(b) "
                "RETURN elementId(r) AS id"
            )

            result = session.run(query, **params)
            rel_id = result.single()

            if rel_id:
                return jsonify({"status": "success", "relationship_id": rel_id['id']}), 201
            else:
                return jsonify({"status": "error", "message": "One or both nodes not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/query_nodes', methods=['POST'])
def query_nodes():
    """Query nodes by label/type with optional property filters."""
    if not driver:
        return jsonify({"status": "error", "message": "Database not connected"}), 503

    data = request.get_json() or {}
    node_type = data.get('node_type') or data.get('label')
    props = data.get('properties', {})

    if not node_type:
        return jsonify({"status": "error", "message": "Request must include 'node_type' (or 'label')"}), 400

    if not str(node_type).replace('_', '').isalnum():
        return jsonify({"status": "error", "message": "Node label must be alphanumeric/underscore"}), 400

    try:
        with driver.session() as session:
            where_clause = " AND ".join([f"n.{k} = $props.{k}" for k in props]) or "true"
            query = (
                f"MATCH (n:{node_type}) WHERE {where_clause} RETURN n"
            )
            result = session.run(query, props=props)
            nodes = [record["n"]._properties for record in result]
            return jsonify({"status": "success", "nodes": nodes})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/find_connected_nodes', methods=['POST'])
def find_connected_nodes():
    """Find connected nodes. Supports two input formats for compatibility."""
    if not driver:
        return jsonify({"status": "error", "message": "Database not connected"}), 503

    data = request.get_json() or {}

    # Compatibility format used by EnhancedGraphIntelligence
    if 'node_name' in data and 'relationship_types' in data:
        try:
            node_name = data['node_name']
            rel_types = data.get('relationship_types', [HEBBIAN_REL_TYPE])
            direction = data.get('direction', 'incoming')  # incoming means (Agent)-[r]->(Concept)
            with driver.session() as session:
                if direction == 'incoming':
                    # Agents connected to this concept
                    query = (
                        "MATCH (a:Agent)-[r:%s]->(c:Concept {name: $name}) "
                        "RETURN a as agent, r as rel" % ("|".join(rel_types))
                    )
                else:
                    query = (
                        "MATCH (c:Concept {name: $name})-[r:%s]->(b) "
                        "RETURN b as agent, r as rel" % ("|".join(rel_types))
                    )
                result = session.run(query, name=node_name.lower())
                agents = []
                for record in result:
                    node_props = record["agent"]._properties
                    rel_props = dict(record["rel"])
                    node_props = dict(node_props)
                    node_props["relationship_properties"] = rel_props
                    agents.append(node_props)
                return jsonify({"status": "success", "connected_agents": agents})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # Original format
    required_fields = ['start_node_label', 'start_node_properties', 'relationship_type']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": f"Request must include {required_fields}"}), 400

    start_label = data['start_node_label']
    start_props = data['start_node_properties']
    rel_type = data['relationship_type']
    target_label = data.get('target_node_label', '')
    direction = data.get('relationship_direction', 'out')

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

@app.route('/get_agents_for_concept', methods=['POST'])
def get_agents_for_concept():
    """Return agents connected to a concept with relationship properties (Hebbian)."""
    if not driver:
        return jsonify({"status": "error", "message": "Database not connected"}), 503

    data = request.get_json() or {}
    concept = (data.get('concept') or '').strip().lower()
    if not concept:
        return jsonify({"status": "error", "message": "Request must include 'concept'"}), 400

    rel_type = data.get('relationship_type', HEBBIAN_REL_TYPE)
    try:
        with driver.session() as session:
            query = (
                f"MATCH (a:Agent)-[r:{rel_type}]->(c:Concept {{name: $name}}) "
                "RETURN a as agent, r as rel"
            )
            result = session.run(query, name=concept)
            agents = []
            for record in result:
                node_props = record["agent"]._properties
                rel_props = dict(record["rel"])
                agents.append({
                    "agent": node_props,
                    "relationship": rel_props
                })
            return jsonify({"status": "success", "concept": concept, "agents": agents})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/hebbian/strengthen', methods=['POST'])
def hebbian_strengthen():
    """Strengthen or weaken the relationship weight between Agent and Concept based on outcome."""
    if not driver:
        return jsonify({"status": "error", "message": "Database not connected"}), 503

    data = request.get_json() or {}
    agent_id = (data.get('agent_id') or '').strip()
    concept = (data.get('concept') or '').strip().lower()
    success = bool(data.get('success', True))
    rel_type = data.get('relationship_type', HEBBIAN_REL_TYPE)
    delta_success = float(data.get('delta_success', HEBBIAN_DELTA_SUCCESS))
    delta_failure = float(data.get('delta_failure', HEBBIAN_DELTA_FAILURE))

    if not agent_id or not concept:
        return jsonify({"status": "error", "message": "Request must include 'agent_id' and 'concept'"}), 400

    try:
        with driver.session() as session:
            query = (
                f"MERGE (a:Agent {{name: $agent_id}}) "
                f"MERGE (c:Concept {{name: $concept}}) "
                f"MERGE (a)-[r:{rel_type}]->(c) "
                "ON CREATE SET r.weight = 0.5, r.usage_count = 0, r.success_count = 0, r.failure_count = 0, "
                "r.success_rate = 0.5, r.decay_rate = $decay_rate, r.last_updated = timestamp() "
                "WITH r, (CASE $success WHEN true THEN $delta_success ELSE -$delta_failure END) AS delta "
                "SET r.usage_count = r.usage_count + 1, "
                "r.success_count = r.success_count + (CASE $success WHEN true THEN 1 ELSE 0 END), "
                "r.failure_count = r.failure_count + (CASE $success WHEN true THEN 0 ELSE 1 END), "
                "r.success_rate = toFloat(r.success_count) / toFloat(r.usage_count), "
                "r.weight = CASE WHEN r.weight + delta > 1.0 THEN 1.0 WHEN r.weight + delta < 0.0 THEN 0.0 ELSE r.weight + delta END, "
                "r.last_updated = timestamp() "
                "RETURN r as rel"
            )
            params = {
                'agent_id': agent_id,
                'concept': concept,
                'success': success,
                'delta_success': delta_success,
                'delta_failure': delta_failure,
                'decay_rate': HEBBIAN_DECAY_RATE
            }
            result = session.run(query, **params)
            rel = result.single()
            rel_props = dict(rel["rel"]) if rel else {}
            return jsonify({"status": "success", "relationship": rel_props})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/hebbian/decay', methods=['POST'])
def hebbian_decay():
    """Apply decay to HANDLES_CONCEPT relationship weights, optionally filtered by concept/agent."""
    if not driver:
        return jsonify({"status": "error", "message": "Database not connected"}), 503

    data = request.get_json() or {}
    rel_type = data.get('relationship_type', HEBBIAN_REL_TYPE)
    agent_id = data.get('agent_id')
    concept = (data.get('concept') or '').strip().lower() if data.get('concept') else None
    decay_rate = float(data.get('decay_rate', HEBBIAN_DECAY_RATE))

    try:
        with driver.session() as session:
            if agent_id and concept:
                query = (
                    f"MATCH (a:Agent {{name: $agent_id}})-[r:{rel_type}]->(c:Concept {{name: $concept}}) "
                    "SET r.weight = CASE WHEN r.weight * (1.0 - $decay_rate) < 0.0 THEN 0.0 ELSE r.weight * (1.0 - $decay_rate) END, r.last_updated = timestamp() "
                    "RETURN r as rel"
                )
                params = {'agent_id': agent_id, 'concept': concept, 'decay_rate': decay_rate}
                result = session.run(query, **params)
                rel = result.single()
                rel_props = dict(rel["rel"]) if rel else {}
                return jsonify({"status": "success", "decayed": 1 if rel else 0, "relationship": rel_props})
            elif concept:
                query = (
                    f"MATCH (:Concept {{name: $concept}})<-[r:{rel_type}]-(:Agent) "
                    "SET r.weight = CASE WHEN r.weight * (1.0 - $decay_rate) < 0.0 THEN 0.0 ELSE r.weight * (1.0 - $decay_rate) END, r.last_updated = timestamp() "
                    "RETURN count(r) as cnt"
                )
                result = session.run(query, concept=concept, decay_rate=decay_rate)
                cnt = result.single()["cnt"]
                return jsonify({"status": "success", "decayed": cnt})
            elif agent_id:
                query = (
                    f"MATCH (:Agent {{name: $agent_id}})-[r:{rel_type}]->(:Concept) "
                    "SET r.weight = CASE WHEN r.weight * (1.0 - $decay_rate) < 0.0 THEN 0.0 ELSE r.weight * (1.0 - $decay_rate) END, r.last_updated = timestamp() "
                    "RETURN count(r) as cnt"
                )
                result = session.run(query, agent_id=agent_id, decay_rate=decay_rate)
                cnt = result.single()["cnt"]
                return jsonify({"status": "success", "decayed": cnt})
            else:
                query = (
                    f"MATCH ()-[r:{rel_type}]->() "
                    "SET r.weight = CASE WHEN r.weight * (1.0 - $decay_rate) < 0.0 THEN 0.0 ELSE r.weight * (1.0 - $decay_rate) END, r.last_updated = timestamp() "
                    "RETURN count(r) as cnt"
                )
                result = session.run(query, decay_rate=decay_rate)
                cnt = result.single()["cnt"]
                return jsonify({"status": "success", "decayed": cnt})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def _hebbian_decay_background_loop():
    """Background loop applying periodic Hebbian decay to relationships."""
    while True:
        try:
            if driver and ENABLE_HEBBIAN_DECAY:
                with driver.session() as session:
                    query = (
                        f"MATCH ()-[r:{HEBBIAN_REL_TYPE}]->() "
                        "SET r.weight = CASE WHEN r.weight * (1.0 - $decay_rate) < 0.0 THEN 0.0 ELSE r.weight * (1.0 - $decay_rate) END, r.last_updated = timestamp() "
                        "RETURN count(r) as cnt"
                    )
                    session.run(query, decay_rate=HEBBIAN_DECAY_RATE)
            time.sleep(HEBBIAN_DECAY_INTERVAL_SEC)
        except Exception:
            # Avoid killing thread on errors
            time.sleep(HEBBIAN_DECAY_INTERVAL_SEC)


def close_driver():
    if driver:
        driver.close()

if __name__ == '__main__':
    import atexit
    atexit.register(close_driver)
    # Start background decay thread if enabled
    try:
        if ENABLE_HEBBIAN_DECAY:
            threading.Thread(target=_hebbian_decay_background_loop, daemon=True).start()
    except Exception:
        pass
    app.run(host='0.0.0.0', port=5008, debug=True)