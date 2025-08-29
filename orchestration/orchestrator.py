import requests
from typing import Optional

# The Orchestrator now communicates with the GraphDB Manager, not the old registry.
GRAPHDB_MANAGER_URL = "http://graphdb_manager_ai:5008"

def discover_agent_via_graph(concept: str, intent: str) -> Optional[str]:
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

def send_task_to_agent(task: dict) -> Optional[dict]:
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