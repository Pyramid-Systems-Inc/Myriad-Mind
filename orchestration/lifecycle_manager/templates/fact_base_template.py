# orchestration/lifecycle_manager/templates/fact_base_template.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# This agent's knowledge will be simple for now
KNOWLEDGE = {
    "definition": "A dynamically created agent for the concept '{{CONCEPT_NAME}}'.",
    "facts": [
        "This agent was created by the Lifecycle Manager.",
        "Its purpose is to store and retrieve facts about {{CONCEPT_NAME}}."
    ]
}

@app.route('/query', methods=['POST'])
def query():
    """
    Endpoint that accepts POST requests for '{{CONCEPT_NAME}}' queries.
    """
    try:
        data = request.get_json()
        if not data or 'intent' not in data:
            return jsonify({
                "agent_name": "{{AGENT_NAME}}",
                "status": "error",
                "data": "Missing 'intent' in request"
            }), 400
        
        intent = data['intent']
        
        if intent == 'define':
            response_data = KNOWLEDGE['definition']
        elif intent == 'get_facts':
            response_data = KNOWLEDGE['facts']
        else:
            return jsonify({
                "agent_name": "{{AGENT_NAME}}",
                "status": "error",
                "data": f"Unknown intent: {intent}. Supported intents: define, get_facts"
            }), 400
            
        return jsonify({
            "agent_name": "{{AGENT_NAME}}",
            "status": "success",
            "data": response_data
        })
            
    except Exception as e:
        return jsonify({
            "agent_name": "{{AGENT_NAME}}",
            "status": "error",
            "data": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "agent": "{{AGENT_NAME}}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port={{PORT}}, debug=True)