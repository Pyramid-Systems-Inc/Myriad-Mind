import requests
import time

LIFECYCLE_MANAGER_URL = "http://lifecycle_manager:5005/create_agent"
AGENT_REGISTRY_URL = "http://agent_registry_service:5006"

def discover_agent_endpoint(concept: str, intent: str) -> str | None:
    """Calls the Agent Registry Service to discover an agent's endpoint."""
    try:
        payload = {"concept": concept, "intent": intent}
        response = requests.post(f"{AGENT_REGISTRY_URL}/discover", json=payload, timeout=5)
        if response.status_code == 200:
            return response.json().get("endpoint")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error discovering agent for ({concept}, {intent}): {e}")
        return None

def register_new_agent(agent_data: dict) -> bool:
    """Calls the Agent Registry Service to register a newly created agent."""
    try:
        payload = {
            "agent_name": agent_data["agent_name"],
            "concept": agent_data["concept_name"],
            "intent_map": agent_data["intent_map"],
            "endpoint": agent_data["endpoint"]
        }
        response = requests.post(f"{AGENT_REGISTRY_URL}/register", json=payload, timeout=5)
        response.raise_for_status()
        return response.status_code == 201
    except requests.exceptions.RequestException as e:
        print(f"Error registering new agent '{agent_data.get('agent_name')}': {e}")
        return False

def trigger_neurogenesis(concept: str) -> bool:
    """Calls the Lifecycle Manager and then registers the new agent."""
    print(f"Triggering neurogenesis for concept: '{concept}'...")
    try:
        # For now, we default to creating a FactBase agent.
        # Future versions could infer the required agent_type.
        payload = {"concept_name": concept, "agent_type": "FactBase"}
        response = requests.post(LIFECYCLE_MANAGER_URL, json=payload, timeout=45)
        response.raise_for_status()
        new_agent_data = response.json()

        if new_agent_data.get("status") == "success":
            print(f"Neurogenesis successful. New agent '{new_agent_data['agent_name']}' created.")
            new_agent_data['concept_name'] = concept
            if register_new_agent(new_agent_data):
                print(f"Agent '{new_agent_data['agent_name']}' registered successfully.")
                time.sleep(3)
                return True
            else:
                print(f"Agent '{new_agent_data['agent_name']}' created but failed to register.")
                return False
        else:
            print(f"Error from Lifecycle Manager: {new_agent_data.get('message')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Failed to trigger neurogenesis: {e}")
        return False

def send_task_to_agent(task: dict) -> dict | None:
    """Sends a single task to the appropriate agent."""
    concept, intent = task['concept'], task['intent']
    agent_url = discover_agent_endpoint(concept, intent)

    if not agent_url:
        print(f"No agent found for concept '{concept}' and intent '{intent}'.")
        if trigger_neurogenesis(concept):
            agent_url = discover_agent_endpoint(concept, intent)
        else:
            return {"task_id": task["task_id"], "status": "error", "error_message": "Agent not found and neurogenesis failed."}

    if agent_url:
        payload = {"task_id": task["task_id"], "intent": intent, "concept": concept, "args": task.get("args", {})}
        print(f"Dispatching Agent Job to {agent_url}: {payload}")
        try:
            response = requests.post(agent_url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"task_id": task["task_id"], "status": "error", "error_message": str(e)}
    else:
        return {"task_id": task["task_id"], "status": "error", "error_message": f"Agent for '{concept}' created, but intent '{intent}' not supported."}

def process_tasks(tasks: list) -> dict:
    """Processes a list of tasks by sending them to agents and collecting results."""
    # This bootstrap registration is temporary. In a mature system, agents would self-register.
    initial_agents = [
        {"agent_name": "Lightbulb_Definition_AI", "concept_name": "lightbulb", "endpoint": "http://lightbulb_definition_ai:5001", "intent_map": {"define": "/query", "explain_impact": "/query", "analyze_historical_context": "/query"}},
        {"agent_name": "Lightbulb_Function_AI", "concept_name": "lightbulb", "endpoint": "http://lightbulb_function_ai:5002", "intent_map": {"explain_limitation": "/query", "compare": "/query", "synthesize_response": "/query"}},
        {"agent_name": "Lightbulb_Function_AI", "concept_name": "factories", "endpoint": "http://lightbulb_function_ai:5002", "intent_map": {"explain_impact": "/query"}}
    ]
    for agent in initial_agents:
        register_new_agent(agent)
    
    all_results = {}
    for task in tasks:
        result = send_task_to_agent(task)
        all_results[str(task["task_id"])] = result or {"task_id": task["task_id"], "status": "error", "error_message": "Failed to process task."}
    return all_results