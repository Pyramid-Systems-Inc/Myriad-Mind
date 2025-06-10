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
        
        # Handle the 'define' intent - this is where the cognitive logic resides
        if intent == 'define':
            # This is the "thinking" happening inside the agent
            definition = "an electric device that produces light via an incandescent filament"
            return jsonify({
                "agent_name": "Lightbulb_Definition_AI",
                "status": "success",
                "data": definition
            })
        else:
            return jsonify({
                "agent_name": "Lightbulb_Definition_AI",
                "status": "error",
                "data": f"Unknown intent: {intent}"
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