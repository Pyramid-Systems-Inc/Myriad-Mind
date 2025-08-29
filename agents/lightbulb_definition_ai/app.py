from flask import Flask, request, jsonify
import requests
import os
from typing import Optional, Dict, Any

app = Flask(__name__)

# Agent-to-Agent Communication Configuration
GRAPHDB_MANAGER_URL = os.environ.get("GRAPHDB_MANAGER_URL", "http://graphdb_manager_ai:5008")
AGENT_NAME = "Lightbulb_Definition_AI"
AGENT_TYPE = "FactBase"
PRIMARY_CONCEPTS = ["lightbulb"]

def handle_concept_research(concept: str, request_details: Dict[str, Any], context: Dict[str, Any]) -> str:
    """Handle concept research requests for unknown concepts (neurogenesis support)"""
    
    # Check if this concept might be related to our expertise
    concept_lower = concept.lower()
    related_terms = ["light", "bulb", "lamp", "illumination", "electric", "edison", "incandescent", "electricity"]
    
    is_related = any(term in concept_lower for term in related_terms)
    
    if is_related:
        # Provide research based on our knowledge domain
        if any(term in concept_lower for term in ["led", "fluorescent", "halogen"]):
            return f"Based on my lighting expertise: {concept} appears to be a type of lighting technology. Like traditional incandescent lightbulbs, it likely converts electrical energy into light, but may use different mechanisms for illumination. Modern lighting technologies often improve upon the basic incandescent principle of heating a filament to produce light."
        
        elif any(term in concept_lower for term in ["solar", "renewable", "green"]):
            return f"From a lighting perspective: {concept} may relate to sustainable lighting solutions. Traditional incandescent lightbulbs are inefficient, and {concept} might represent an improvement in energy efficiency or renewable energy integration for lighting systems."
            
        elif any(term in concept_lower for term in ["smart", "iot", "connected"]):
            return f"Based on lighting technology knowledge: {concept} likely represents an advancement beyond basic incandescent lightbulbs. Smart lighting typically adds connectivity, programmability, and energy efficiency to traditional lighting functions."
            
        else:
            return f"Drawing from lighting expertise: {concept} appears related to illumination technology. While I specialize in traditional incandescent lightbulbs, {concept} may represent a variation, improvement, or related application of electrical lighting principles."
    
    else:
        # Concept not obviously related to lighting - provide general research approach
        research_depth = request_details.get('research_depth', 'basic')
        
        if research_depth == 'comprehensive':
            return f"From a definitional research perspective: {concept} requires specialized knowledge outside my lighting expertise. However, I can suggest that like any technical concept, {concept} likely has: 1) A specific definition and purpose, 2) Key characteristics or properties, 3) Applications or use cases, 4) Historical development, and 5) Relationships to other concepts. Further research would require domain experts."
        else:
            return f"Research note: {concept} falls outside my specialized knowledge of lighting technology. This concept would benefit from investigation by domain experts or specialized agents with relevant expertise."

def discover_peer_agents(concept: str) -> list:
    """Discover other agents that handle a specific concept via graph traversal"""
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
            if data.get("nodes"):
                # Filter out self to avoid circular calls
                return [node for node in data["nodes"] 
                       if node.get("properties", {}).get("name") != AGENT_NAME]
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error discovering peer agents for '{concept}': {e}")
        return []

def request_peer_collaboration(peer_endpoint: str, collaboration_request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Send a collaboration request to a peer agent"""
    try:
        response = requests.post(f"{peer_endpoint}/collaborate", json=collaboration_request, timeout=8)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Peer collaboration failed with status {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error collaborating with peer at {peer_endpoint}: {e}")
        return None

@app.route('/query', methods=['POST'])
def query():
    """
    Endpoint that accepts POST requests for lightbulb definition queries.
    Implements the Agent-to-Orchestrator Protocol (The "Agent Result").
    """
    try:
        # Get the intent from the request
        data = request.get_json()
        if not data or 'intent' not in data:
            return jsonify({
                "agent_name": "Lightbulb_Definition_AI",
                "status": "error",
                "data": "Missing 'intent' in request"
            }), 400
        
        intent = data['intent']
        
        # Handle multiple intents - this is where the cognitive logic resides
        if intent == 'define':
            # Basic definition
            definition = "an electric device that produces light via an incandescent filament"
            return jsonify({
                "agent_name": "Lightbulb_Definition_AI",
                "status": "success",
                "data": definition
            })
        elif intent == 'explain_impact':
            # Impact explanation from definition perspective
            impact = "The lightbulb revolutionized illumination by providing reliable, controllable electric light that could extend working hours and improve safety in industrial settings."
            return jsonify({
                "agent_name": "Lightbulb_Definition_AI",
                "status": "success",
                "data": impact
            })
        elif intent == 'analyze_historical_context':
            # Historical context
            context = "The incandescent lightbulb was perfected by Thomas Edison in 1879, marking a pivotal moment in the transition from gas and candle lighting to electric illumination."
            return jsonify({
                "agent_name": "Lightbulb_Definition_AI",
                "status": "success",
                "data": context
            })
        else:
            return jsonify({
                "agent_name": "Lightbulb_Definition_AI",
                "status": "error",
                "data": f"Unknown intent: {intent}. Supported intents: define, explain_impact, analyze_historical_context"
            }), 400
            
    except Exception as e:
        return jsonify({
            "agent_name": "Lightbulb_Definition_AI",
            "status": "error",
            "data": str(e)
        }), 500

@app.route('/collaborate', methods=['POST'])
def collaborate():
    """
    Agent-to-Agent collaboration endpoint.
    Enables direct peer-to-peer communication without orchestrator mediation.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "agent_name": AGENT_NAME,
                "status": "error", 
                "data": "Missing collaboration request data"
            }), 400

        # Extract collaboration request details
        source_agent = data.get('source_agent', {})
        collaboration_type = data.get('collaboration_type', 'knowledge_request')
        target_concept = data.get('target_concept', '')
        specific_request = data.get('specific_request', {})
        context = data.get('context', {})

        print(f"🤝 Collaboration request from {source_agent.get('name', 'unknown')} for concept '{target_concept}'")

        # Handle different types of collaboration
        if collaboration_type == 'knowledge_request':
            return handle_knowledge_request(target_concept, specific_request, context, source_agent)
        elif collaboration_type == 'context_sharing':
            return handle_context_sharing(target_concept, specific_request, context, source_agent)
        else:
            return jsonify({
                "agent_name": AGENT_NAME,
                "status": "error",
                "data": f"Unknown collaboration type: {collaboration_type}"
            }), 400

    except Exception as e:
        return jsonify({
            "agent_name": AGENT_NAME,
            "status": "error",
            "data": f"Collaboration error: {str(e)}"
        }), 500

