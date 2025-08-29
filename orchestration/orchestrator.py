import requests
import time

# The Orchestrator now communicates with the GraphDB Manager, not the old registry.
GRAPHDB_MANAGER_URL = "http://graphdb_manager_ai:5008"
LIFECYCLE_MANAGER_URL = "http://lifecycle_manager:5005/create_agent"

def populate_initial_graph():
    """
    Populates the graph database with the initial, known agents.
    This replaces the old bootstrap registration process.
    """
    print("🧠 Populating initial knowledge graph...")
    
    initial_nodes = [
        {"label": "Concept", "properties": {"name": "lightbulb"}},
        {"label": "Concept", "properties": {"name": "factories"}},
        {"label": "Agent", "properties": {"name": "Lightbulb_Definition_AI", "endpoint": "http://lightbulb_definition_ai:5001/query"}},
        {"label": "Agent", "properties": {"name": "Lightbulb_Function_AI", "endpoint": "http://lightbulb_function_ai:5002/query"}}
    ]
    
    for node in initial_nodes:
        try:
            requests.post(f"{GRAPHDB_MANAGER_URL}/create_node", json=node, timeout=5)
        except requests.exceptions.RequestException:
            # It might already exist from a previous run, which is fine.
            pass
            
    initial_relationships = [
        {"source_label": "Agent", "source_properties": {"name": "Lightbulb_Definition_AI"}, "target_label": "Concept", "target_properties": {"name": "lightbulb"}, "type": "HANDLES_CONCEPT"},
        {"source_label": "Agent", "source_properties": {"name": "Lightbulb_Function_AI"}, "target_label": "Concept", "target_properties": {"name": "lightbulb"}, "type": "HANDLES_CONCEPT"},
        {"source_label": "Agent", "source_properties": {"name": "Lightbulb_Function_AI"}, "target_label": "Concept", "target_properties": {"name": "factories"}, "type": "HANDLES_CONCEPT"}
    ]
    
    for rel in initial_relationships:
        try:
            requests.post(f"{GRAPHDB_MANAGER_URL}/create_relationship", json=rel, timeout=5)
        except requests.exceptions.RequestException:
            pass
    
    print("✅ Initial knowledge graph populated.")


def discover_agent_via_graph(concept: str, intent: str) -> str | None:
    """Discovers an agent by querying the knowledge graph."""
    try:
        # For now, we assume the intent maps to a generic 'HANDLES_CONCEPT' relationship.
        # This will become more sophisticated later.
        payload = {
            "start_node_label": "Concept",
            "start_node_properties": {"name": concept.lower()},
            "relationship_type": "HANDLES_CONCEPT",
            "relationship_direction": "in",
            "target_node_label": "Agent"
        }
        response = requests.post(f"{GRAPHDB_MANAGER_URL}/find_connected_nodes", json=payload, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("nodes"):
                # Just return the first agent found for now.
                # Future logic could select the best agent based on properties.
                agent_node = data["nodes"][0]
                return agent_node.get("endpoint")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error discovering agent for '{concept}' via graph: {e}")
        return None

def send_task_to_agent(task: dict) -> dict | None:
    """Sends a single task to the appropriate agent discovered via the graph."""
    concept, intent = task['concept'], task['intent']
    agent_url = discover_agent_via_graph(concept, intent)
    
    # Neurogenesis logic is removed for now, as it needs to be re-architected
    # to create graph nodes instead of calling the old lifecycle manager.

    if agent_url:
        payload = {"task_id": task["task_id"], "intent": intent, "concept": concept, "args": task.get("args", {})}
        print(f"Dispatching Agent Job to {agent_url} (discovered via graph): {payload}")
        try:
            response = requests.post(agent_url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"task_id": task["task_id"], "status": "error", "error_message": str(e)}
    else:
        return {"task_id": task["task_id"], "status": "error", "error_message": f"No agent found in graph for concept '{concept}'"}

def process_tasks(tasks: list) -> dict:
    """Processes a list of tasks by sending them to agents and collecting results."""
    all_results = {}
    for task in tasks:
        result = send_task_to_agent(task)
        all_results[str(task["task_id"])] = result or {"task_id": task["task_id"], "status": "error", "error_message": "Failed to process task."}
    return all_results

# A one-time setup function to populate the graph when the module is first imported.
populate_initial_graph()