"""
Comprehensive Test Suite for Multi-Language System
=================================================

This test suite covers all aspects of the multi-language implementation:
- Language detection across 11 languages
- Multi-language query parsing  
- Translation services
- Cross-language knowledge sharing
- Uncertainty handling with Socratic dialogue
- End-to-end multi-language workflows

Author: Myriad Cognitive Architecture Team
Version: 1.0
Date: 2025-10-02
"""

import pytest
from typing import Dict, List

# Import multi-language components
from myriad.core.multilang import (
    Language,
    get_language_detector,
    get_multilang_parser,
    get_translation_service,
    get_cross_language_knowledge_manager
)

# Import uncertainty and Socratic components
from myriad.core.uncertainty.uncertainty_signals import (
    get_uncertainty_detector,
    UncertaintyType,
    UncertaintyLevel
)
from myriad.core.socratic.socratic_questioning import (
    get_socratic_dialogue_manager,
    QuestionType
)


class TestLanguageDetection:
    """Test language detection capabilities"""
    
    def setup_method(self):
        """Setup for each test"""
        self.detector = get_language_detector()
    
    def test_english_detection(self):
        """Test English language detection"""
        queries = [
            "What is the impact of the lightbulb?",
            "How did factories change society?",
            "Tell me about the Industrial Revolution"
        ]
        
        for query in queries:
            result = self.detector.detect_language(query)
            assert result.detected_language == Language.ENGLISH
            assert result.confidence > 0.8
            print(f"✓ English detected: '{query}' (confidence: {result.confidence:.2f})")
    
    def test_spanish_detection(self):
        """Test Spanish language detection"""
        queries = [
            "¿Qué es el impacto de la bombilla?",
            "¿Cómo cambiaron las fábricas la sociedad?",
            "Háblame sobre la Revolución Industrial"
        ]
        
        for query in queries:
            result = self.detector.detect_language(query)
            assert result.detected_language == Language.SPANISH
            assert result.confidence > 0.7
            print(f"✓ Spanish detected: '{query}' (confidence: {result.confidence:.2f})")
    
    def test_french_detection(self):
        """Test French language detection"""
        queries = [
            "Qu'est-ce que l'impact de l'ampoule?",
            "Comment les usines ont changé la société?",
            "Parle-moi de la Révolution Industrielle"
        ]
        
        for query in queries:
            result = self.detector.detect_language(query)
            assert result.detected_language == Language.FRENCH
            assert result.confidence > 0.7
            print(f"✓ French detected: '{query}' (confidence: {result.confidence:.2f})")
    
    def test_german_detection(self):
        """Test German language detection"""
        queries = [
            "Was ist die Auswirkung der Glühbirne?",
            "Wie haben Fabriken die Gesellschaft verändert?",
            "Erzähl mir über die Industrielle Revolution"
        ]
        
        for query in queries:
            result = self.detector.detect_language(query)
            assert result.detected_language == Language.GERMAN
            assert result.confidence > 0.7
            print(f"✓ German detected: '{query}' (confidence: {result.confidence:.2f})")
    
    def test_chinese_detection(self):
        """Test Chinese language detection"""
        queries = [
            "灯泡的影响是什么？",
            "工厂如何改变社会？",
            "告诉我关于工业革命"
        ]
        
        for query in queries:
            result = self.detector.detect_language(query)
            assert result.detected_language == Language.CHINESE
            assert result.confidence > 0.9  # Should be very confident with CJK characters
            print(f"✓ Chinese detected: '{query}' (confidence: {result.confidence:.2f})")
    
    def test_language_confidence_scoring(self):
        """Test that confidence scores are reasonable"""
        query = "What is the impact of technology?"
        result = self.detector.detect_language(query)
        
        assert 0.0 <= result.confidence <= 1.0
        assert len(result.alternatives) >= 0
        print(f"✓ Confidence scoring works: {result.confidence:.2f}")


