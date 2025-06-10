"""
Central Orchestrator for Myriad Cognitive Architecture
Manages agent registry and orchestrates queries to specialized agents.
"""

import logging
import requests
import json
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('orchestrator.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        """Initialize the Orchestrator with the AI Registry."""
        # AI_REGISTRY: Maps agent names to their network addresses
        self.AI_REGISTRY = {
            'Lightbulb_AI': 'http://localhost:5001',
            'Factory_AI': 'http://localhost:5002',
            # Future agents will be added here
        }
        logger.info("Orchestrator initialized with AI Registry")
        logger.info(f"Registered agents: {list(self.AI_REGISTRY.keys())}")
    
    def orchestrate_query(self, keywords: List[str]) -> Dict[str, Any]:
        """
        Core orchestration logic: takes keywords and queries appropriate agents.
        
        Args:
            keywords: List of keywords extracted from user query
            
        Returns:
            Dictionary containing responses from all queried agents
        """
        logger.info(f"Received keywords for orchestration: {keywords}")
        
        # Determine which agents to query based on keywords
        agents_to_query = self._determine_relevant_agents(keywords)
        logger.info(f"Determined relevant agents: {agents_to_query}")
        
        # Query each relevant agent
        agent_responses = {}
        for agent_name in agents_to_query:
            try:
                logger.info(f"Querying {agent_name}...")
                response = self._query_agent(agent_name, keywords)
                agent_responses[agent_name] = response
                logger.info(f"Received response from {agent_name}: {response}")
            except Exception as e:
                logger.error(f"Failed to query {agent_name}: {str(e)}")
                agent_responses[agent_name] = {"error": str(e)}
        
        logger.info(f"Orchestration complete. Total responses: {len(agent_responses)}")
        return agent_responses
    
    def _determine_relevant_agents(self, keywords: List[str]) -> List[str]:
        """
        Determine which agents are relevant for the given keywords.
        
        Args:
            keywords: List of keywords from the query
            
        Returns:
            List of agent names to query
        """
        relevant_agents = []
        
        # Simple keyword matching for Phase 1
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if 'lightbulb' in keyword_lower or 'light' in keyword_lower:
                if 'Lightbulb_AI' not in relevant_agents:
                    relevant_agents.append('Lightbulb_AI')
            
            if 'factory' in keyword_lower or 'factories' in keyword_lower or 'industrial' in keyword_lower:
                if 'Factory_AI' not in relevant_agents:
                    relevant_agents.append('Factory_AI')
        
        # If no specific matches, query all available agents (fallback)
        if not relevant_agents:
            relevant_agents = list(self.AI_REGISTRY.keys())
            logger.info("No specific agent matches found, querying all available agents")
        
        return relevant_agents
    
    def _query_agent(self, agent_name: str, keywords: List[str]) -> Dict[str, Any]:
        """
        Send a query to a specific agent.
        
        Args:
            agent_name: Name of the agent to query
            keywords: Keywords to send to the agent
            
        Returns:
            Response from the agent
            
        Raises:
            Exception: If agent query fails
        """
        if agent_name not in self.AI_REGISTRY:
            raise ValueError(f"Agent {agent_name} not found in registry")
        
        agent_url = self.AI_REGISTRY[agent_name]
        query_endpoint = f"{agent_url}/query"
        
        # Prepare the query payload
        payload = {
            "query": "core_info",
            "keywords": keywords
        }
        
        try:
            # Make the HTTP request to the agent
            response = requests.get(
                query_endpoint,
                params=payload,
                timeout=10  # 10 second timeout
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.ConnectionError:
            raise Exception(f"Could not connect to {agent_name} at {agent_url}")
        except requests.exceptions.Timeout:
            raise Exception(f"Timeout while querying {agent_name}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP error while querying {agent_name}: {str(e)}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response from {agent_name}")
    
    def get_registry_status(self) -> Dict[str, str]:
        """
        Get the current status of all agents in the registry.
        
        Returns:
            Dictionary mapping agent names to their status
        """
        logger.info("Checking registry status...")
        status = {}
        
        for agent_name, agent_url in self.AI_REGISTRY.items():
            try:
                response = requests.get(f"{agent_url}/health", timeout=5)
                if response.status_code == 200:
                    status[agent_name] = "online"
                else:
                    status[agent_name] = f"error (HTTP {response.status_code})"
            except Exception:
                status[agent_name] = "offline"
        
        logger.info(f"Registry status: {status}")
        return status

def main():
    """Main function for testing the orchestrator."""
    orchestrator = Orchestrator()
    
    # Test the orchestrator with sample keywords
    test_keywords = ["lightbulb", "factories"]
    logger.info(f"Testing orchestrator with keywords: {test_keywords}")
    
    try:
        responses = orchestrator.orchestrate_query(test_keywords)
        logger.info("Test orchestration completed successfully")
        print(f"Agent responses: {json.dumps(responses, indent=2)}")
    except Exception as e:
        logger.error(f"Test orchestration failed: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()