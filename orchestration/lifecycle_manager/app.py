from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the Lifecycle Manager."""
    return jsonify({
        "status": "healthy",
        "service": "Lifecycle Manager",
        "version": "1.0.0"
    })

@app.route('/create_agent', methods=['POST'])
def create_agent():
    """
    Endpoint to handle agent creation requests.
    Initially, this will be a mocked response.
    Implements "Orchestrator-to-LifecycleManager (Agent Creation Request)" protocol.
    """
    try:
        data = request.get_json()
        if not data or 'concept_name' not in data or 'agent_type' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'concept_name' or 'agent_type' in request"
            }), 400

        concept_name = data['concept_name']
        agent_type = data['agent_type']

        # Mocked response for now. In the future, this will trigger scaffolding.
        new_agent_name = f"{concept_name.replace(' ', '_').capitalize()}_{agent_type}_AI"
        mocked_endpoint = f"http://{new_agent_name.lower()}:5005/query"

        # Implements "LifecycleManager-to-Orchestrator (Agent Creation Confirmation)"
        response_payload = {
            "agent_name": new_agent_name,
            "status": "success",
            "endpoint": mocked_endpoint,
            "message": "Mocked: Agent creation process initiated."
        }
        
        return jsonify(response_payload), 202 # 202 Accepted, as creation is not instant

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)