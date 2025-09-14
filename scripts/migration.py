import requests
import json
import os

GRAPHDB_MANAGER_URL = os.environ.get("GRAPHDB_MANAGER_URL", "http://localhost:5008")
KNOWLEDGE_BASE_FILE = os.path.join(os.path.dirname(__file__), 'knowledge_base.json')

def clear_graph():
    """Clears the entire graph to ensure a clean slate."""
    # This is a destructive operation and should be used with caution.
    # The graphdb_manager does not expose this by default; it would need to be added for a migration script.
    # For now, we assume the user can manually clear the DB if needed.
    print("SKIPPING: Graph clearing. Please manually clear Neo4j if a fresh start is needed.")
    pass

def migrate_knowledge_to_graph():
    """
    Reads the knowledge_base.json file and populates the Neo4j database
    in a two-pass process: nodes first, then relationships.
    """
    print("🚀 Starting migration of knowledge base to the graph...")

    try:
        with open(KNOWLEDGE_BASE_FILE, 'r') as f:
            knowledge_base = json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: Knowledge base file not found at '{KNOWLEDGE_BASE_FILE}'")
        return
    except json.JSONDecodeError:
        print(f"❌ ERROR: Could not parse '{KNOWLEDGE_BASE_FILE}'. Please check for valid JSON.")
        return

    # 1. Create all Nodes
    print("\n--- Step 1: Creating All Nodes ---")
    nodes = knowledge_base.get("nodes", [])
    if not nodes:
        print("⚠️ No nodes found in knowledge base file.")
    else:
        for node_payload in nodes:
            try:
                label = node_payload.get('label')
                props = node_payload.get('properties', {})
                name = props.get('name', '[Unnamed]')
                print(f"Creating {label} node: '{name}'")
                response = requests.post(f"{GRAPHDB_MANAGER_URL}/create_node", json=node_payload, timeout=5)
                response.raise_for_status()
                print(f"  -> Success (ID: {response.json().get('node_id')})")
            except requests.exceptions.RequestException as e:
                print(f"  -> ❌ Error creating node '{name}': {e}")
                print(f"     Response: {e.response.text if e.response else 'No response'}")

    # 2. Create all Relationships
    print("\n--- Step 2: Creating All Relationships ---")
    relationships = knowledge_base.get("relationships", [])
    if not relationships:
        print("⚠️ No relationships found in knowledge base file.")
    else:
        for rel_payload in relationships:
            try:
                start_label = rel_payload.get('start_node_label')
                start_props = rel_payload.get('start_node_properties', {})
                end_label = rel_payload.get('end_node_label')
                end_props = rel_payload.get('end_node_properties', {})
                rel_type = rel_payload.get('type')
                
                # The create_relationship endpoint expects different key names
                api_payload = {
                    "start_node_label": start_label,
                    "start_node_properties": start_props,
                    "end_node_label": end_label,
                    "end_node_properties": end_props,
                    "relationship_type": rel_type,
                    "relationship_properties": rel_payload.get("properties", {})
                }
                
                start_name = start_props.get('name', '[Unnamed]')
                end_name = end_props.get('name', '[Unnamed]')
                
                print(f"Linking '{start_name}' --[{rel_type}]--> '{end_name}'")
                response = requests.post(f"{GRAPHDB_MANAGER_URL}/create_relationship", json=api_payload, timeout=5)
                response.raise_for_status()
                print(f"  -> Success (ID: {response.json().get('relationship_id')})")
            except requests.exceptions.RequestException as e:
                print(f"  -> ❌ Error creating relationship: {e}")
                print(f"     Response: {e.response.text if e.response else 'No response'}")

    print("\n🎉 Migration complete! The knowledge graph is populated.")

if __name__ == "__main__":
    # In a real scenario, you might want to add argument parsing
    # to, for example, clear the graph before migrating.
    # clear_graph() 
    migrate_knowledge_to_graph()