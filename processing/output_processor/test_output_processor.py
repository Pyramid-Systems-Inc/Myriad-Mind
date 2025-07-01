"""
Comprehensive Unit Tests for Enhanced Output Processor
Implements Task 3.2.5: Write Comprehensive Unit Tests

Tests all components: Synthesizer, Formatter, and main Output Processor
"""

import pytest
import json
from unittest.mock import Mock, patch

from .synthesizer import AdvancedSynthesizer, SynthesisParameters, AgentResponse
from .formatter import MultiFormatFormatter, FormattingParameters, OutputFormat, TargetLength, EvidenceLevel
from .output_processor import EnhancedOutputProcessor
from .app import app

class TestAdvancedSynthesizer:
    """Test cases for the Advanced Synthesizer component"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.synthesizer = AdvancedSynthesizer()
    
    def test_structure_responses_basic_format(self):
        """Test structuring responses from basic format"""
        agent_responses = {
            "1": {"agent_name": "Test_Agent", "status": "success", "data": "Test response"},
            "2": {"agent_name": "Another_Agent", "status": "success", "data": "Another response"}
        }
        
        structured = self.synthesizer._structure_responses(agent_responses)
        
        assert len(structured) == 2
        assert structured[0].agent_id == "Test_Agent"
        assert structured[0].content == "Test response"
        assert structured[0].confidence == 0.8  # Default for basic format
    
    def test_structure_responses_enhanced_format(self):
        """Test structuring responses from enhanced format"""
        agent_responses = {
            "1": {
                "agent_id": "enhanced_agent_001",
                "content": "Enhanced response",
                "confidence": 0.95,
                "contribution_weight": 0.7
            }
        }
        
        structured = self.synthesizer._structure_responses(agent_responses)
        
        assert len(structured) == 1
        assert structured[0].agent_id == "enhanced_agent_001"
        assert structured[0].confidence == 0.95
        assert structured[0].contribution_weight == 0.7
    
    def test_filter_by_confidence(self):
        """Test confidence-based filtering"""
        responses = [
            AgentResponse("agent1", "1", "content1", 0.9, 1.0),
            AgentResponse("agent2", "2", "content2", 0.4, 1.0),
            AgentResponse("agent3", "3", "content3", 0.7, 1.0)
        ]
        
        filtered = self.synthesizer._filter_by_confidence(responses, 0.6)
        
        assert len(filtered) == 2
        assert all(r.confidence >= 0.6 for r in filtered)
    
    def test_analyze_correlations(self):
        """Test correlation analysis between responses"""
        responses = [
            AgentResponse("agent1", "1", "The lightbulb was important because it extended working hours", 0.9, 1.0),
            AgentResponse("agent2", "2", "Furthermore, electric lighting improved factory safety", 0.8, 1.0)
        ]
        
        correlations = self.synthesizer._analyze_correlations(responses)
        
        assert 'reinforcement_pairs' in correlations
        assert 'contradiction_pairs' in correlations
        assert 'content_overlap' in correlations
    
    def test_synthesize_responses_success(self):
        """Test successful synthesis of multiple responses"""
        agent_responses = {
            "1": {"agent_name": "Definition_AI", "status": "success", "data": "A lightbulb produces light"},
            "2": {"agent_name": "Impact_AI", "status": "success", "data": "It revolutionized factory work"}
        }
        
        synthesis_params = SynthesisParameters()
        query_metadata = {"synthesis_intent": "explain_importance"}
        
        result = self.synthesizer.synthesize_responses(
            agent_responses, synthesis_params, query_metadata
        )
        
        assert result.synthesized_content is not None
        assert len(result.synthesized_content) > 0
        assert result.confidence_score > 0
        assert len(result.evidence_sources) > 0
    
    def test_synthesize_responses_low_confidence(self):
        """Test synthesis with low confidence responses"""
        agent_responses = {
            "1": {"agent_name": "Uncertain_AI", "status": "success", "data": "Maybe it's important"}
        }
        
        synthesis_params = SynthesisParameters(confidence_threshold=0.9)
        query_metadata = {}
        
        result = self.synthesizer.synthesize_responses(
            agent_responses, synthesis_params, query_metadata
        )
        
        assert result.confidence_score == 0.0
        assert "insufficient confident data" in result.synthesized_content.lower()
        assert len(result.warnings) > 0

class TestMultiFormatFormatter:
    """Test cases for the Multi-format Formatter component"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.formatter = MultiFormatFormatter()
    
    def test_format_explanatory_paragraph(self):
        """Test explanatory paragraph formatting"""
        content = "The lightbulb was important. It extended working hours. It improved safety."
        sources = ["Definition_AI", "Impact_AI"]
        
        params = FormattingParameters(
            output_format=OutputFormat.EXPLANATORY_PARAGRAPH,
            target_length=TargetLength.STANDARD,
            evidence_level=EvidenceLevel.STANDARD
        )
        
        result = self.formatter.format_response(
            content, sources, 0.85, {}, params
        )
        
        assert result.format_type == "explanatory_paragraph"
        assert "Sources:" in result.content
        assert result.word_count > 0
    
    def test_format_structured_list(self):
        """Test structured list formatting"""
        content = "First point about lightbulbs. Second point about factories. Third point about impact."
        sources = ["Test_AI"]
        
        params = FormattingParameters(
            output_format=OutputFormat.STRUCTURED_LIST,
            target_length=TargetLength.BRIEF,
            evidence_level=EvidenceLevel.MINIMAL
        )
        
        result = self.formatter.format_response(
            content, sources, 0.9, {}, params
        )
        
        assert result.format_type == "structured_list"
        assert "1." in result.content or "•" in result.content
    
    def test_length_control_brief(self):
        """Test length control for brief responses"""
        long_content = " ".join(["This is a very long sentence with many words."] * 20)
        
        truncated = self.formatter._apply_length_control(long_content, TargetLength.BRIEF)
        word_count = len(truncated.split())
        
        assert word_count <= 100  # Brief target maximum
    
    def test_length_control_detailed(self):
        """Test length control for detailed responses"""
        short_content = "Short content."
        
        # Should not truncate short content
        result = self.formatter._apply_length_control(short_content, TargetLength.DETAILED)
        
        assert result == short_content
    
    def test_evidence_attribution_levels(self):
        """Test different evidence attribution levels"""
        content = "Test content"
        sources = ["Agent1", "Agent2"]
        
        # Test minimal level
        result_minimal, citations_minimal = self.formatter._add_evidence_attribution(
            content, sources, EvidenceLevel.MINIMAL
        )
        assert result_minimal == content  # No attribution added
        
        # Test standard level
        result_standard, citations_standard = self.formatter._add_evidence_attribution(
            content, sources, EvidenceLevel.STANDARD
        )
        assert "Sources:" in result_standard
        assert len(citations_standard) > 0
    
    def test_confidence_indicator_generation(self):
        """Test confidence indicator generation"""
        high_conf = self.formatter._generate_confidence_indicator(0.95)
        low_conf = self.formatter._generate_confidence_indicator(0.3)
        
        assert "high confidence" in high_conf
        assert "low confidence" in low_conf or "uncertain" in low_conf

