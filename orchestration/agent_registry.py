from typing import Dict, Tuple, Optional

# Agent Registry: Maps (concept, intent) to agent URL
AGENT_REGISTRY: Dict[Tuple[str, str], str] = {
    # Lightbulb Definition AI - handles definitions and basic facts
    ('lightbulb', 'define'): 'http://localhost:5001/query',
    ('lightbulb', 'explain_impact'): 'http://localhost:5001/query',
    ('lightbulb', 'analyze_historical_context'): 'http://localhost:5001/query',

    # Lightbulb Function AI - handles applications and impact
    ('lightbulb', 'explain_limitation'): 'http://localhost:5002/query',
    ('factories', 'explain_impact'): 'http://localhost:5002/query',
    ('factory', 'explain_impact'): 'http://localhost:5002/query',
    ('industrial', 'explain_impact'): 'http://localhost:5002/query',

    # Complex queries - route to Function AI for impact analysis
    ('why was the lightbulb important for factories', 'explain_impact'): 'http://localhost:5002/query',
    ('compare the impact of lightbulbs versus candles in factory settings', 'compare'): 'http://localhost:5002/query',
    ('compare the impact of lightbulbs versus candles in factory settings_factory_relationship', 'compare'): 'http://localhost:5002/query',

    # Synthesis tasks - route to Function AI as it handles complex reasoning
    ('multi_concept_synthesis', 'synthesize_response'): 'http://localhost:5002/query'
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