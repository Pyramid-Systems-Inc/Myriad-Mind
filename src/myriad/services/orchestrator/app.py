from flask import Flask, request, jsonify, Response
import logging
import sys
import os

# Ensure the orchestrator module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from services.orchestrator.orchestrator import process_tasks, discover_agent_via_graph

# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service configuration
ORCHESTRATOR_VERSION = "1.0.0"

# Prometheus metrics
query_counter = Counter('orchestrator_queries_total', 'Total queries processed', ['status'])
query_duration = Histogram('orchestrator_query_duration_seconds', 'Query processing time')
active_agents = Gauge('orchestrator_active_agents', 'Number of active agents')
neurogenesis_counter = Counter('orchestrator_neurogenesis_total', 'Dynamic agents created')
task_success = Counter('orchestrator_task_success_total', 'Successful tasks')
task_failure = Counter('orchestrator_task_failure_total', 'Failed tasks')
agent_discovery_counter = Counter('orchestrator_agent_discovery_total', 'Agent discovery attempts', ['status'])

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "orchestrator",
        "version": ORCHESTRATOR_VERSION
    }), 200

@app.route('/process_query', methods=['POST'])
@app.route('/process', methods=['POST'])  # Maintain backward compatibility
@query_duration.time()
def process_query():
    """Main query processing endpoint - processes a list of tasks"""
    query_counter.labels(status='attempted').inc()
    
    try:
        data = request.json
        
        if not data:
            query_counter.labels(status='invalid').inc()
            return jsonify({"error": "No data provided"}), 400
        
        # Support both single task and multiple tasks
        if 'tasks' in data:
            # Multiple tasks format (integration tester compatibility)
            tasks = data.get('tasks')
            if not isinstance(tasks, list):
                query_counter.labels(status='invalid').inc()
                return jsonify({"error": "'tasks' must be a list"}), 400
            
            logger.info(f"Processing {len(tasks)} tasks")
            results = process_tasks(tasks)
            
            # Count successes and failures
            for task_id, result in results.items():
                if result.get('status') == 'success':
                    task_success.inc()
                else:
                    task_failure.inc()
            
            query_counter.labels(status='success').inc()
            return jsonify({
                "status": "success",
                "results": results
            }), 200
            
        elif 'query' in data:
            # Single query format (simple API)
            query = data.get('query')
            user_id = data.get('user_id', 'default')
            
            # Convert to task format
            task = {
                "task_id": 1,
                "concept": query,
                "intent": "define",  # Default intent
                "args": {"user_id": user_id}
            }
            
            logger.info(f"Processing single query: {query}")
            result = process_tasks([task])
            
            # Track success/failure
            task_result = result.get("1", {})
            if task_result.get('status') == 'success':
                task_success.inc()
            else:
                task_failure.inc()
            
            query_counter.labels(status='success').inc()
            return jsonify({
                "status": "success",
                "result": task_result
            }), 200
        else:
            query_counter.labels(status='invalid').inc()
            return jsonify({"error": "Request must include 'tasks' or 'query'"}), 400
            
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        task_failure.inc()
        query_counter.labels(status='error').inc()
        return jsonify({"error": str(e)}), 500

