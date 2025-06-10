"""
Lightbulb_AI Agent - A specialized microservice for lightbulb-related knowledge
Part of the Myriad Cognitive Architecture
"""

from flask import Flask, request, jsonify
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

class LightbulbAI:
    def __init__(self):
        """Initialize the Lightbulb AI agent."""
        self.agent_name = "Lightbulb_AI"
        logger.info(f"{self.agent_name} initialized")
    
    def get_status(self):
        """Return the current status of the agent."""
        return {
            "status": "Lightbulb_AI is online",
            "agent_name": self.agent_name,
            "version": "1.0.0",
            "type": "specialized_knowledge_agent"
        }
    
    def process_query(self, query_data):
        """
        Process a query and return relevant information.
        For Phase 1, this returns a hardcoded success message.
        """
        logger.info(f"Processing query: {query_data}")
        
        # Phase 1: Return hardcoded success message
        response = {
            "source_agent": self.agent_name,
            "status": "Lightbulb_AI is online",
            "query_processed": True,
            "message": "Agent is ready and operational"
        }
        
        logger.info(f"Query processed successfully: {response}")
        return response

# Initialize the agent
lightbulb_ai = LightbulbAI()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the agent."""
    logger.info("Health check requested")
    return jsonify({"status": "healthy", "agent": "Lightbulb_AI"})

@app.route('/query', methods=['GET', 'POST'])
def query_endpoint():
    """
    Main query endpoint for the agent.
    Accepts both GET and POST requests.
    """
    try:
        # Handle both GET and POST requests
        if request.method == 'GET':
            query_data = request.args.to_dict()
        else:  # POST
            query_data = request.get_json() or {}
        
        logger.info(f"Received query request: {query_data}")
        
        # Process the query
        response = lightbulb_ai.process_query(query_data)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({
            "source_agent": "Lightbulb_AI",
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/info', methods=['GET'])
def agent_info():
    """Return information about this agent."""
    info = {
        "agent_name": "Lightbulb_AI",
        "description": "Specialized AI agent for lightbulb and lighting-related knowledge",
        "version": "1.0.0",
        "endpoints": [
            "/health - Health check",
            "/query - Main query endpoint",
            "/info - Agent information"
        ],
        "architecture": "Myriad Cognitive Architecture",
        "phase": "Phase 1 - Foundation"
    }
    return jsonify(info)

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - returns basic agent status."""
    return jsonify(lightbulb_ai.get_status())

if __name__ == '__main__':
    # Get port from environment variable or default to 5001
    port = int(os.environ.get('PORT', 5001))
    
    logger.info(f"Starting {lightbulb_ai.agent_name} on port {port}")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',  # Accept connections from all interfaces
        port=port,
        debug=False  # Set to False for production
    )