def handle_knowledge_request(concept: str, request_details: Dict[str, Any], context: Dict[str, Any], source_agent: Dict[str, Any]) -> tuple:
    """Handle knowledge requests from peer agents"""
    
    # Check if we can help with this concept
    if concept.lower() not in [c.lower() for c in PRIMARY_CONCEPTS]:
        return jsonify({
            "agent_name": AGENT_NAME,
            "status": "no_expertise",
            "data": f"I don't have expertise in '{concept}'. My expertise is in: {PRIMARY_CONCEPTS}"
        }), 200

    # Extract what kind of knowledge is requested
    knowledge_type = request_details.get('knowledge_type', 'definition')
    
    if knowledge_type == 'definition':
        knowledge = "an electric device that produces light via an incandescent filament"
    elif knowledge_type == 'historical_context':
        knowledge = "The incandescent lightbulb was perfected by Thomas Edison in 1879, marking a pivotal moment in the transition from gas and candle lighting to electric illumination."
    elif knowledge_type == 'properties':
        knowledge = "Key properties: electrical resistance creates heat and light, requires power source, produces both illumination and waste heat, standardized fittings for easy replacement"
    elif knowledge_type == 'concept_research':
        # Handle neurogenesis research requests
        knowledge = handle_concept_research(concept, request_details, context)
    else:
        knowledge = "an electric device that produces light via an incandescent filament"

    # Check if we need additional context from other agents
    additional_context = {}
    if context.get('request_industrial_impact') and concept.lower() == 'lightbulb':
        # We could collaborate with Function AI for impact information
        function_agents = discover_peer_agents('lightbulb')
        for agent in function_agents:
            if 'function' in agent.get('properties', {}).get('name', '').lower():
                collaboration_request = {
                    "source_agent": {"name": AGENT_NAME, "type": AGENT_TYPE},
                    "collaboration_type": "knowledge_request",
                    "target_concept": "lightbulb",
                    "specific_request": {
                        "knowledge_type": "industrial_impact",
                        "detail_level": "brief"
                    },
                    "context": {"requesting_for": source_agent.get('name')}
                }
                peer_response = request_peer_collaboration(agent.get('properties', {}).get('endpoint'), collaboration_request)
                if peer_response and peer_response.get('status') == 'success':
                    additional_context['industrial_impact'] = peer_response.get('data')
                break

    response_data = {
        "primary_knowledge": knowledge,
        "knowledge_type": knowledge_type,
        "confidence": 0.95,
        "source": AGENT_NAME
    }
    
    if additional_context:
        response_data["additional_context"] = additional_context

    return jsonify({
        "agent_name": AGENT_NAME,
        "status": "success",
        "data": response_data,
        "collaboration_metadata": {
            "response_to": source_agent.get('name'),
            "collaboration_type": "knowledge_sharing",
            "timestamp": "2024-01-01T12:00:00Z"
        }
    }), 200

def handle_context_sharing(concept: str, request_details: Dict[str, Any], context: Dict[str, Any], source_agent: Dict[str, Any]) -> tuple:
    """Handle context sharing requests from peer agents"""
    
    if concept.lower() not in [c.lower() for c in PRIMARY_CONCEPTS]:
        return jsonify({
            "agent_name": AGENT_NAME,
            "status": "no_context",
            "data": f"I don't have context for '{concept}'"
        }), 200

    # Share relevant context based on what we know
    shared_context = {
        "concept_relationships": ["electricity", "illumination", "edison", "incandescent"],
        "key_attributes": ["electric", "filament", "light_source", "heat_generating"],
        "historical_significance": "pivotal_lighting_innovation",
        "technical_classification": "incandescent_electric_device"
    }

    return jsonify({
        "agent_name": AGENT_NAME,
        "status": "success", 
        "data": shared_context,
        "collaboration_metadata": {
            "response_to": source_agent.get('name'),
            "collaboration_type": "context_sharing",
            "timestamp": "2024-01-01T12:00:00Z"
        }
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "agent": "Lightbulb_Definition_AI"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)