class TestMultiLanguageParsing:
    """Test multi-language query parsing"""
    
    def setup_method(self):
        """Setup for each test"""
        self.parser = get_multilang_parser()
    
    def test_english_parsing(self):
        """Test English query parsing"""
        query = "What is the historical impact of the lightbulb on industrial factories?"
        
        metadata, parsed = self.parser.parse_query(query)
        
        assert metadata.detected_language == Language.ENGLISH
        assert parsed.language == Language.ENGLISH
        assert parsed.primary_intent in ['define', 'explain_impact', 'analyze_historical_context']
        assert len(parsed.concepts) > 0
        assert parsed.complexity_score > 0
        
        print(f"✓ English parsing successful:")
        print(f"  Intent: {parsed.primary_intent}")
        print(f"  Concepts: {parsed.concepts}")
        print(f"  Complexity: {parsed.complexity_score:.2f}")
    
    def test_spanish_parsing(self):
        """Test Spanish query parsing"""
        query = "¿Cuál es el impacto histórico de la bombilla en las fábricas industriales?"
        
        metadata, parsed = self.parser.parse_query(query)
        
        assert metadata.detected_language == Language.SPANISH
        assert parsed.language == Language.SPANISH
        assert parsed.primary_intent in ['define', 'explain_impact', 'analyze_historical_context']
        assert len(parsed.concepts) > 0
        
        print(f"✓ Spanish parsing successful:")
        print(f"  Intent: {parsed.primary_intent}")
        print(f"  Concepts: {parsed.concepts}")
    
    def test_french_parsing(self):
        """Test French query parsing"""
        query = "Quel est l'impact historique de l'ampoule sur les usines industrielles?"
        
        metadata, parsed = self.parser.parse_query(query)
        
        assert metadata.detected_language == Language.FRENCH
        assert parsed.language == Language.FRENCH
        assert parsed.primary_intent in ['define', 'explain_impact', 'analyze_historical_context']
        
        print(f"✓ French parsing successful:")
        print(f"  Intent: {parsed.primary_intent}")
    
    def test_intent_recognition_across_languages(self):
        """Test that same intent is recognized across languages"""
        queries = {
            'en': "What is a lightbulb?",
            'es': "¿Qué es una bombilla?",
            'fr': "Qu'est-ce qu'une ampoule?",
            'de': "Was ist eine Glühbirne?"
        }
        
        intents = {}
        for lang, query in queries.items():
            _, parsed = self.parser.parse_query(query)
            intents[lang] = parsed.primary_intent
        
        # All should have 'define' intent
        for lang, intent in intents.items():
            assert intent == 'define'
            print(f"✓ {lang}: Intent '{intent}' correctly identified")
    
    def test_complexity_scoring(self):
        """Test query complexity scoring"""
        simple_query = "What is a lightbulb?"
        complex_query = "How did the invention of the electric lightbulb impact industrial manufacturing processes and worker productivity in late 19th century factories?"
        
        _, simple_parsed = self.parser.parse_query(simple_query)
        _, complex_parsed = self.parser.parse_query(complex_query)
        
        assert simple_parsed.complexity_score < complex_parsed.complexity_score
        print(f"✓ Complexity scoring works:")
        print(f"  Simple: {simple_parsed.complexity_score:.2f}")
        print(f"  Complex: {complex_parsed.complexity_score:.2f}")


