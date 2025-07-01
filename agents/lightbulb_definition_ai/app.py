from flask import Flask, request, jsonify

app = Flask(__name__)

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

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "agent": "Lightbulb_Definition_AI"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)