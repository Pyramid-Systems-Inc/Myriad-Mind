from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Orchestrator service URL
ORCHESTRATOR_URL = os.environ.get('ORCHESTRATOR_URL', 'http://orchestrator:5000')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the Integration Tester."""
    return jsonify({
        "status": "healthy",
        "service": "Integration Tester AI",
        "version": "1.0.0"
    })

@app.route('/run_orchestration', methods=['POST'])
def run_orchestration():
    """
    Receives a task list, forwards it to the Orchestrator service,
    and returns the collected agent results.
    """
    try:
        data = request.get_json()
        if not data or 'tasks' not in data:
            return jsonify({"status": "error", "message": "Request must include 'tasks' list"}), 400
        
        tasks = data['tasks']
        
        # Forward the request to the orchestrator service
        response = requests.post(
            f"{ORCHESTRATOR_URL}/process",
            json={"tasks": tasks},
            timeout=60
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                "status": "error",
                "message": f"Orchestrator returned status {response.status_code}",
                "details": response.text
            }), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Failed to connect to orchestrator: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)