class TestTranslationService:
    """Test translation service"""
    
    def setup_method(self):
        """Setup for each test"""
        self.translator = get_translation_service()
    
    def test_dictionary_translation(self):
        """Test dictionary-based translation"""
        # Test translating a known concept
        result = self.translator.translate('lightbulb', Language.ENGLISH, Language.SPANISH)
        
        assert result is not None
        assert result.translated_text == 'bombilla'
        assert result.method == 'dictionary'
        assert result.confidence == 1.0
        
        print(f"✓ Dictionary translation: lightbulb -> {result.translated_text}")
    
    def test_translation_across_multiple_languages(self):
        """Test translating across multiple language pairs"""
        test_cases = [
            ('lightbulb', Language.ENGLISH, Language.FRENCH, 'ampoule'),
            ('lightbulb', Language.ENGLISH, Language.GERMAN, 'Glühbirne'),
            ('factory', Language.ENGLISH, Language.SPANISH, 'fábrica'),
            ('technology', Language.ENGLISH, Language.ITALIAN, 'tecnologia')
        ]
        
        for source_text, source_lang, target_lang, expected in test_cases:
            result = self.translator.translate(source_text, source_lang, target_lang)
            
            if result and result.method == 'dictionary':
                assert result.translated_text == expected
                print(f"✓ {source_text} ({source_lang.value}) -> {result.translated_text} ({target_lang.value})")
    
    def test_translation_caching(self):
        """Test that translations are cached"""
        # Translate the same thing twice
        result1 = self.translator.translate('lightbulb', Language.ENGLISH, Language.SPANISH)
        result2 = self.translator.translate('lightbulb', Language.ENGLISH, Language.SPANISH)
        
        # Second one should be cached
        assert result2.method == 'cached'
        
        stats = self.translator.get_statistics()
        assert stats['cache_stats']['cache_hits'] > 0
        
        print(f"✓ Translation caching works:")
        print(f"  Cache size: {stats['cache_stats']['cache_size']}")
        print(f"  Cache hits: {stats['cache_stats']['cache_hits']}")
    
    def test_same_language_translation(self):
        """Test translation where source and target are the same"""
        result = self.translator.translate('lightbulb', Language.ENGLISH, Language.ENGLISH)
        
        assert result.translated_text == 'lightbulb'
        assert result.method == 'same_language'
        
        print(f"✓ Same language translation handled correctly")
    
    def test_get_all_translations(self):
        """Test getting all translations of a concept"""
        translations = self.translator.get_all_translations('lightbulb', Language.ENGLISH)
        
        assert Language.SPANISH in translations
        assert Language.FRENCH in translations
        assert translations[Language.SPANISH] == 'bombilla'
        
        print(f"✓ All translations retrieved: {len(translations)} languages")
        for lang, term in translations.items():
            print(f"  {lang.value}: {term}")


class TestCrossLanguageKnowledge:
    """Test cross-language knowledge management"""
    
    def setup_method(self):
        """Setup for each test"""
        self.knowledge_mgr = get_cross_language_knowledge_manager()
        # Clear any existing data
        self.knowledge_mgr.concepts.clear()
        self.knowledge_mgr.language_index.clear()
    
    def test_add_concept(self):
        """Test adding a new concept"""
        concept_id = self.knowledge_mgr.add_concept(
            'lightbulb',
            Language.ENGLISH,
            definition='An electric light with a wire filament'
        )
        
        assert concept_id is not None
        assert concept_id in self.knowledge_mgr.concepts
        
        concept = self.knowledge_mgr.concepts[concept_id]
        assert concept.canonical_name == 'lightbulb'
        assert Language.ENGLISH in concept.language_variants
        
        print(f"✓ Concept added: {concept_id}")
        print(f"  Variants: {len(concept.language_variants)} languages")
    
    def test_auto_translation(self):
        """Test automatic translation of concepts"""
        concept_id = self.knowledge_mgr.add_concept(
            'factory',
            Language.ENGLISH,
            definition='A building where goods are manufactured'
        )
        
        concept = self.knowledge_mgr.concepts[concept_id]
        
        # Should have multiple language variants
        assert len(concept.language_variants) > 1
        assert Language.SPANISH in concept.language_variants
        assert concept.language_variants[Language.SPANISH] == 'fábrica'
        
        print(f"✓ Auto-translation created {len(concept.language_variants)} variants")
    
    def test_get_concept_in_language(self):
        """Test retrieving concept in different language"""
        concept_id = self.knowledge_mgr.add_concept(
            'technology',
            Language.ENGLISH
        )
        
        spanish_term = self.knowledge_mgr.get_concept_in_language(
            concept_id, Language.SPANISH
        )
        french_term = self.knowledge_mgr.get_concept_in_language(
            concept_id, Language.FRENCH
        )
        
        assert spanish_term == 'tecnología'
        assert french_term == 'technologie'
        
        print(f"✓ Concept retrieved in multiple languages:")
        print(f"  Spanish: {spanish_term}")
        print(f"  French: {french_term}")
    
    def test_cross_language_search(self):
        """Test searching across languages"""
        # Add a concept in English
        concept_id = self.knowledge_mgr.add_concept(
            'electricity',
            Language.ENGLISH,
            definition='Flow of electric charge'
        )
        
        # Search using Spanish term
        results = self.knowledge_mgr.cross_language_search(
            'electricidad',
            Language.SPANISH
        )
        
        assert len(results) > 0
        assert results[0].concept_id == concept_id
        
        print(f"✓ Cross-language search successful")
        print(f"  Found {len(results)} results")
    
    def test_knowledge_sharing(self):
        """Test sharing knowledge across languages"""
        concept_id = self.knowledge_mgr.add_concept(
            'invention',
            Language.ENGLISH,
            definition='A new device or process'
        )
        
        # Share from English to Spanish
        success = self.knowledge_mgr.share_knowledge_across_languages(
            concept_id,
            Language.ENGLISH,
            Language.SPANISH
        )
        
        assert success
        
        concept = self.knowledge_mgr.concepts[concept_id]
        assert Language.SPANISH in concept.definitions
        
        print(f"✓ Knowledge shared across languages")
    
    def test_ensure_multilingual_coverage(self):
        """Test ensuring concept exists in all languages"""
        concept_id = self.knowledge_mgr.add_concept(
            'revolution',
            Language.ENGLISH
        )
        
        coverage = self.knowledge_mgr.ensure_multilingual_coverage(concept_id)
        
        assert len(coverage) >= 5  # At least 5 languages
        assert Language.ENGLISH in coverage
        assert Language.SPANISH in coverage
        
        print(f"✓ Multilingual coverage ensured: {len(coverage)} languages")
        for lang, term in coverage.items():
            print(f"  {lang.value}: {term}")


