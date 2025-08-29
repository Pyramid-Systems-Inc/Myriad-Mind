import requests
import json

# Configuration for all known agents in the system
AGENT_CONFIG = {
    "agents": [
        {
            "name": "Lightbulb_Definition_AI",
            "endpoint": "http://lightbulb_definition_ai:5001/query",
            "type": "FactBase",
            "handled_concepts": ["lightbulb"]
        },
        {
            "name": "Lightbulb_Function_AI",
            "endpoint": "http://lightbulb_function_ai:5002/query",
            "type": "FunctionExecutor",
            "handled_concepts": ["lightbulb", "factories"]
        }
    ]
}

GRAPHDB_MANAGER_URL = "http://localhost:5008"

def clear_graph():
    """Clears the entire graph to ensure a clean slate."""
    print("🔥 Clearing all existing nodes and relationships from the graph...")
    try:
        with requests.post(f"{GRAPHDB_MANAGER_URL}/_internal/clear", timeout=10) as response:
            response.raise_for_status()
            print("✅ Graph cleared successfully.")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not clear graph. It might be empty already. Error: {e}")


def migrate_agents_to_graph():
    """
    Reads the AGENT_CONFIG and populates the Neo4j database.
    This script is the definitive way to register agents in the new architecture.
    """
    print("🚀 Starting migration of agents to the knowledge graph...")

    all_concepts = set()
    for agent in AGENT_CONFIG["agents"]:
        for concept in agent["handled_concepts"]:
            all_concepts.add(concept)

    # 1. Create all Concept nodes
    print("\n--- Step 1: Creating Concept Nodes ---")
    for concept_name in all_concepts:
        node_payload = {
            "label": "Concept",
            "properties": {"name": concept_name}
        }
        try:
            print(f"Creating Concept node: '{concept_name}'")
            response = requests.post(f"{GRAPHDB_MANAGER_URL}/create_node", json=node_payload, timeout=5)
            response.raise_for_status()
            print(f"  -> Success (ID: {response.json().get('node_id')})")
        except requests.exceptions.RequestException as e:
            print(f"  -> Error creating concept node '{concept_name}': {e}")

    # 2. Create all Agent nodes
    print("\n--- Step 2: Creating Agent Nodes ---")
    for agent in AGENT_CONFIG["agents"]:
        node_payload = {
            "label": "Agent",
            "properties": {
                "name": agent["name"],
                "endpoint": agent["endpoint"],
                "type": agent["type"]
            }
        }
        try:
            print(f"Creating Agent node: '{agent['name']}'")
            response = requests.post(f"{GRAPHDB_MANAGER_URL}/create_node", json=node_payload, timeout=5)
            response.raise_for_status()
            print(f"  -> Success (ID: {response.json().get('node_id')})")
        except requests.exceptions.RequestException as e:
            print(f"  -> Error creating agent node '{agent['name']}': {e}")

    # 3. Create all relationships
    print("\n--- Step 3: Creating Relationships ---")
    for agent in AGENT_CONFIG["agents"]:
        for concept_name in agent["handled_concepts"]:
            rel_payload = {
                "source_label": "Agent",
                "source_properties": {"name": agent["name"]},
                "target_label": "Concept",
                "target_properties": {"name": concept_name},
                "type": "HANDLES_CONCEPT",
                "properties": {"weight": 1.0} # Default weight
            }
            try:
                print(f"Linking '{agent['name']}' --[HANDLES_CONCEPT]--> '{concept_name}'")
                response = requests.post(f"{GRAPHDB_MANAGER_URL}/create_relationship", json=rel_payload, timeout=5)
                response.raise_for_status()
                print(f"  -> Success (ID: {response.json().get('relationship_id')})")
            except requests.exceptions.RequestException as e:
                print(f"  -> Error creating relationship for '{agent['name']}': {e}")

    print("\n🎉 Migration complete! The knowledge graph is populated.")

if __name__ == "__main__":
    # Optional: Add a small utility to the graph manager to clear the DB for clean migrations
    # For now, we assume a fresh start or manual clearing.
    migrate_agents_to_graph()