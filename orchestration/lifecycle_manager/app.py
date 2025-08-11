# orchestration/lifecycle_manager/app.py
import os
import shutil
import docker
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize Docker client
# This will work inside the container because we mount the docker.sock
try:
    docker_client = docker.from_env()
except docker.errors.DockerException:
    print("WARNING: Could not connect to Docker daemon. Agent deployment will be disabled.")
    docker_client = None

PORT_COUNTER = 5006 # Start after registry

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the Lifecycle Manager."""
    docker_status = "connected" if docker_client else "disconnected"
    return jsonify({
        "status": "healthy",
        "service": "Lifecycle Manager",
        "version": "1.0.0",
        "docker_status": docker_status
    })

@app.route('/create_agent', methods=['POST'])
def create_agent():
    """
    Endpoint to handle agent creation requests.
    This version scaffolds files, builds the Docker image, and runs the container.
    """
    global PORT_COUNTER
    if not docker_client:
        return jsonify({"status": "error", "message": "Docker client not available."}), 503

    try:
        data = request.get_json()
        if not data or 'concept_name' not in data or 'agent_type' not in data:
            return jsonify({"status": "error", "message": "Missing 'concept_name' or 'agent_type' in request"}), 400

        concept_name = data['concept_name']
        agent_type = data['agent_type']
        
        # --- Scaffolding Logic ---
        agent_name = f"{concept_name.replace(' ', '_').capitalize()}_{agent_type}_AI"
        agent_name_lower = agent_name.lower()
        agent_dir_relative = os.path.join('agents', agent_name_lower)
        agent_dir_absolute = os.path.abspath(agent_dir_relative)

        if os.path.exists(agent_dir_absolute):
            return jsonify({"status": "error", "message": f"Agent '{agent_name}' already exists."}), 409

        os.makedirs(agent_dir_absolute, exist_ok=True)
        
        if agent_type != 'FactBase':
            return jsonify({"status": "error", "message": f"Agent type '{agent_type}' not supported."}), 400

        PORT_COUNTER += 1
        new_port = PORT_COUNTER
        template_path = os.path.join(os.path.dirname(__file__), 'templates/fact_base_template.py')
        
        with open(template_path, 'r') as f:
            template_content = f.read()

        content = template_content.replace('{{CONCEPT_NAME}}', concept_name)
        content = content.replace('{{AGENT_NAME}}', agent_name)
        content = content.replace('{{PORT}}', str(new_port))

        with open(os.path.join(agent_dir_absolute, 'app.py'), 'w') as f:
            f.write(content)
            
        shutil.copyfile('agents/lightbulb_definition_ai/Dockerfile', os.path.join(agent_dir_absolute, 'Dockerfile'))

        image, _ = docker_client.images.build(path=agent_dir_absolute, tag=agent_name_lower, rm=True)
        container = docker_client.containers.run(
            agent_name_lower, detach=True, name=agent_name_lower,
            ports={f'{new_port}/tcp': new_port}, network='myriad-mind_myriad_network'
        )
        
        intent_map = {"define": "/query", "get_facts": "/query"}

        response_payload = {
            "agent_name": agent_name,
            "status": "success",
            "container_id": container.id,
            "endpoint": f"http://{agent_name_lower}:{new_port}",
            "port": new_port,
            "intent_map": intent_map,
            "message": f"Agent '{agent_name}' deployed successfully."
        }
        
        return jsonify(response_payload), 201

    except docker.errors.BuildError as e:
        return jsonify({"status": "error", "message": "Docker build failed.", "logs": str(e)}), 500
    except Exception as e:
        # Clean up created directory on failure
        if 'agent_dir_absolute' in locals() and os.path.exists(agent_dir_absolute):
             shutil.rmtree(agent_dir_absolute)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)