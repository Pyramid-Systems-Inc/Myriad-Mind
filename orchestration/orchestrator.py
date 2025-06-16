import requests
from orchestration.agent_registry import get_agent_url

def send_task_to_agent(task: dict) -> dict | None:
    """
    Sends a single task to the appropriate agent.
    """
    agent_url = get_agent_url(task['concept'], task['intent'])

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
            response.raise_for_status()  # Raise an exception for HTTP errors
            agent_result = response.json()
            print(f"Received Agent Result: {agent_result}")
            return agent_result
        except requests.exceptions.RequestException as e:
            print(f"Error sending task {task['task_id']} to agent: {e}")
            return {"task_id": task["task_id"], "status": "error", "error_message": str(e)}
        except Exception as e:
            print(f"An unexpected error occurred for task {task['task_id']}: {e}")
            return {"task_id": task["task_id"], "status": "unexpected_error", "error_message": str(e)}
    else:
        print(f"Error: No agent URL found for concept '{task['concept']}' and intent '{task['intent']}'")
        return {"task_id": task["task_id"], "status": "error", "error_message": "Agent URL not found"}

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
            # Ensure a result is always recorded, even if send_task_to_agent returned None (though it shouldn't with current logic)
            all_results[str(task["task_id"])] = {"task_id": task["task_id"], "status": "error", "error_message": "Failed to process task, no result from agent."}
    return all_results

if __name__ == '__main__':
    # Example usage (for direct testing of this module, not part of the main flow)
    sample_tasks_for_orchestrator_test = [
        {"task_id": 101, "intent": "define", "concept": "lightbulb", "args": {}},
        {"task_id": 102, "intent": "explain_limitation", "concept": "lightbulb", "args": {}},
        {"task_id": 103, "intent": "non_existent_intent", "concept": "lightbulb", "args": {}} # Test missing agent
    ]
    print("--- Testing orchestrator.py directly ---")
    results = process_tasks(sample_tasks_for_orchestrator_test)
    print("\n--- Orchestrator Test Results ---")
    for task_id, result in results.items():
        print(f"Task {task_id}: {result}")
    print("--- End of orchestrator.py direct test ---")