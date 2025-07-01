from flask import Flask, request, jsonify

app = Flask(__name__)

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

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "agent": "Lightbulb_Function_AI"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)