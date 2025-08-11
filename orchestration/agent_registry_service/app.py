# orchestration/agent_registry_service/app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# This will serve as our in-memory database for agents.
# The structure is: {(concept, intent): {agent_data}}
AGENT_DB = {}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the Agent Registry."""
    return jsonify({
        "status": "healthy",
        "service": "Agent Registry Service",
        "version": "1.0.0",
        "agents_registered": len(AGENT_DB)
    })

@app.route('/register', methods=['POST'])
def register_agent():
    """
    Registers an agent's capabilities and endpoint.
    Implements "Orchestrator-to-AgentRegistry (Register Agent)" protocol.
    """
    try:
        data = request.get_json()
        if not data or 'agent_name' not in data or 'concept' not in data or 'intent_map' not in data:
            return jsonify({"status": "error", "message": "Invalid registration data"}), 400

        concept = data['concept']
        intent_map = data['intent_map']

        for intent, path in intent_map.items():
            key = (concept.lower(), intent.lower())
            AGENT_DB[key] = data
            print(f"Registered: {key} -> {data['agent_name']}")
        
        # Mocked response from PROTOCOLS.md (Task 3.4.3)
        response_payload = {
            "registration_response": {
                "status": "success",
                "assigned_cluster": "default_cluster", # Mocked
                "agent_network_id": f"net_{data['agent_name'].lower()}",
                "message": f"Agent '{data['agent_name']}' registered for {len(intent_map)} intents."
            }
        }
        return jsonify(response_payload), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/discover', methods=['POST'])
def discover_agent():
    """
    Discovers an agent for a given concept and intent.
    """
    try:
        data = request.get_json()
        if not data or 'concept' not in data or 'intent' not in data:
            return jsonify({"status": "error", "message": "Missing 'concept' or 'intent'"}), 400

        key = (data['concept'].lower(), data['intent'].lower())
        agent_data = AGENT_DB.get(key)

        if agent_data:
            # Construct the specific endpoint from the intent_map
            endpoint = agent_data.get('endpoint', '')
            path = agent_data.get('intent_map', {}).get(data['intent'].lower(), '')
            full_url = f"{endpoint.rstrip('/')}{path}"

            return jsonify({
                "status": "success",
                "agent_name": agent_data['agent_name'],
                "endpoint": full_url
            })
        else:
            return jsonify({"status": "not_found", "message": "No agent found for the given concept and intent"}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/list', methods=['GET'])
def list_agents():
    """Lists all registered agent endpoints for debugging."""
    return jsonify({"registered_agents": {str(k): v for k, v in AGENT_DB.items()}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)