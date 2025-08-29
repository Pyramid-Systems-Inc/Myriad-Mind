from flask import Flask, request, jsonify
import requests
import os
from typing import Optional, Dict, Any

app = Flask(__name__)

# Agent-to-Agent Communication Configuration
GRAPHDB_MANAGER_URL = os.environ.get("GRAPHDB_MANAGER_URL", "http://graphdb_manager_ai:5008")
AGENT_NAME = "Lightbulb_Function_AI"
AGENT_TYPE = "FunctionExecutor"
PRIMARY_CONCEPTS = ["lightbulb", "factories"]

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

# Internal state for the simulated lightbulb
lightbulb_state = {
    "is_on": False,
    "brightness": 0  # 0-100 scale
}

@app.route('/query', methods=['POST'])
def query():
    """
    Endpoint that accepts POST requests for lightbulb function queries.
    Implements the Agent-to-Orchestrator Protocol (The "Agent Result").
    """
    try:
        # Get the intent from the request
        data = request.get_json()
        if not data or 'intent' not in data:
            return jsonify({
                "agent_name": "Lightbulb_Function_AI",
                "status": "error",
                "data": "Missing 'intent' in request"
            }), 400
        
        intent = data['intent']
        
        # Handle different function intents - this is where the cognitive logic resides
        if intent == 'explain_limitation':
            # This is the "thinking" happening inside the agent for roadmap requirement
            reasoned_limitation = "it generates significant waste heat, making it inefficient."
            return jsonify({
                "agent_name": "Lightbulb_Function_AI",
                "status": "success",
                "data": reasoned_limitation
            })

        elif intent == 'explain_impact':
            # Explain the impact of lightbulbs, especially in industrial/factory contexts
            concept = data.get('concept', '').lower()
            if 'factor' in concept or 'industrial' in concept:
                impact = "Lightbulbs revolutionized factory work by extending productive hours beyond daylight, improving worker safety through better illumination, and enabling 24-hour industrial operations that dramatically increased productivity."
            else:
                impact = "The lightbulb transformed society by extending usable hours, improving safety through better lighting, and enabling new forms of work and social activities after dark."
            return jsonify({
                "agent_name": "Lightbulb_Function_AI",
                "status": "success",
                "data": impact
            })

        elif intent == 'compare':
            # Handle comparison queries
            concept = data.get('concept', '').lower()
            if 'candle' in concept or 'versus' in concept:
                comparison = "Lightbulbs provided consistent, bright illumination without fire hazards, smoke, or the need for constant replacement like candles. In factories, this meant safer working conditions, no risk of fires from open flames, and reliable lighting that didn't dim over time."
            else:
                comparison = "Lightbulbs offer superior brightness, safety, and reliability compared to traditional lighting methods."
            return jsonify({
                "agent_name": "Lightbulb_Function_AI",
                "status": "success",
                "data": comparison
            })

        elif intent == 'synthesize_response':
            # Handle synthesis requests for complex multi-concept queries
            synthesis = "The lightbulb's importance for factories stemmed from its ability to provide safe, reliable illumination that extended working hours, improved productivity, and reduced fire hazards compared to gas or candle lighting."
            return jsonify({
                "agent_name": "Lightbulb_Function_AI",
                "status": "success",
                "data": synthesis
            })
            
        elif intent == 'turn_on':
            # Turn the lightbulb on
            lightbulb_state["is_on"] = True
            if lightbulb_state["brightness"] == 0:
                lightbulb_state["brightness"] = 100  # Default full brightness
            return jsonify({
                "agent_name": "Lightbulb_Function_AI",
                "status": "success",
                "data": f"Lightbulb turned on at {lightbulb_state['brightness']}% brightness"
            })
            
        elif intent == 'turn_off':
            # Turn the lightbulb off
            lightbulb_state["is_on"] = False
            return jsonify({
                "agent_name": "Lightbulb_Function_AI",
                "status": "success",
                "data": "Lightbulb turned off"
            })
            
        elif intent == 'dim':
            # Set brightness level
            brightness = data.get('args', {}).get('brightness', 50)  # Default to 50% if not specified
            try:
                brightness = int(brightness)
                if brightness < 0 or brightness > 100:
                    return jsonify({
                        "agent_name": "Lightbulb_Function_AI",
                        "status": "error",
                        "data": "Brightness must be between 0 and 100"
                    }), 400
                
                lightbulb_state["brightness"] = brightness
                if brightness > 0:
                    lightbulb_state["is_on"] = True
                else:
                    lightbulb_state["is_on"] = False
                    
                return jsonify({
                    "agent_name": "Lightbulb_Function_AI",
                    "status": "success",
                    "data": f"Lightbulb brightness set to {brightness}%"
                })
            except (ValueError, TypeError):
                return jsonify({
                    "agent_name": "Lightbulb_Function_AI",
                    "status": "error",
                    "data": "Invalid brightness value. Must be a number between 0 and 100"
                }), 400
                
        elif intent == 'status':
            # Return current state
            status_msg = f"Lightbulb is {'on' if lightbulb_state['is_on'] else 'off'}"
            if lightbulb_state['is_on']:
                status_msg += f" at {lightbulb_state['brightness']}% brightness"
            return jsonify({
                "agent_name": "Lightbulb_Function_AI",
                "status": "success",
                "data": status_msg
            })
            
        else:
            return jsonify({
                "agent_name": "Lightbulb_Function_AI",
                "status": "error",
                "data": f"Unknown intent: {intent}"
            }), 400
            
    except Exception as e:
        return jsonify({
            "agent_name": "Lightbulb_Function_AI",
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
        elif collaboration_type == 'function_execution':
            return handle_function_execution(target_concept, specific_request, context, source_agent)
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
    knowledge_type = request_details.get('knowledge_type', 'impact')
    
    if knowledge_type == 'industrial_impact':
        knowledge = "Lightbulbs revolutionized factory work by extending productive hours beyond daylight, improving worker safety through better illumination, and enabling 24-hour industrial operations that dramatically increased productivity."
    elif knowledge_type == 'limitations':
        knowledge = "it generates significant waste heat, making it inefficient."
    elif knowledge_type == 'factory_applications':
        knowledge = "In factories, lightbulbs enabled night shifts, improved precision work visibility, reduced fire hazards from gas/candle lighting, and allowed for better quality control through consistent illumination."
    elif knowledge_type == 'historical_timeline':
        # Let's collaborate with Definition AI for historical context
        definition_agents = discover_peer_agents('lightbulb')
        historical_info = None
        for agent in definition_agents:
            if 'definition' in agent.get('properties', {}).get('name', '').lower():
                collaboration_request = {
                    "source_agent": {"name": AGENT_NAME, "type": AGENT_TYPE},
                    "collaboration_type": "knowledge_request",
                    "target_concept": "lightbulb",
                    "specific_request": {
                        "knowledge_type": "historical_context",
                        "detail_level": "brief"
                    },
                    "context": {"requesting_for": source_agent.get('name')}
                }
                peer_response = request_peer_collaboration(agent.get('properties', {}).get('endpoint'), collaboration_request)
                if peer_response and peer_response.get('status') == 'success':
                    historical_info = peer_response.get('data', {}).get('primary_knowledge')
                break
        
        if historical_info:
            knowledge = f"From a functional perspective: {historical_info} The adoption in factories was rapid due to immediate productivity benefits."
        else:
            knowledge = "Factory adoption of lightbulbs occurred rapidly in the 1880s due to immediate productivity and safety benefits."
    else:
        knowledge = "Lightbulbs transformed factory operations by enabling extended working hours and improving workplace safety."

    response_data = {
        "primary_knowledge": knowledge,
        "knowledge_type": knowledge_type,
        "confidence": 0.90,
        "source": AGENT_NAME,
        "functional_perspective": True
    }

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

    # Share functional and application-focused context
    shared_context = {
        "functional_relationships": ["factories", "productivity", "working_hours", "safety"],
        "key_impacts": ["extended_hours", "improved_safety", "increased_productivity", "quality_control"],
        "application_domains": ["industrial", "manufacturing", "night_operations"],
        "performance_metrics": ["productivity_increase", "accident_reduction", "operational_hours"]
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

def handle_function_execution(concept: str, request_details: Dict[str, Any], context: Dict[str, Any], source_agent: Dict[str, Any]) -> tuple:
    """Handle function execution requests from peer agents"""
    
    function_type = request_details.get('function_type', 'analyze')
    
    if function_type == 'impact_analysis':
        # Perform impact analysis for the requesting agent
        analysis_result = {
            "impact_category": "industrial_transformation",
            "primary_benefits": [
                "Extended operational hours (8-12 to 16-24 hours)",
                "Improved worker safety (reduced fire hazards)",
                "Enhanced precision work capability",
                "Increased overall productivity (20-40% improvement)"
            ],
            "quantitative_estimates": {
                "productivity_increase": "20-40%",
                "operational_hour_extension": "100-200%",
                "safety_improvement": "significant_reduction_in_fire_incidents"
            },
            "analysis_confidence": 0.85
        }
        
        return jsonify({
            "agent_name": AGENT_NAME,
            "status": "success",
            "data": analysis_result,
            "collaboration_metadata": {
                "response_to": source_agent.get('name'),
                "collaboration_type": "function_execution",
                "function_performed": "impact_analysis",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }), 200
    
    else:
        return jsonify({
            "agent_name": AGENT_NAME,
            "status": "function_not_supported",
            "data": f"Function type '{function_type}' not supported. Available functions: impact_analysis"
        }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "agent": "Lightbulb_Function_AI"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)