class TestEnhancedOutputProcessor:
    """Test cases for the main Enhanced Output Processor"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.processor = EnhancedOutputProcessor()
    
    def test_process_collected_results_basic(self):
        """Test processing basic collected results format"""
        collected_results = {
            "query_id": "test_123",
            "collected_results": {
                "1": {"agent_name": "Test_Agent", "status": "success", "data": "Test response"}
            }
        }
        
        result = self.processor.process_collected_results(collected_results)
        
        assert result.status == "success"
        assert result.query_id == "test_123"
        assert len(result.final_content) > 0
        assert result.confidence_score > 0
    
    def test_process_synthesis_request_enhanced(self):
        """Test processing enhanced synthesis request"""
        synthesis_request = {
            "query_metadata": {
                "query_id": "enhanced_test_456",
                "original_query": "Test query",
                "synthesis_intent": "explain_importance"
            },
            "agent_responses": {
                "1": {
                    "agent_id": "test_agent_001",
                    "content": "Test response content",
                    "confidence": 0.9,
                    "contribution_weight": 1.0
                }
            },
            "synthesis_parameters": {
                "output_format": "explanatory_paragraph",
                "target_length": "standard",
                "evidence_level": "standard"
            }
        }
        
        result = self.processor.process_synthesis_request(synthesis_request)
        
        assert result.status == "success"
        assert result.query_id == "enhanced_test_456"
        assert result.response_metadata is not None
    
    def test_parameter_parsing(self):
        """Test parsing of synthesis and formatting parameters"""
        params_dict = {
            "output_format": "structured_list",
            "target_length": "detailed",
            "evidence_level": "academic",
            "causal_chain_emphasis": True
        }
        
        synthesis_params = self.processor._parse_synthesis_parameters(params_dict)
        formatting_params = self.processor._parse_formatting_parameters(params_dict)
        
        assert synthesis_params.output_format == "structured_list"
        assert synthesis_params.causal_chain_emphasis == True
        assert formatting_params.output_format == OutputFormat.STRUCTURED_LIST
        assert formatting_params.target_length == TargetLength.DETAILED
        assert formatting_params.evidence_level == EvidenceLevel.ACADEMIC
    
    def test_response_format_conversion(self):
        """Test conversion between basic and enhanced response formats"""
        # Create a sample final response
        from .output_processor import FinalResponse
        final_response = FinalResponse(
            response_id="resp_test_001",
            query_id="query_test_001",
            final_content="Test final content",
            confidence_score=0.85,
            response_metadata={"test": "metadata"},
            processing_time_ms=150
        )
        
        # Test basic format conversion
        basic_format = self.processor.to_basic_response_format(final_response)
        assert "final_answer" in basic_format
        assert basic_format["confidence"] == 0.85
        
        # Test enhanced format conversion
        enhanced_format = self.processor.to_enhanced_response_format(final_response)
        assert "final_response" in enhanced_format
        assert "response_metadata" in enhanced_format
    
    def test_quality_assessment(self):
        """Test response quality assessment methods"""
        from .formatter import FormattedResponse
        
        # Test completeness assessment
        good_response = FormattedResponse(
            content="This is a well-formed response with sufficient detail and proper structure.",
            format_type="explanatory_paragraph",
            word_count=120,
            confidence_indicator="high confidence",
            citations=["Agent1", "Agent2"],
            metadata={}
        )
        
        completeness = self.processor._assess_completeness(good_response)
        coherence = self.processor._assess_coherence(good_response)
        
        assert completeness > 0.5
        assert coherence > 0.5

class TestOutputProcessorFlaskApp:
    """Test cases for the Flask application"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'capabilities' in data
    
    def test_synthesize_basic_endpoint(self):
        """Test basic synthesis endpoint"""
        payload = {
            "query_id": "test_query",
            "collected_results": {
                "1": {"agent_name": "Test_Agent", "status": "success", "data": "Test response"}
            }
        }
        
        response = self.app.post('/synthesize/basic',
                               data=json.dumps(payload),
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'final_answer' in data
    
    def test_synthesize_enhanced_endpoint(self):
        """Test enhanced synthesis endpoint"""
        payload = {
            "synthesis_request": {
                "query_metadata": {
                    "query_id": "enhanced_test",
                    "original_query": "Test query"
                },
                "agent_responses": {
                    "1": {
                        "agent_id": "test_agent",
                        "content": "Test content",
                        "confidence": 0.9,
                        "contribution_weight": 1.0
                    }
                },
                "synthesis_parameters": {
                    "output_format": "explanatory_paragraph",
                    "target_length": "standard"
                }
            }
        }
        
        response = self.app.post('/synthesize/enhanced',
                               data=json.dumps(payload),
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'final_response' in data
    
    def test_format_endpoint(self):
        """Test content formatting endpoint"""
        payload = {
            "content": "Test content to format",
            "formatting_parameters": {
                "output_format": "structured_list",
                "target_length": "brief"
            },
            "evidence_sources": ["Test_Agent"],
            "confidence_score": 0.8
        }
        
        response = self.app.post('/format',
                               data=json.dumps(payload),
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'formatted_content' in data
    
    def test_test_endpoint(self):
        """Test the test endpoint"""
        response = self.app.post('/test')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'sample_response' in data
    
    def test_auto_format_detection(self):
        """Test automatic format detection in main synthesize endpoint"""
        # Test basic format detection
        basic_payload = {
            "query_id": "test",
            "collected_results": {
                "1": {"agent_name": "Test", "status": "success", "data": "Test"}
            }
        }
        
        response = self.app.post('/synthesize',
                               data=json.dumps(basic_payload),
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'final_answer' in data  # Basic format response
        
        # Test enhanced format detection
        enhanced_payload = {
            "synthesis_request": {
                "query_metadata": {"query_id": "test"},
                "agent_responses": {"1": {"agent_id": "test", "content": "test", "confidence": 0.8}},
                "synthesis_parameters": {"output_format": "explanatory_paragraph"}
            }
        }
        
        response = self.app.post('/synthesize',
                               data=json.dumps(enhanced_payload),
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'final_response' in data  # Enhanced format response
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        # Test missing data
        response = self.app.post('/synthesize/basic',
                               data=json.dumps({}),
                               content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        
        # Test malformed JSON
        response = self.app.post('/synthesize/basic',
                               data="invalid json",
                               content_type='application/json')
        
        assert response.status_code == 400

if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
