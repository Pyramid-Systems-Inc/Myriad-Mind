"""
Enhanced Output Processor Flask Service
Implements Task 3.2.4: Output Processor Flask Service

This Flask application provides HTTP endpoints for the Enhanced Output Processor,
following the established service patterns in the Myriad architecture.
"""

from flask import Flask, request, jsonify
import traceback
from typing import Dict, Any

from .output_processor import EnhancedOutputProcessor

app = Flask(__name__)

# Initialize the Enhanced Output Processor
processor = EnhancedOutputProcessor()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for service monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "Enhanced Output Processor",
        "version": "1.0.0",
        "capabilities": [
            "multi_agent_synthesis",
            "multi_format_output",
            "confidence_weighting",
            "evidence_attribution",
            "length_control"
        ]
    })

@app.route('/synthesize', methods=['POST'])
def synthesize_responses():
    """
    Main endpoint for processing collected results into final responses
    
    Expected input (basic format):
    {
        "query_id": "xyz-123",
        "collected_results": {
            "1": {"agent_name": "Agent1", "status": "success", "data": "response1"},
            "2": {"agent_name": "Agent2", "status": "success", "data": "response2"}
        }
    }
    
    Expected input (enhanced format):
    {
        "synthesis_request": {
            "query_metadata": {...},
            "agent_responses": {...},
            "synthesis_parameters": {...}
        }
    }
    
    Returns final synthesized and formatted response
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
        
        # Determine if this is basic or enhanced format
        if 'synthesis_request' in data:
            # Enhanced format
            synthesis_request = data['synthesis_request']
            final_response = processor.process_synthesis_request(synthesis_request)
            response_format = 'enhanced'
        elif 'query_id' in data and 'collected_results' in data:
            # Basic format (current Orchestrator)
            final_response = processor.process_collected_results(data)
            response_format = 'basic'
        else:
            return jsonify({
                "status": "error",
                "error_code": "INVALID_FORMAT",
                "error_message": "Request must contain either 'synthesis_request' or 'query_id' and 'collected_results'"
            }), 400
        
        # Return appropriate format
        if response_format == 'enhanced':
            response_data = processor.to_enhanced_response_format(final_response)
        else:
            response_data = processor.to_basic_response_format(final_response)
        
        return jsonify({
            "status": "success",
            "processor_name": "Enhanced_Output_Processor",
            **response_data
        })
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error processing synthesis request: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "error_code": "PROCESSING_ERROR",
            "error_message": f"Failed to process synthesis request: {str(e)}"
        }), 500

@app.route('/synthesize/basic', methods=['POST'])
def synthesize_basic():
    """
    Endpoint for basic synthesis (backward compatibility)
    
    Simplified interface for current system integration
    """
    try:
        if not request.json:
            return jsonify({
                "status": "error",
                "error_code": "INVALID_REQUEST",
                "error_message": "Request must contain JSON data"
            }), 400
        
        data = request.json
        
        # Ensure basic format
        if 'query_id' not in data or 'collected_results' not in data:
            return jsonify({
                "status": "error",
                "error_code": "MISSING_FIELDS",
                "error_message": "Request must contain 'query_id' and 'collected_results'"
            }), 400
        
        # Process with basic format
        final_response = processor.process_collected_results(data)
        basic_response = processor.to_basic_response_format(final_response)
        
        return jsonify({
            "status": "success",
            "processor_name": "Enhanced_Output_Processor",
            **basic_response
        })
        
    except Exception as e:
        print(f"Error in basic synthesis: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "error_code": "PROCESSING_ERROR",
            "error_message": f"Failed to process basic synthesis: {str(e)}"
        }), 500

@app.route('/synthesize/enhanced', methods=['POST'])
def synthesize_enhanced():
    """
    Endpoint for enhanced synthesis with full protocol support
    
    Supports all advanced features and parameters
    """
    try:
        if not request.json:
            return jsonify({
                "status": "error",
                "error_code": "INVALID_REQUEST",
                "error_message": "Request must contain JSON data"
            }), 400
        
        data = request.json
        
        # Ensure enhanced format
        if 'synthesis_request' not in data:
            return jsonify({
                "status": "error",
                "error_code": "MISSING_SYNTHESIS_REQUEST",
                "error_message": "Request must contain 'synthesis_request'"
            }), 400
        
        synthesis_request = data['synthesis_request']
        
        # Validate synthesis request structure
        required_fields = ['query_metadata', 'agent_responses', 'synthesis_parameters']
        missing_fields = [field for field in required_fields if field not in synthesis_request]
        
        if missing_fields:
            return jsonify({
                "status": "error",
                "error_code": "MISSING_FIELDS",
                "error_message": f"synthesis_request missing fields: {missing_fields}"
            }), 400
        
        # Process with enhanced format
        final_response = processor.process_synthesis_request(synthesis_request)
        enhanced_response = processor.to_enhanced_response_format(final_response)
        
        return jsonify({
            "status": "success",
            "processor_name": "Enhanced_Output_Processor",
            **enhanced_response
        })
        
    except Exception as e:
        print(f"Error in enhanced synthesis: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "error_code": "PROCESSING_ERROR",
            "error_message": f"Failed to process enhanced synthesis: {str(e)}"
        }), 500

@app.route('/format', methods=['POST'])
def format_content():
    """
    Endpoint for content formatting only (without synthesis)
    
    Useful for testing formatting capabilities or re-formatting existing content
    """
    try:
        if not request.json:
            return jsonify({
                "status": "error",
                "error_code": "INVALID_REQUEST",
                "error_message": "Request must contain JSON data"
            }), 400
        
        data = request.json
        
        # Required fields for formatting
        if 'content' not in data:
            return jsonify({
                "status": "error",
                "error_code": "MISSING_CONTENT",
                "error_message": "Request must contain 'content' field"
            }), 400
        
        content = data['content']
        formatting_params = data.get('formatting_parameters', {})
        
        # Parse formatting parameters
        parsed_params = processor._parse_formatting_parameters(formatting_params)
        
        # Format the content (using formatter directly)
        formatted_response = processor.formatter.format_response(
            synthesized_content=content,
            evidence_sources=data.get('evidence_sources', []),
            confidence_score=data.get('confidence_score', 0.8),
            synthesis_metadata=data.get('synthesis_metadata', {}),
            formatting_parameters=parsed_params,
            warnings=data.get('warnings', [])
        )
        
        return jsonify({
            "status": "success",
            "formatted_content": formatted_response.content,
            "format_type": formatted_response.format_type,
            "word_count": formatted_response.word_count,
            "citations": formatted_response.citations,
            "metadata": formatted_response.metadata
        })
        
    except Exception as e:
        print(f"Error in content formatting: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "error_code": "FORMATTING_ERROR",
            "error_message": f"Failed to format content: {str(e)}"
        }), 500

@app.route('/test', methods=['POST'])
def test_synthesis():
    """
    Test endpoint for development and debugging
    
    Provides sample data processing for testing
    """
    try:
        # Sample test data
        test_data = {
            "query_id": "test_query_001",
            "collected_results": {
                "1": {
                    "agent_name": "Test_Definition_AI",
                    "status": "success",
                    "data": "A lightbulb is an electric light source that produces light through the heating of a filament."
                },
                "2": {
                    "agent_name": "Test_Function_AI", 
                    "status": "success",
                    "data": "The lightbulb revolutionized factory work by extending working hours beyond daylight."
                }
            }
        }
        
        # Process test data
        final_response = processor.process_collected_results(test_data)
        basic_response = processor.to_basic_response_format(final_response)
        
        return jsonify({
            "status": "success",
            "test_result": "Test synthesis completed successfully",
            "sample_response": basic_response
        })
        
    except Exception as e:
        print(f"Error in test synthesis: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "error_code": "TEST_ERROR",
            "error_message": f"Test synthesis failed: {str(e)}"
        }), 500

if __name__ == '__main__':
    # For development/testing
    print("Starting Enhanced Output Processor Service...")
    print("Available endpoints:")
    print("  GET  /health - Health check")
    print("  POST /synthesize - Main synthesis endpoint (auto-detects format)")
    print("  POST /synthesize/basic - Basic compatibility mode")
    print("  POST /synthesize/enhanced - Enhanced protocol mode")
    print("  POST /format - Content formatting only")
    print("  POST /test - Test endpoint with sample data")
    
    app.run(host='0.0.0.0', port=5004, debug=True)