@app.route('/agents', methods=['GET'])
def list_agents():
    """List all available agents from the graph database"""
    try:
        # Import here to avoid circular dependencies
        from services.orchestrator.orchestrator import GRAPHDB_MANAGER_URL, _http_session
        
        # Query the graph database for all agent nodes
        payload = {
            "label": "Agent"
        }
        
        response = _http_session.post(
            f"{GRAPHDB_MANAGER_URL}/query_nodes",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            agents = data.get("nodes", [])
            
            # Format agent information
            agent_list = []
            for agent in agents:
                agent_list.append({
                    "name": agent.get("name"),
                    "type": agent.get("type"),
                    "endpoint": agent.get("endpoint"),
                    "status": agent.get("status", "unknown"),
                    "capabilities": agent.get("capabilities", [])
                })
            
            return jsonify({
                "agents": agent_list,
                "count": len(agent_list)
            }), 200
        else:
            logger.error(f"Failed to query agents: {response.status_code}")
            return jsonify({
                "error": "Failed to retrieve agents",
                "agents": [],
                "count": 0
            }), 500
            
    except Exception as e:
        logger.error(f"Error listing agents: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/metrics', methods=['GET'])
def metrics():
    """Expose Prometheus metrics"""
    try:
        # Update active agents gauge before returning metrics
        try:
            from services.orchestrator.orchestrator import GRAPHDB_MANAGER_URL, _http_session
            response = _http_session.post(
                f"{GRAPHDB_MANAGER_URL}/query_nodes",
                json={"label": "Agent"},
                timeout=5
            )
            if response.status_code == 200:
                agents = response.json().get("nodes", [])
                active_agents.set(len(agents))
        except Exception as e:
            logger.debug(f"Could not update active agents metric: {e}")
        
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    except Exception as e:
        logger.error(f"Error generating metrics: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/metrics/json', methods=['GET'])
def metrics_json():
    """Expose orchestrator metrics in JSON format (legacy endpoint)"""
    try:
        # Import performance engine if available
        from services.orchestrator.orchestrator import (
            PERFORMANCE_OPTIMIZATION_AVAILABLE,
            performance_engine
        )
        
        metrics_data = {
            "service": "orchestrator",
            "version": ORCHESTRATOR_VERSION,
            "features": {
                "dynamic_agents_enabled": os.environ.get("ENABLE_DYNAMIC_AGENTS", "true").lower() == "true",
                "autonomous_learning_enabled": os.environ.get("ENABLE_AUTONOMOUS_LEARNING", "true").lower() == "true",
                "performance_optimization_enabled": PERFORMANCE_OPTIMIZATION_AVAILABLE
            }
        }
        
        # Add performance metrics if available
        if PERFORMANCE_OPTIMIZATION_AVAILABLE and performance_engine:
            try:
                perf_stats = performance_engine.monitor.get_statistics()
                metrics_data["performance"] = perf_stats
            except Exception as pe:
                logger.warning(f"Could not retrieve performance statistics: {pe}")
                metrics_data["performance"] = {"error": "Performance statistics unavailable"}
        else:
            metrics_data["performance"] = {"status": "performance_engine_not_available"}
        
        return jsonify(metrics_data), 200
        
    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/discover', methods=['POST'])
def discover_agent():
    """Discover appropriate agent for a concept and intent"""
    try:
        data = request.json
        
        if not data or 'concept' not in data:
            agent_discovery_counter.labels(status='invalid').inc()
            return jsonify({"error": "Request must include 'concept'"}), 400
        
        concept = data.get('concept')
        intent = data.get('intent', 'define')
        
        logger.info(f"Discovering agent for concept '{concept}' with intent '{intent}'")
        
        agent_url = discover_agent_via_graph(concept, intent)
        
        if agent_url:
            agent_discovery_counter.labels(status='found').inc()
            return jsonify({
                "status": "success",
                "concept": concept,
                "intent": intent,
                "agent_url": agent_url
            }), 200
        else:
            agent_discovery_counter.labels(status='not_found').inc()
            return jsonify({
                "status": "no_agent_found",
                "concept": concept,
                "intent": intent,
                "agent_url": None,
                "message": f"No agent found for concept '{concept}' with intent '{intent}'"
            }), 404
            
    except Exception as e:
        logger.error(f"Error discovering agent: {str(e)}", exc_info=True)
        agent_discovery_counter.labels(status='error').inc()
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Get orchestrator service status and dependencies"""
    try:
        from services.orchestrator.orchestrator import (
            GRAPHDB_MANAGER_URL,
            LIFECYCLE_MANAGER_AVAILABLE,
            LEARNING_ENGINE_AVAILABLE,
            ENHANCED_INTELLIGENCE_AVAILABLE,
            PERFORMANCE_OPTIMIZATION_AVAILABLE,
            _http_session
        )
        
        # Check GraphDB Manager connectivity
        graphdb_status = "unknown"
        try:
            response = _http_session.get(f"{GRAPHDB_MANAGER_URL}/health", timeout=5)
            graphdb_status = "connected" if response.status_code == 200 else "disconnected"
        except:
            graphdb_status = "disconnected"
        
        status_data = {
            "service": "orchestrator",
            "status": "running",
            "version": ORCHESTRATOR_VERSION,
            "dependencies": {
                "graphdb_manager": graphdb_status,
                "lifecycle_manager": "available" if LIFECYCLE_MANAGER_AVAILABLE else "unavailable",
                "learning_engine": "available" if LEARNING_ENGINE_AVAILABLE else "unavailable",
                "enhanced_intelligence": "available" if ENHANCED_INTELLIGENCE_AVAILABLE else "unavailable",
                "performance_engine": "available" if PERFORMANCE_OPTIMIZATION_AVAILABLE else "unavailable"
            },
            "environment": {
                "graphdb_url": GRAPHDB_MANAGER_URL,
                "dynamic_agents": os.environ.get("ENABLE_DYNAMIC_AGENTS", "true"),
                "autonomous_learning": os.environ.get("ENABLE_AUTONOMOUS_LEARNING", "true")
            }
        }
        
        return jsonify(status_data), 200
        
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info(f"Starting Orchestrator Service v{ORCHESTRATOR_VERSION}")
    logger.info(f"GraphDB Manager URL: {os.environ.get('GRAPHDB_MANAGER_URL', 'http://graphdb-manager:5008')}")
    logger.info(f"Dynamic Agents: {os.environ.get('ENABLE_DYNAMIC_AGENTS', 'true')}")
    logger.info(f"Autonomous Learning: {os.environ.get('ENABLE_AUTONOMOUS_LEARNING', 'true')}")
    
    app.run(host='0.0.0.0', port=5000, debug=False)