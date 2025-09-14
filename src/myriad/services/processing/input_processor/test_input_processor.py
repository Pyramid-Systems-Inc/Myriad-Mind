"""
Comprehensive Unit Tests for Enhanced Input Processor
Implements Task 3.1.7: Write Comprehensive Unit Tests

Tests all components: Parser, Intent Recognizer, Ambiguity Resolver, and main processor
"""

import pytest
import json
from unittest.mock import Mock, patch

from .parser import AdvancedParser
from .intent_recognizer import IntentRecognizer, IntentType
from .ambiguity_resolver import AmbiguityResolver, AmbiguityType
from .input_processor import EnhancedInputProcessor
from .app import app

class TestAdvancedParser:
    """Test cases for the Advanced Parser component"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.parser = AdvancedParser()
    
    def test_parse_simple_definition_query(self):
        """Test parsing a simple definition query"""
        query = "What is a lightbulb?"
        query_metadata, parsed_query = self.parser.parse_query(query)
        
        assert query_metadata.original_query == query
        assert parsed_query.primary_intent == "define"
        assert "lightbulb" in parsed_query.concepts
        assert parsed_query.complexity_score > 0
        assert parsed_query.estimated_agents_needed >= 1
    
    def test_parse_complex_historical_query(self):
        """Test parsing a complex historical query"""
        query = "Why was the lightbulb important for factories during the industrial revolution?"
        query_metadata, parsed_query = self.parser.parse_query(query)
        
        assert parsed_query.primary_intent in ["explain_impact", "analyze_historical_context"]
        assert "lightbulb" in parsed_query.concepts
        assert "factories" in parsed_query.concepts or "factory" in parsed_query.concepts
        assert len(parsed_query.relationships) > 0
        assert parsed_query.complexity_score > 0.5
        assert parsed_query.estimated_agents_needed > 1
    
    def test_extract_concepts(self):
        """Test concept extraction"""
        query = "Compare LED lighting with traditional incandescent bulbs"
        concepts = self.parser._extract_concepts(query)
        
        assert len(concepts) > 0
        # Should extract relevant concepts while filtering stopwords
        assert not any(word in concepts for word in ['the', 'and', 'with'])
    
    def test_calculate_complexity_score(self):
        """Test complexity score calculation"""
        simple_query = "What is light?"
        complex_query = "Analyze the historical impact of electric lighting on industrial productivity during the late 19th century manufacturing revolution"
        
        _, simple_parsed = self.parser.parse_query(simple_query)
        _, complex_parsed = self.parser.parse_query(complex_query)
        
        assert complex_parsed.complexity_score > simple_parsed.complexity_score

class TestIntentRecognizer:
    """Test cases for the Intent Recognizer component"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.recognizer = IntentRecognizer()
    
    def test_recognize_define_intent(self):
        """Test recognition of define intent"""
        queries = [
            "What is a lightbulb?",
            "Define electricity",
            "Tell me about factories"
        ]
        
        for query in queries:
            result = self.recognizer.recognize_intent(query)
            assert result.primary_intent == IntentType.DEFINE.value
            assert result.confidence > 0.5
    
    def test_recognize_historical_context_intent(self):
        """Test recognition of historical context intent"""
        queries = [
            "When did the lightbulb develop?",
            "What is the history of factories?",
            "How did electricity evolve?"
        ]
        
        for query in queries:
            result = self.recognizer.recognize_intent(query)
            assert result.primary_intent == IntentType.ANALYZE_HISTORICAL_CONTEXT.value
    
    def test_recognize_compare_intent(self):
        """Test recognition of compare intent"""
        queries = [
            "Compare LED vs incandescent bulbs",
            "What's the difference between factories and workshops?",
            "LED versus traditional lighting"
        ]
        
        for query in queries:
            result = self.recognizer.recognize_intent(query)
            assert result.primary_intent == IntentType.COMPARE.value
    
    def test_ambiguous_intent_detection(self):
        """Test detection of ambiguous intents"""
        ambiguous_query = "Tell me about lightbulbs"  # Could be define or historical
        result = self.recognizer.recognize_intent(ambiguous_query)
        
        # Should have alternative intents
        assert len(result.alternative_intents) > 0
    
    def test_context_aware_detection(self):
        """Test context-aware intent detection"""
        query = "lightbulb factories"
        context = {"previous_queries": ["What is the history of manufacturing?"]}
        
        result = self.recognizer.recognize_intent(query, context)
        # Context should influence intent detection
        assert result.context_factors is not None