class TestUncertaintyIntegration:
    """Test uncertainty detection and handling"""
    
    def setup_method(self):
        """Setup for each test"""
        self.uncertainty_detector = get_uncertainty_detector()
    
    def test_knowledge_gap_detection(self):
        """Test detecting knowledge gaps"""
        query_data = {
            'query': 'What is quantum entanglement?',
            'concepts': ['quantum entanglement'],
            'confidence': 0.2,
            'ambiguity': False
        }
        
        assessment = self.uncertainty_detector.assess_uncertainty(
            query_data,
            'TestAgent'
        )
        
        assert assessment.uncertainty_level in [UncertaintyLevel.MEDIUM, UncertaintyLevel.HIGH]
        print(f"✓ Knowledge gap detected:")
        print(f"  Type: {assessment.primary_uncertainty_type.value}")
        print(f"  Level: {assessment.uncertainty_level.value}")
    
    def test_ambiguous_query_detection(self):
        """Test detecting ambiguous queries"""
        query_data = {
            'query': 'What about banks?',  # Could be financial or river banks
            'concepts': ['banks'],
            'confidence': 0.6,
            'ambiguity': True
        }
        
        assessment = self.uncertainty_detector.assess_uncertainty(
            query_data,
            'TestAgent'
        )
        
        assert assessment.primary_uncertainty_type == UncertaintyType.AMBIGUOUS_TERMS
        print(f"✓ Ambiguity detected: {assessment.description}")


class TestSocraticDialogue:
    """Test Socratic questioning system"""
    
    def setup_method(self):
        """Setup for each test"""
        self.dialogue_mgr = get_socratic_dialogue_manager()
    
    def test_dialogue_initiation(self):
        """Test initiating a Socratic dialogue"""
        from myriad.core.uncertainty.uncertainty_signals import UncertaintyAssessment
        
        assessment = UncertaintyAssessment(
            agent_id='TestAgent',
            primary_uncertainty_type=UncertaintyType.KNOWLEDGE_GAP,
            uncertainty_level=UncertaintyLevel.HIGH,
            uncertainty_score=0.8,
            affected_concepts=['quantum physics'],
            description='Insufficient knowledge about quantum physics',
            suggested_actions=['Request clarification'],
            context={}
        )
        
        session = self.dialogue_mgr.initiate_dialogue(
            'What is quantum physics?',
            assessment,
            language='en'
        )
        
        assert session is not None
        assert len(session.questions_asked) > 0
        assert session.current_state.value == 'questioning'
        
        print(f"✓ Dialogue initiated:")
        print(f"  Session ID: {session.session_id}")
        print(f"  Questions: {len(session.questions_asked)}")
        for q in session.questions_asked:
            print(f"    - {q.question_text}")
    
    def test_multilanguage_questions(self):
        """Test generating questions in different languages"""
        from myriad.core.uncertainty.uncertainty_signals import UncertaintyAssessment
        
        assessment = UncertaintyAssessment(
            agent_id='TestAgent',
            primary_uncertainty_type=UncertaintyType.AMBIGUOUS_TERMS,
            uncertainty_level=UncertaintyLevel.MEDIUM,
            uncertainty_score=0.6,
            affected_concepts=['bank'],
            description='Ambiguous term: bank',
            suggested_actions=['Clarify meaning'],
            context={'meanings': ['financial institution', 'river bank']}
        )
        
        # Test in different languages
        for lang in ['en', 'es', 'fr']:
            session = self.dialogue_mgr.initiate_dialogue(
                'Tell me about banks',
                assessment,
                language=lang
            )
            
            assert len(session.questions_asked) > 0
            print(f"✓ Questions generated in {lang}:")
            for q in session.questions_asked[:1]:  # Show first question
                print(f"  {q.question_text}")


