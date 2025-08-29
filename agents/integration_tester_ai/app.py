from flask import Flask, request, jsonify
import sys
import os

# Ensure the orchestration module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from orchestration.orchestrator import process_tasks

app = Flask(__name__)

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
    Receives a task list, runs the orchestration logic inside the container,
    and returns the collected agent results.
    """
    try:
        data = request.get_json()
        if not data or 'tasks' not in data:
            return jsonify({"status": "error", "message": "Request must include 'tasks' list"}), 400
        
        tasks = data['tasks']
        
        # This function now runs inside the Docker network, so it can resolve service names.
        results = process_tasks(tasks)
        
        return jsonify({
            "status": "success",
            "results": results
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)