from typing import Dict, Tuple, Optional

# Agent Registry: Maps (concept, intent) to agent URL
AGENT_REGISTRY: Dict[Tuple[str, str], str] = {
    ('lightbulb', 'define'): 'http://lightbulb_definition_ai:5001/query',
    ('lightbulb', 'explain_limitation'): 'http://lightbulb_function_ai:5002/query'
}

def register_agent(concept: str, intent: str, url: str) -> None:
    """
    Registers or updates an agent in the AGENT_REGISTRY.

    Args:
        concept: The concept the agent handles.
        intent: The intent related to the concept.
        url: The URL endpoint of the agent.
    """
    AGENT_REGISTRY[(concept.lower(), intent.lower())] = url

def get_agent_url(concept: str, intent: str) -> Optional[str]:
    """
    Retrieves an agent's URL from the AGENT_REGISTRY.

    Args:
        concept: The concept the agent handles.
        intent: The intent related to the concept.

    Returns:
        The agent's URL if found, otherwise None.
    """
    return AGENT_REGISTRY.get((concept.lower(), intent.lower()))

if __name__ == '__main__':
    # Example Usage (optional, for testing)
    print(f"Initial Registry: {AGENT_REGISTRY}")

    register_agent('weather', 'get_forecast', 'http://weather_agent:5003/query')
    print(f"Registry after adding weather agent: {AGENT_REGISTRY}")

    print(f"URL for ('lightbulb', 'define'): {get_agent_url('lightbulb', 'define')}")
    print(f"URL for ('weather', 'get_forecast'): {get_agent_url('weather', 'get_forecast')}")
    print(f"URL for ('nonexistent', 'action'): {get_agent_url('nonexistent', 'action')}")