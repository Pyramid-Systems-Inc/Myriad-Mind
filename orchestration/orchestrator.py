import requests
import time
from orchestration.agent_registry import get_agent_url, register_agent

LIFECYCLE_MANAGER_URL = "http://lifecycle_manager:5005/create_agent"

def trigger_neurogenesis(concept: str) -> str | None:
    """
    Calls the Lifecycle Manager to create a new agent for an unknown concept.
    """
    print(f"Triggering neurogenesis for concept: '{concept}'...")
    try:
        # For now, we default to creating a FactBase agent.
        # Future versions could infer the required agent_type.
        payload = {"concept_name": concept, "agent_type": "FactBase"}
        response = requests.post(LIFECYCLE_MANAGER_URL, json=payload, timeout=30) # Increased timeout for build
        
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "success":
            agent_name = data["agent_name"]
            new_endpoint = data["endpoint"]
            port = data["port"]
            
            # The new agent's endpoint inside the docker network is via its name
            network_endpoint = f"http://{agent_name.lower()}:{port}/query"

            print(f"Neurogenesis successful. New agent '{agent_name}' created.")
            
            # Dynamically register the new agent's capabilities.
            # The template supports 'define' and 'get_facts'.
            register_agent(concept, 'define', network_endpoint)
            register_agent(concept, 'get_facts', network_endpoint)
            print(f"Agent '{agent_name}' registered for intents: define, get_facts")

            # Wait a moment for the new container to be fully responsive
            time.sleep(3)
            
            return network_endpoint
        else:
            print(f"Error from Lifecycle Manager: {data.get('message')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Failed to trigger neurogenesis: {e}")
        return None

def send_task_to_agent(task: dict) -> dict | None:
    """
    Sends a single task to the appropriate agent.
    If the agent doesn't exist, it triggers neurogenesis to create it.
    """
    agent_url = get_agent_url(task['concept'], task['intent'])

    if not agent_url:
        print(f"No agent found for concept '{task['concept']}' and intent '{task['intent']}'.")
        # Attempt to create a new agent for the concept
        new_agent_url = trigger_neurogenesis(task['concept'])
        
        if new_agent_url:
            # Retry getting the URL for the specific intent
            agent_url = get_agent_url(task['concept'], task['intent'])
        else:
            return {"task_id": task["task_id"], "status": "error", "error_message": "Agent not found and neurogenesis failed."}

    if agent_url:
        agent_job_payload = {
            "task_id": task["task_id"],
            "intent": task["intent"],
            "concept": task["concept"],
            "args": task.get("args", {})
        }
        print(f"Dispatching Agent Job to {agent_url}: {agent_job_payload}")
        try:
            response = requests.post(agent_url, json=agent_job_payload, timeout=10)
            response.raise_for_status()
            agent_result = response.json()
            print(f"Received Agent Result: {agent_result}")
            return agent_result
        except requests.exceptions.RequestException as e:
            print(f"Error sending task {task['task_id']} to agent: {e}")
            return {"task_id": task["task_id"], "status": "error", "error_message": str(e)}
    else:
        print(f"Error: Agent for '{task['concept']}' created, but intent '{task['intent']}' not supported.")
        return {"task_id": task["task_id"], "status": "error", "error_message": f"Agent for '{task['concept']}' does not support intent '{task['intent']}'"}

def process_tasks(tasks: list) -> dict:
    """
    Processes a list of tasks by sending them to agents and collecting results.
    """
    all_results = {}
    for task in tasks:
        result = send_task_to_agent(task)
        if result:
            all_results[str(task["task_id"])] = result
        else:
            all_results[str(task["task_id"])] = {"task_id": task["task_id"], "status": "error", "error_message": "Failed to process task, no result from agent."}
    return all_results

if __name__ == '__main__':
    # Example usage for direct testing, now including neurogenesis
    sample_tasks_for_orchestrator_test = [
        {"task_id": 101, "intent": "define", "concept": "lightbulb", "args": {}},
        {"task_id": 102, "intent": "define", "concept": "philosophy", "args": {}}, # This should trigger neurogenesis
        {"task_id": 103, "intent": "get_facts", "concept": "philosophy", "args": {}} # This should use the new agent
    ]
    print("--- Testing orchestrator.py directly with neurogenesis ---")
    results = process_tasks(sample_tasks_for_orchestrator_test)
    print("\n--- Orchestrator Test Results ---")
    for task_id, result in results.items():
        print(f"Task {task_id}: {result}")
    print("--- End of orchestrator.py direct test ---")