class TestAmbiguityResolver:
    """Test cases for the Ambiguity Resolver component"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.resolver = AmbiguityResolver()
    
    def test_detect_concept_ambiguity(self):
        """Test detection of ambiguous concepts"""
        query = "What is a drive?"  # Ambiguous: computer drive vs driving
        concepts = ["drive"]
        mock_intent_result = Mock()
        mock_intent_result.is_ambiguous = False
        
        detection = self.resolver.detect_ambiguity(query, concepts, mock_intent_result)
        
        assert detection.is_ambiguous
        assert detection.ambiguity_type == AmbiguityType.CONCEPT_AMBIGUITY
        assert "drive" in detection.ambiguous_elements
        assert len(detection.suggested_clarifications) > 0
    
    def test_detect_intent_ambiguity(self):
        """Test detection of intent ambiguity"""
        query = "Tell me about lightbulbs"
        concepts = ["lightbulbs"]
        mock_intent_result = Mock()
        mock_intent_result.is_ambiguous = True
        mock_intent_result.primary_intent = "define"
        mock_intent_result.alternative_intents = [("analyze_historical_context", 0.7)]
        
        detection = self.resolver.detect_ambiguity(query, concepts, mock_intent_result)
        
        assert detection.is_ambiguous
        assert len(detection.suggested_clarifications) > 0
    
    def test_resolve_with_context(self):
        """Test ambiguity resolution using context"""
        query = "What is a bank?"
        detection = Mock()
        detection.is_ambiguous = True
        detection.ambiguous_elements = ["bank"]
        
        # Context suggesting financial meaning
        context = {"previous_queries": ["How do loans work?"]}
        
        result = self.resolver.resolve_ambiguity(query, detection, context)
        
        # Should attempt resolution (may or may not succeed depending on implementation)
        assert result is not None
    
    def test_fallback_resolution(self):
        """Test fallback resolution for unresolved ambiguity"""
        query = "What is a bank?"
        detection = Mock()
        detection.is_ambiguous = True
        detection.ambiguous_elements = ["bank"]
        
        result = self.resolver.resolve_ambiguity(query, detection, None)
        
        assert result is not None
        assert result.fallback_interpretation is not None

class TestEnhancedInputProcessor:
    """Test cases for the main Enhanced Input Processor"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.processor = EnhancedInputProcessor()
    
    def test_process_simple_query(self):
        """Test processing a simple query"""
        query = "What is a lightbulb?"
        
        result = self.processor.process_query(query)
        
        assert result.protocol_version == "1.0"
        assert result.query_metadata is not None
        assert result.parsed_query is not None
        assert len(result.task_list) > 0
        assert result.processing_metadata is not None
    
    def test_process_complex_query(self):
        """Test processing a complex query with multiple concepts"""
        query = "Why was the lightbulb important for factories during industrialization?"
        
        result = self.processor.process_query(query)
        
        # Should generate multiple tasks
        assert len(result.task_list) > 1
        
        # Should have tasks with dependencies
        task_with_deps = next((task for task in result.task_list if task['dependencies']), None)
        assert task_with_deps is not None
    
    def test_generate_task_list(self):
        """Test task list generation"""
        # Mock parsed query
        from .parser import ParsedQuery
        parsed_query = ParsedQuery(
            primary_intent="explain_impact",
            concepts=["lightbulb", "factory"],
            relationships=[{"type": "causal", "subject": "lightbulb", "object": "factory"}],
            complexity_score=0.7,
            estimated_agents_needed=3
        )
        
        # Mock intent result
        from .intent_recognizer import IntentResult
        intent_result = IntentResult(
            primary_intent="explain_impact",
            confidence=0.9,
            alternative_intents=[],
            is_ambiguous=False,
            context_factors={}
        )
        
        tasks = self.processor._generate_task_list(parsed_query, intent_result, None, None)
        
        assert len(tasks) > 0
        # Should have tasks for each concept
        concept_tasks = [task for task in tasks if task.concept in ["lightbulb", "factory"]]
        assert len(concept_tasks) >= 2
    
    def test_to_orchestrator_protocol(self):
        """Test conversion to orchestrator protocol format"""
        query = "What is a lightbulb?"
        enhanced_result = self.processor.process_query(query)
        
        basic_protocol = self.processor.to_orchestrator_protocol(enhanced_result)
        
        assert "query_id" in basic_protocol
        assert "tasks" in basic_protocol
        assert len(basic_protocol["tasks"]) > 0
        
        # Check task format
        task = basic_protocol["tasks"][0]
        assert "task_id" in task
        assert "intent" in task
        assert "concept" in task
        assert "args" in task

class TestInputProcessorFlaskApp:
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
    
    def test_process_endpoint(self):
        """Test main process endpoint"""
        payload = {
            "query": "What is a lightbulb?",
            "user_context": {"session_id": "test_session"}
        }
        
        response = self.app.post('/process', 
                               data=json.dumps(payload),
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'enhanced_task_list' in data
    
    def test_process_basic_endpoint(self):
        """Test basic compatibility endpoint"""
        payload = {
            "query": "What is a lightbulb?"
        }
        
        response = self.app.post('/process/basic',
                               data=json.dumps(payload),
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'task_list' in data
        
        # Should be in basic orchestrator format
        task_list = data['task_list']
        assert 'query_id' in task_list
        assert 'tasks' in task_list
    
    def test_analyze_endpoint(self):
        """Test query analysis endpoint"""
        payload = {
            "query": "Why was the lightbulb important for factories?"
        }
        
        response = self.app.post('/analyze',
                               data=json.dumps(payload),
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'analysis' in data
        
        analysis = data['analysis']
        assert 'parsed_query' in analysis
        assert 'intent_analysis' in analysis
        assert 'ambiguity_analysis' in analysis
    
    def test_invalid_request(self):
        """Test handling of invalid requests"""
        # Missing query
        response = self.app.post('/process',
                               data=json.dumps({}),
                               content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'MISSING_QUERY' in data['error_code']
    
    def test_malformed_json(self):
        """Test handling of malformed JSON"""
        response = self.app.post('/process',
                               data="invalid json",
                               content_type='application/json')
        
        assert response.status_code == 400

if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
