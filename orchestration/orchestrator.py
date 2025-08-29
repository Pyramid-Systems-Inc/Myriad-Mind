import requests
import json
import time
from typing import Optional, Dict, Any, List

# The Orchestrator now communicates with the GraphDB Manager, not the old registry.
GRAPHDB_MANAGER_URL = "http://graphdb_manager_ai:5008"

# Agent endpoints for concept research
LIGHTBULB_DEFINITION_AI_URL = "http://lightbulb_definition_ai:5001"
LIGHTBULB_FUNCTION_AI_URL = "http://lightbulb_function_ai:5002"

def check_concept_exists(concept: str) -> bool:
    """Check if a concept node already exists in the graph"""
    try:
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
            return len(data.get("nodes", [])) > 0
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking concept existence for '{concept}': {e}")
        return False

def research_unknown_concept(concept: str, intent: str) -> Dict[str, Any]:
    """Research an unknown concept using existing agents"""
    print(f"🧠 NEUROGENESIS: Researching unknown concept '{concept}' for intent '{intent}'")
    
    research_data = {
        "concept": concept,
        "intent": intent,
        "research_timestamp": time.time(),
        "research_sources": [],
        "knowledge_gathered": {},
        "related_concepts": [],
        "confidence_score": 0.0
    }
    
    # Use existing agents to research the concept through collaboration
    research_agents = [
        {"name": "Lightbulb_Definition_AI", "url": LIGHTBULB_DEFINITION_AI_URL, "expertise": "technical_definitions"},
        {"name": "Lightbulb_Function_AI", "url": LIGHTBULB_FUNCTION_AI_URL, "expertise": "functional_analysis"}
    ]
    
    for agent in research_agents:
        print(f"  📚 Requesting research assistance from {agent['name']}...")
        research_result = request_concept_research(agent, concept, intent)
        if research_result:
            research_data["knowledge_gathered"][agent['expertise']] = research_result
            research_data["research_sources"].append(agent["name"])
    
    # Synthesize research results
    synthesized_knowledge = synthesize_research_results(research_data)
    research_data.update(synthesized_knowledge)
    
    return research_data

