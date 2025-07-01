"""
Enhanced Input Processor Flask Service
Implements Task 3.1.6: Input Processor Flask Service

This Flask application provides HTTP endpoints for the Enhanced Input Processor,
following the established service patterns in the Myriad architecture.
"""

from flask import Flask, request, jsonify
import traceback
from typing import Dict, Any

from .input_processor import EnhancedInputProcessor

app = Flask(__name__)

# Initialize the Enhanced Input Processor
processor = EnhancedInputProcessor()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for service monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "Enhanced Input Processor",
        "version": "1.0.0",
        "capabilities": [
            "advanced_parsing",
            "intent_recognition", 
            "ambiguity_resolution",
            "task_list_generation"
        ]
    })

@app.route('/process', methods=['POST'])
def process_query():
    """
    Main endpoint for processing raw queries into task lists
    
    Expected input:
    {
        "query": "Why was the lightbulb important for factories?",
        "user_context": {
            "session_id": "sess_123",
            "previous_queries": [],
            "preferred_detail_level": "standard"
        }
    }
    
    Returns enhanced task list per PROTOCOLS.md
    """
    try:
        # Validate request
        if not request.json:
            return jsonify({
                "status": "error",
                "error_code": "INVALID_REQUEST",
                "error_message": "Request must contain JSON data"
            }), 400
        
        data = request.json
        
        # Extract query
        if 'query' not in data:
            return jsonify({
                "status": "error",
                "error_code": "MISSING_QUERY",
                "error_message": "Request must contain 'query' field"
            }), 400
        
        raw_query = data['query']
        user_context = data.get('user_context', {})
        
        # Process the query
        enhanced_task_list = processor.process_query(raw_query, user_context)
        
        # Return the enhanced task list
        return jsonify({
            "status": "success",
            "processor_name": "Enhanced_Input_Processor",
            "enhanced_task_list": {
                "protocol_version": enhanced_task_list.protocol_version,
                "query_metadata": enhanced_task_list.query_metadata,
                "parsed_query": enhanced_task_list.parsed_query,
                "task_list": enhanced_task_list.task_list,
                "ambiguity_info": enhanced_task_list.ambiguity_info,
                "processing_metadata": enhanced_task_list.processing_metadata
            }
        })
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error processing query: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "error_code": "PROCESSING_ERROR",
            "error_message": f"Failed to process query: {str(e)}"
        }), 500

@app.route('/process/basic', methods=['POST'])
def process_query_basic():
    """
    Endpoint for backward compatibility with existing Orchestrator
    
    Returns task list in the basic format expected by current Orchestrator
    """
    try:
        # Validate request
        if not request.json:
            return jsonify({
                "status": "error",
                "error_code": "INVALID_REQUEST", 
                "error_message": "Request must contain JSON data"
            }), 400
        
        data = request.json
        
        if 'query' not in data:
            return jsonify({
                "status": "error",
                "error_code": "MISSING_QUERY",
                "error_message": "Request must contain 'query' field"
            }), 400
        
        raw_query = data['query']
        user_context = data.get('user_context', {})
        
        # Process the query
        enhanced_task_list = processor.process_query(raw_query, user_context)
        
        # Convert to basic protocol format
        basic_task_list = processor.to_orchestrator_protocol(enhanced_task_list)
        
        return jsonify({
            "status": "success",
            "processor_name": "Enhanced_Input_Processor",
            "task_list": basic_task_list
        })
        
    except Exception as e:
        print(f"Error processing query (basic): {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "error_code": "PROCESSING_ERROR",
            "error_message": f"Failed to process query: {str(e)}"
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_query():
    """
    Endpoint for detailed query analysis without task generation
    
    Useful for debugging and understanding how queries are parsed
    """
    try:
        if not request.json or 'query' not in request.json:
            return jsonify({
                "status": "error",
                "error_message": "Request must contain 'query' field"
            }), 400
        
        raw_query = request.json['query']
        user_context = request.json.get('user_context', {})
        
        # Parse the query
        query_metadata, parsed_query = processor.parser.parse_query(raw_query, user_context)
        
        # Recognize intent
        intent_result = processor.intent_recognizer.recognize_intent(raw_query, user_context)
        
        # Detect ambiguity
        ambiguity_detection = processor.ambiguity_resolver.detect_ambiguity(
            raw_query, parsed_query.concepts, intent_result
        )
        
        return jsonify({
            "status": "success",
            "analysis": {
                "query_metadata": {
                    "query_id": query_metadata.query_id,
                    "original_query": query_metadata.original_query,
                    "timestamp": query_metadata.timestamp
                },
                "parsed_query": {
                    "primary_intent": parsed_query.primary_intent,
                    "concepts": parsed_query.concepts,
                    "relationships": parsed_query.relationships,
                    "complexity_score": parsed_query.complexity_score,
                    "estimated_agents_needed": parsed_query.estimated_agents_needed
                },
                "intent_analysis": {
                    "primary_intent": intent_result.primary_intent,
                    "confidence": intent_result.confidence,
                    "alternative_intents": intent_result.alternative_intents,
                    "is_ambiguous": intent_result.is_ambiguous
                },
                "ambiguity_analysis": {
                    "is_ambiguous": ambiguity_detection.is_ambiguous,
                    "ambiguity_type": ambiguity_detection.ambiguity_type.value if ambiguity_detection.ambiguity_type else None,
                    "ambiguous_elements": ambiguity_detection.ambiguous_elements,
                    "suggested_clarifications": ambiguity_detection.suggested_clarifications
                }
            }
        })
        
    except Exception as e:
        print(f"Error analyzing query: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "error_code": "ANALYSIS_ERROR",
            "error_message": f"Failed to analyze query: {str(e)}"
        }), 500

if __name__ == '__main__':
    # For development/testing
    print("Starting Enhanced Input Processor Service...")
    print("Available endpoints:")
    print("  GET  /health - Health check")
    print("  POST /process - Full enhanced processing")
    print("  POST /process/basic - Basic compatibility mode")
    print("  POST /analyze - Query analysis only")
    
    app.run(host='0.0.0.0', port=5003, debug=True)