class TestEndToEndWorkflow:
    """Test end-to-end multi-language workflows"""
    
    def test_complete_multilanguage_pipeline(self):
        """Test complete pipeline from query to response"""
        parser = get_multilang_parser()
        knowledge_mgr = get_cross_language_knowledge_manager()
        
        # Add some concepts
        knowledge_mgr.add_concept('lightbulb', Language.ENGLISH,
                                 definition='Electric light source')
        
        # Process queries in different languages
        queries = {
            'en': "What is a lightbulb?",
            'es': "¿Qué es una bombilla?",
            'fr': "Qu'est-ce qu'une ampoule?"
        }
        
        for lang, query in queries.items():
            metadata, parsed = parser.parse_query(query)
            
            assert parsed.primary_intent == 'define'
            print(f"✓ {lang}: Processed successfully")
            print(f"  Language: {metadata.detected_language.value}")
            print(f"  Intent: {parsed.primary_intent}")
    
    def test_uncertainty_to_clarification_workflow(self):
        """Test workflow from uncertainty detection to clarification"""
        from myriad.core.uncertainty.uncertainty_signals import UncertaintyAssessment
        
        detector = get_uncertainty_detector()
        dialogue_mgr = get_socratic_dialogue_manager()
        
        # Detect uncertainty
        query_data = {
            'query': 'What is X?',
            'concepts': ['X'],
            'confidence': 0.2,
            'ambiguity': False
        }
        
        assessment = detector.assess_uncertainty(query_data, 'TestAgent')
        
        # Generate clarification questions
        session = dialogue_mgr.initiate_dialogue(
            query_data['query'],
            assessment,
            language='en'
        )
        
        assert session is not None
        assert len(session.questions_asked) > 0
        
        print(f"✓ Uncertainty to clarification workflow complete")
        print(f"  Uncertainty level: {assessment.uncertainty_level.value}")
        print(f"  Questions generated: {len(session.questions_asked)}")


def run_all_tests():
    """Run all tests with detailed output"""
    print("\n" + "="*70)
    print("MYRIAD MULTI-LANGUAGE SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*70 + "\n")
    
    test_classes = [
        TestLanguageDetection,
        TestMultiLanguageParsing,
        TestTranslationService,
        TestCrossLanguageKnowledge,
        TestUncertaintyIntegration,
        TestSocraticDialogue,
        TestEndToEndWorkflow
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for test_class in test_classes:
        print(f"\n{'='*70}")
        print(f"Running: {test_class.__name__}")
        print(f"{'='*70}\n")
        
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith('test_')]
        
        for test_method_name in test_methods:
            total_tests += 1
            try:
                # Run setup
                if hasattr(test_instance, 'setup_method'):
                    test_instance.setup_method()
                
                # Run test
                test_method = getattr(test_instance, test_method_name)
                test_method()
                
                passed_tests += 1
                print()
            except AssertionError as e:
                print(f"✗ FAILED: {test_method_name}")
                print(f"  Error: {e}\n")
            except Exception as e:
                print(f"✗ ERROR: {test_method_name}")
                print(f"  Exception: {e}\n")
    
    print(f"\n{'='*70}")
    print(f"TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    run_all_tests()