def request_concept_research(agent: Dict[str, str], concept: str, intent: str) -> Optional[Dict[str, Any]]:
    """Request an agent to research an unknown concept"""
    collaboration_request = {
        "source_agent": {"name": "Orchestrator_Neurogenesis", "type": "ConceptResearcher"},
        "collaboration_type": "knowledge_request",
        "target_concept": concept,
        "specific_request": {
            "knowledge_type": "concept_research",
            "research_depth": "comprehensive",
            "focus_areas": [intent, "definition", "relationships", "applications"]
        },
        "context": {
            "neurogenesis_trigger": True,
            "unknown_concept": concept,
            "original_intent": intent,
            "research_purpose": "concept_expansion"
        }
    }
    
    try:
        response = requests.post(f"{agent['url']}/collaborate", json=collaboration_request, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                return result.get("data")
            elif result.get("status") == "no_expertise":
                print(f"    ℹ️  {agent['name']} has no expertise in '{concept}'")
                return None
        else:
            print(f"    ⚠️  Research request failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Research request error: {e}")
    
    return None

def synthesize_research_results(research_data: Dict[str, Any]) -> Dict[str, Any]:
    """Synthesize research results into a coherent concept understanding"""
    knowledge = research_data.get("knowledge_gathered", {})
    concept = research_data.get("concept", "unknown")
    
    synthesized = {
        "primary_definition": "",
        "key_attributes": [],
        "related_concepts": [],
        "applications": [],
        "confidence_score": 0.0
    }
    
    # Extract and combine knowledge from different sources
    definitions = []
    attributes = []
    applications = []
    confidence_scores = []
    
    for expertise, data in knowledge.items():
        if isinstance(data, dict):
            # Extract primary knowledge
            if "primary_knowledge" in data:
                definitions.append(data["primary_knowledge"])
            
            # Extract confidence scores
            if "confidence" in data:
                confidence_scores.append(data["confidence"])
            
            # Extract additional context if available
            if "additional_context" in data:
                context = data["additional_context"]
                if isinstance(context, dict):
                    for key, value in context.items():
                        if "application" in key.lower() or "impact" in key.lower():
                            applications.append(str(value))
    
    # Synthesize primary definition
    if definitions:
        synthesized["primary_definition"] = f"Based on research: {' | '.join(definitions[:2])}"
    else:
        synthesized["primary_definition"] = f"Unknown concept '{concept}' requires further research"
    
    # Calculate confidence
    if confidence_scores:
        synthesized["confidence_score"] = sum(confidence_scores) / len(confidence_scores)
    else:
        synthesized["confidence_score"] = 0.1  # Low confidence for unknown concepts
    
    # Extract related concepts and applications
    synthesized["applications"] = applications[:3]  # Top 3 applications
    synthesized["related_concepts"] = [concept.lower()]  # At minimum, relate to itself
    
    return synthesized

def create_concept_node(concept: str, research_data: Dict[str, Any]) -> bool:
    """Create a rich concept node in the graph with researched data"""
    print(f"🔬 Creating rich concept node for '{concept}'...")
    
    node_properties = {
        "name": concept.lower(),
        "display_name": concept,
        "type": "researched_concept",
        "creation_method": "neurogenesis_research",
        "creation_timestamp": research_data.get("research_timestamp", time.time()),
        "primary_definition": research_data.get("primary_definition", ""),
        "confidence_score": research_data.get("confidence_score", 0.0),
        "research_sources": json.dumps(research_data.get("research_sources", [])),
        "key_attributes": json.dumps(research_data.get("key_attributes", [])),
        "related_concepts": json.dumps(research_data.get("related_concepts", [])),
        "applications": json.dumps(research_data.get("applications", [])),
        "original_intent": research_data.get("intent", ""),
        "research_status": "active"
    }
    
    try:
        # Create the concept node
        create_payload = {
            "label": "Concept",
            "properties": node_properties
        }
        
        response = requests.post(f"{GRAPHDB_MANAGER_URL}/create_node", json=create_payload, timeout=10)
        
        if response.status_code == 201:
            result = response.json()
            node_id = result.get("node_id")
            print(f"  ✅ Created concept node '{concept}' (ID: {node_id})")
            return True
        else:
            print(f"  ❌ Failed to create concept node: {response.status_code}")
            print(f"     Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error creating concept node: {e}")
        return False

def expand_concept(concept: str, intent: str) -> Dict[str, Any]:
    """Complete concept expansion process: research + graph node creation"""
    print(f"🚀 CONCEPT EXPANSION: Starting expansion for '{concept}'")
    
    # Step 1: Research the concept
    research_data = research_unknown_concept(concept, intent)
    
    # Step 2: Create rich graph node
    success = create_concept_node(concept, research_data)
    
    # Step 3: Return expansion result
    expansion_result = {
        "concept": concept,
        "expansion_successful": success,
        "research_data": research_data,
        "expansion_method": "neurogenesis_phase1",
        "can_retry": True
    }
    
    if success:
        print(f"  🎉 Concept expansion completed successfully for '{concept}'!")
        expansion_result["message"] = f"Successfully expanded knowledge about '{concept}' through agent research and graph node creation."
    else:
        print(f"  ⚠️  Concept expansion partially completed for '{concept}' (research done, node creation failed)")
        expansion_result["message"] = f"Researched '{concept}' but failed to create graph node. Research data available."
    
    return expansion_result

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
    
    if agent_url:
        # Agent found - normal processing
        payload = {"task_id": task["task_id"], "intent": intent, "concept": concept, "args": task.get("args", {})}
        print(f"Dispatching Agent Job to {agent_url} (discovered via graph): {payload}")
        try:
            response = requests.post(agent_url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"task_id": task["task_id"], "status": "error", "error_message": str(e)}
    else:
        # 🧠 NEUROGENESIS TRIGGER: No agent found for concept
        print(f"🧠 NEUROGENESIS TRIGGERED: No agent found for concept '{concept}' with intent '{intent}'")
        
        # Check if this is a completely unknown concept
        concept_exists = check_concept_exists(concept)
        
        if not concept_exists:
            print(f"  🔍 Concept '{concept}' is completely unknown - triggering concept expansion!")
            
            # Trigger concept expansion (Phase 1: Concept Expansion)
            expansion_result = expand_concept(concept, intent)
            
            if expansion_result.get("expansion_successful"):
                # Concept expansion successful - return the researched knowledge
                return {
                    "task_id": task["task_id"],
                    "status": "neurogenesis_success",
                    "data": expansion_result["message"],
                    "neurogenesis_data": {
                        "concept": concept,
                        "expansion_method": "concept_research",
                        "research_summary": expansion_result["research_data"].get("primary_definition", ""),
                        "confidence": expansion_result["research_data"].get("confidence_score", 0.0),
                        "sources": expansion_result["research_data"].get("research_sources", [])
                    },
                    "agent_name": "Orchestrator_Neurogenesis"
                }
            else:
                # Concept expansion failed but we have research data
                research_data = expansion_result.get("research_data", {})
                if research_data.get("primary_definition"):
                    return {
                        "task_id": task["task_id"],
                        "status": "neurogenesis_partial",
                        "data": f"Researched '{concept}': {research_data.get('primary_definition', 'No definition found')}",
                        "neurogenesis_data": {
                            "concept": concept,
                            "expansion_method": "research_only",
                            "research_summary": research_data.get("primary_definition", ""),
                            "confidence": research_data.get("confidence_score", 0.0),
                            "sources": research_data.get("research_sources", [])
                        },
                        "agent_name": "Orchestrator_Neurogenesis"
                    }
                else:
                    return {
                        "task_id": task["task_id"],
                        "status": "neurogenesis_failed",
                        "data": f"Unable to research or expand knowledge about '{concept}'. This concept may require specialized agents or external knowledge sources.",
                        "error_message": f"Concept expansion failed for '{concept}'"
                    }
        else:
            # Concept exists but no agent handles it
            return {
                "task_id": task["task_id"],
                "status": "no_agent_available",
                "data": f"Concept '{concept}' exists in the knowledge graph but no agent is currently available to handle intent '{intent}'. This may require agent creation in future phases.",
                "error_message": f"No agent available for known concept '{concept}' with intent '{intent}'"
            }

def process_tasks(tasks: list) -> dict:
    """Processes a list of tasks by sending them to agents and collecting results."""
    all_results = {}
    for task in tasks:
        result = send_task_to_agent(task)
        all_results[str(task["task_id"])] = result or {"task_id": task["task_id"], "status": "error", "error_message": "Failed to process task."}
    return all_results