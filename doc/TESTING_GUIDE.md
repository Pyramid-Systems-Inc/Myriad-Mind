# Multi-Language System Testing Guide
**Complete Testing Instructions for Option 4**

**Date**: October 2, 2025  
**Version**: 1.0  
**Status**: Ready for Testing

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Test Environment Setup](#test-environment-setup)
4. [Running Tests](#running-tests)
5. [Manual Testing Procedures](#manual-testing-procedures)
6. [Performance Testing](#performance-testing)
7. [Integration Testing](#integration-testing)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides comprehensive instructions for testing all implemented features:

✅ **Option 1**: Multi-language parsers (8 languages)  
✅ **Option 2**: Uncertainty integration with output processor  
✅ **Option 3**: Translation service and cross-language knowledge  

### What We're Testing

- Language detection accuracy (11 languages)
- Multi-language query parsing
- Intent recognition across languages
- Translation services
- Cross-language knowledge sharing
- Uncertainty detection and signaling
- Socratic dialogue generation
- End-to-end multi-language workflows

---

## Prerequisites

### Required Dependencies

Ensure all dependencies are installed:

```bash
cd "d:\My Dev Life\AI Development\Myriad-Mind"
pip install -r requirements.txt
```

### Current Dependencies

```
flask
requests
pytest
spacy
nltk
docker
neo4j
```

### Optional (for full testing)

For more comprehensive language testing:

```bash
# For better language detection
pip install langdetect

# For Chinese text processing
pip install jieba

# For testing frameworks
pip install pytest-cov pytest-benchmark
```

---

## Test Environment Setup

### 1. Verify Project Structure

Ensure all new files are in place:

```bash
cd "d:\My Dev Life\AI Development\Myriad-Mind"

# Check multi-language module
dir src\myriad\core\multilang

# Should show:
# - __init__.py
# - language_detector.py
# - multilang_parser.py
# - translation_service.py
# - cross_language_knowledge.py
```

### 2. Verify Imports

Test that modules can be imported:

```bash
python -c "from myriad.core.multilang import Language, get_language_detector, get_multilang_parser; print('Imports successful!')"
```

### 3. Check Python Environment

```bash
python --version  # Should be Python 3.7+
```

---

## Running Tests

### Automated Test Suite

#### Run All Tests

```bash
cd "d:\My Dev Life\AI Development\Myriad-Mind"

# Run the comprehensive test suite
python tests\test_multilanguage_system.py
```

**Expected Output:**
```
======================================================================
MYRIAD MULTI-LANGUAGE SYSTEM - COMPREHENSIVE TEST SUITE
======================================================================

======================================================================
Running: TestLanguageDetection
======================================================================

✓ English detected: 'What is the impact of the lightbulb?' (confidence: 0.95)
✓ Spanish detected: '¿Qué es el impacto de la bombilla?' (confidence: 0.89)
...

======================================================================
TEST SUMMARY
======================================================================
Total Tests: 25+
Passed: 25+
Failed: 0
Success Rate: 100.0%
```

#### Run with Pytest

For more detailed output:

```bash
pytest tests\test_multilanguage_system.py -v
```

With coverage report:

```bash
pytest tests\test_multilanguage_system.py --cov=src/myriad/core/multilang --cov-report=html
```

---

## Manual Testing Procedures

### Test 1: Language Detection

**Purpose**: Verify accurate language detection across all supported languages

**Steps**:

1. Open Python interpreter:
```bash
python
```

2. Test language detection:
```python
from myriad.core.multilang import get_language_detector, Language

detector = get_language_detector()

# Test English
result = detector.detect_language("What is the impact of technology?")
print(f"Language: {result.detected_language.value}")
print(f"Confidence: {result.confidence:.2f}")

# Test Spanish
result = detector.detect_language("¿Qué es el impacto de la tecnología?")
print(f"Language: {result.detected_language.value}")
print(f"Confidence: {result.confidence:.2f}")

# Test French
result = detector.detect_language("Quel est l'impact de la technologie?")
print(f"Language: {result.detected_language.value}")
print(f"Confidence: {result.confidence:.2f}")

# Test German
result = detector.detect_language("Was ist die Auswirkung der Technologie?")
print(f"Language: {result.detected_language.value}")
print(f"Confidence: {result.confidence:.2f}")

# Test Chinese
result = detector.detect_language("技术的影响是什么？")
print(f"Language: {result.detected_language.value}")
print(f"Confidence: {result.confidence:.2f}")
```

**Expected Results**:
- Each query should be detected with >70% confidence
- Chinese should have >90% confidence (due to unique character set)
- No false positives

---

### Test 2: Multi-Language Query Parsing

**Purpose**: Verify query parsing works in all languages

**Steps**:

```python
from myriad.core.multilang import get_multilang_parser

parser = get_multilang_parser()

# Test different languages with same intent
queries = [
    ("What is a lightbulb?", "en"),
    ("¿Qué es una bombilla?", "es"),
    ("Qu'est-ce qu'une ampoule?", "fr"),
    ("Was ist eine Glühbirne?", "de"),
    ("灯泡是什么？", "zh")
]

for query, expected_lang in queries:
    metadata, parsed = parser.parse_query(query)
    
    print(f"\nQuery: {query}")
    print(f"  Detected Language: {metadata.detected_language.value}")
    print(f"  Primary Intent: {parsed.primary_intent}")
    print(f"  Concepts: {parsed.concepts}")
    print(f"  Complexity: {parsed.complexity_score:.2f}")
    print(f"  Estimated Agents: {parsed.estimated_agents_needed}")
    
    # Verify
    assert metadata.detected_language.value == expected_lang
    assert parsed.primary_intent == 'define'
    print("  ✓ PASSED")
```

**Expected Results**:
- All queries should be detected in correct language
- All should have 'define' intent
- Concepts should be extracted appropriately

---

### Test 3: Translation Service

**Purpose**: Verify translation works across language pairs

**Steps**:

```python
from myriad.core.multilang import get_translation_service, Language

translator = get_translation_service()

# Test common concepts
concepts = ['lightbulb', 'factory', 'technology', 'electricity']
target_languages = [
    Language.SPANISH, Language.FRENCH, Language.GERMAN,
    Language.PORTUGUESE, Language.ITALIAN
]

for concept in concepts:
    print(f"\nTranslating '{concept}':")
    
    for target_lang in target_languages:
        result = translator.translate(concept, Language.ENGLISH, target_lang)
        
        if result:
            print(f"  {target_lang.value}: {result.translated_text} "
                  f"(method: {result.method}, confidence: {result.confidence:.2f})")
        else:
            print(f"  {target_lang.value}: Translation failed")

# Check statistics
stats = translator.get_statistics()
print(f"\nTranslation Statistics:")
print(f"  Total attempts: {stats['total_attempts']}")
print(f"  Successful: {stats['successful_translations']}")
print(f"  Success rate: {stats['success_rate']:.1%}")
print(f"  Cache hits: {stats['cache_stats']['cache_hits']}")
print(f"  Cache size: {stats['cache_stats']['cache_size']}")
```

**Expected Results**:
- Dictionary translations should return confidence 1.0
- Cached translations should be faster
- Success rate should be >80%

---

### Test 4: Cross-Language Knowledge Management

**Purpose**: Verify knowledge can be shared across languages

**Steps**:

```python
from myriad.core.multilang import get_cross_language_knowledge_manager, Language

knowledge_mgr = get_cross_language_knowledge_manager()

# Add a concept in English
concept_id = knowledge_mgr.add_concept(
    'lightbulb',
    Language.ENGLISH,
    definition='An electric light with a wire filament'
)

print(f"Concept added: {concept_id}")

# Check auto-translations
concept = knowledge_mgr.concepts[concept_id]
print(f"\nAuto-generated translations:")
for lang, term in concept.language_variants.items():
    print(f"  {lang.value}: {term}")

# Retrieve in different languages
print(f"\nRetrieving concept in different languages:")
for lang in [Language.SPANISH, Language.FRENCH, Language.GERMAN]:
    term = knowledge_mgr.get_concept_in_language(concept_id, lang)
    print(f"  {lang.value}: {term}")

# Cross-language search
print(f"\nCross-language search for 'bombilla' (Spanish):")
results = knowledge_mgr.cross_language_search('bombilla', Language.SPANISH)
print(f"  Found {len(results)} results")
for result in results:
    print(f"  - {result.canonical_name} ({result.concept_id})")

# Statistics
stats = knowledge_mgr.get_statistics()
print(f"\nKnowledge Base Statistics:")
print(f"  Total concepts: {stats['total_concepts']}")
print(f"  Total translations: {stats['total_translations']}")
print(f"  Avg translations/concept: {stats['avg_translations_per_concept']:.1f}")
```

**Expected Results**:
- Concept should have translations in 5+ languages
- Cross-language search should find the concept
- Statistics should show multiple translations per concept

---

### Test 5: Uncertainty Detection and Socratic Dialogue

**Purpose**: Verify uncertainty triggers clarification questions

**Steps**:

```python
from myriad.core.uncertainty.uncertainty_signals import (
    get_uncertainty_detector, UncertaintyType, UncertaintyLevel, UncertaintyAssessment
)
from myriad.core.socratic.socratic_questioning import get_socratic_dialogue_manager

# Test uncertainty detection
detector = get_uncertainty_detector()

query_data = {
    'query': 'What is quantum entanglement?',
    'concepts': ['quantum entanglement'],
    'confidence': 0.2,
    'ambiguity': False
}

assessment = detector.assess_uncertainty(query_data, 'TestAgent')

print(f"Uncertainty Assessment:")
print(f"  Type: {assessment.primary_uncertainty_type.value}")
print(f"  Level: {assessment.uncertainty_level.value}")
print(f"  Score: {assessment.uncertainty_score:.2f}")
print(f"  Description: {assessment.description}")

# Test Socratic dialogue in multiple languages
dialogue_mgr = get_socratic_dialogue_manager()

for lang in ['en', 'es', 'fr']:
    print(f"\n{'='*60}")
    print(f"Generating clarification questions in {lang}:")
    print(f"{'='*60}")
    
    session = dialogue_mgr.initiate_dialogue(
        query_data['query'],
        assessment,
        language=lang
    )
    
    print(f"Session ID: {session.session_id}")
    print(f"Questions ({len(session.questions_asked)}):")
    
    for i, question in enumerate(session.questions_asked, 1):
        print(f"  {i}. {question.question_text}")
        print(f"     Type: {question.question_type.value}")
        print(f"     Priority: {question.priority}")
```

**Expected Results**:
- Uncertainty should be detected when confidence is low
- Questions should be generated in correct language
- Questions should be relevant to the uncertainty type

---

### Test 6: Output Processor Integration

**Purpose**: Verify output processor handles clarification requests

**Steps**:

```python
from myriad.services.processing.output_processor.output_processor import EnhancedOutputProcessor

processor = EnhancedOutputProcessor()

# Create a low-confidence scenario
collected_results = {
    'query_id': 'test_query_001',
    'collected_results': {
        'agent_1': {
            'confidence': 0.2,
            'data': 'Limited information available'
        }
    }
}

# Add uncertainty metadata
collected_results['query_metadata'] = {
    'original_query': 'What is quantum physics?',
    'clarification_needed': True,
    'language_info': {
        'detected_language': 'en'
    },
    'uncertainty_info': {
        'primary_uncertainty_type': 'knowledge_gap',
        'uncertainty_level': 'high',
        'uncertainty_score': 0.8,
        'affected_concepts': ['quantum physics']
    }
}

# Process
response = processor.process_collected_results(collected_results)

print(f"Response Status: {response.status}")
print(f"Requires Clarification: {response.requires_clarification}")
print(f"\n{response.final_content}")

if response.clarification_questions:
    print(f"\nClarification Questions:")
    for q in response.clarification_questions:
        print(f"  {q['question_number']}. {q['question_text']}")
```

**Expected Results**:
- Status should be 'needs_clarification'
- Clarification questions should be formatted properly
- Questions should be in appropriate language

---

## Performance Testing

### Test 7: Language Detection Speed

**Purpose**: Measure performance of language detection

**Steps**:

```python
import time
from myriad.core.multilang import get_language_detector

detector = get_language_detector()

test_queries = [
    "What is the impact of technology?",
    "¿Qué es el impacto de la tecnología?",
    "Quel est l'impact de la technologie?",
    "Was ist die Auswirkung der Technologie?",
    "技术的影响是什么？"
] * 20  # 100 queries total

start_time = time.time()

for query in test_queries:
    result = detector.detect_language(query)

end_time = time.time()

total_time = end_time - start_time
avg_time = total_time / len(test_queries)

print(f"Performance Test Results:")
print(f"  Total queries: {len(test_queries)}")
print(f"  Total time: {total_time:.3f}s")
print(f"  Average time per query: {avg_time*1000:.2f}ms")
print(f"  Queries per second: {len(test_queries)/total_time:.1f}")
```

**Target Performance**:
- < 10ms per query for language detection
- > 100 queries/second

---

### Test 8: Translation Cache Effectiveness

**Purpose**: Measure cache hit rates and performance improvement

**Steps**:

```python
import time
from myriad.core.multilang import get_translation_service, Language

translator = get_translation_service()

# Clear cache
translator.cached_api_provider.clear_cache()

concepts = ['lightbulb', 'factory', 'technology', 'electricity', 'history']

# First pass (cold cache)
start_time = time.time()
for concept in concepts * 5:
    translator.translate(concept, Language.ENGLISH, Language.SPANISH)
cold_time = time.time() - start_time

# Second pass (warm cache)
start_time = time.time()
for concept in concepts * 5:
    translator.translate(concept, Language.ENGLISH, Language.SPANISH)
warm_time = time.time() - start_time

stats = translator.get_statistics()

print(f"Cache Performance:")
print(f"  Cold cache time: {cold_time:.3f}s")
print(f"  Warm cache time: {warm_time:.3f}s")
print(f"  Speedup: {cold_time/warm_time:.1f}x")
print(f"  Hit rate: {stats['cache_stats']['hit_rate']:.1%}")
```

**Target Performance**:
- Cache should provide >2x speedup
- Hit rate should be >70% for repeated queries

---

## Integration Testing

### Test 9: End-to-End Multi-Language Workflow

**Purpose**: Test complete pipeline from query to response

**Steps**:

1. Start all services (if using Docker):
```bash
docker-compose up -d
```

2. Test the full pipeline:
```python
from myriad.services.processing.input_processor.input_processor import InputProcessor
from myriad.services.processing.output_processor.output_processor import EnhancedOutputProcessor

# Initialize processors
input_processor = InputProcessor()
output_processor = EnhancedOutputProcessor()

# Test in multiple languages
test_queries = [
    ("What is the historical impact of the lightbulb?", "en"),
    ("¿Cuál es el impacto histórico de la bombilla?", "es"),
    ("Quel est l'impact historique de l'ampoule?", "fr")
]

for query, expected_lang in test_queries:
    print(f"\n{'='*70}")
    print(f"Testing: {query}")
    print(f"{'='*70}")
    
    # Process input
    task_list = input_processor.process_query(query)
    
    print(f"✓ Input processed:")
    print(f"  Language: {task_list.language_info['detected_language']}")
    print(f"  Tasks: {len(task_list.task_list)}")
    print(f"  Requires clarification: {task_list.clarification_needed}")
    
    # If clarification needed, show questions
    if task_list.clarification_needed:
        print(f"\nClarification needed!")
        # Would normally send to output processor for formatting
    else:
        print(f"\nReady for orchestration")
```

**Expected Results**:
- Queries in all languages should be processed
- Language should be detected correctly
- Task lists should be generated appropriately
- Uncertainty should trigger clarification when needed

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Import Errors

**Problem**: `ModuleNotFoundError: No module named 'myriad'`

**Solution**:
```bash
# Add project to Python path
cd "d:\My Dev Life\AI Development\Myriad-Mind"
$env:PYTHONPATH = "d:\My Dev Life\AI Development\Myriad-Mind\src;$env:PYTHONPATH"
```

Or in Python:
```python
import sys
sys.path.insert(0, r'd:\My Dev Life\AI Development\Myriad-Mind\src')
```

#### Issue: Language Detection Fails

**Problem**: All queries detected as UNKNOWN

**Solution**:
- Check that text is not empty
- Verify language is in supported list
- Try with more text (single words may not be enough)

#### Issue: Translation Returns None

**Problem**: `translator.translate()` returns None

**Solution**:
- Check if concept is in dictionary
- Verify source and target languages are valid
- API provider may not be configured (uses mock by default)

#### Issue: Low Test Coverage

**Problem**: Not all languages being tested

**Solution**:
Run the comprehensive test suite:
```bash
python tests\test_multilanguage_system.py
```

---

## Test Checklist

Use this checklist to ensure complete testing:

### Language Detection
- [ ] English queries detected correctly
- [ ] Spanish queries detected correctly
- [ ] French queries detected correctly
- [ ] German queries detected correctly
- [ ] Chinese queries detected correctly
- [ ] Portuguese queries detected correctly
- [ ] Italian queries detected correctly
- [ ] Russian queries detected correctly
- [ ] Confidence scores are reasonable (>0.7)
- [ ] Character set detection works for CJK/Cyrillic/Arabic

### Multi-Language Parsing
- [ ] English parser extracts intents correctly
- [ ] Spanish parser extracts intents correctly
- [ ] French parser extracts intents correctly
- [ ] German parser extracts intents correctly
- [ ] Chinese parser extracts intents correctly
- [ ] Concepts extracted appropriately in each language
- [ ] Complexity scoring works across languages
- [ ] Agent estimation reasonable

### Translation Service
- [ ] Dictionary translations work
- [ ] Caching mechanism works
- [ ] Cache hit rate is good (>70%)
- [ ] Batch translation works
- [ ] Same-language translation handled
- [ ] Statistics tracking works

### Cross-Language Knowledge
- [ ] Concepts can be added
- [ ] Auto-translation generates variants
- [ ] Concepts can be retrieved in different languages
- [ ] Cross-language search works
- [ ] Knowledge sharing works
- [ ] Multilingual coverage ensured
- [ ] Export/import functionality works

### Uncertainty & Socratic Dialogue
- [ ] Uncertainty detection works
- [ ] Appropriate uncertainty levels assigned
- [ ] Socratic questions generated
- [ ] Questions in multiple languages
- [ ] Dialogue sessions tracked
- [ ] Different question types generated

### Output Processor Integration
- [ ] Clarification requests handled
- [ ] Questions formatted properly
- [ ] Multi-language messages generated
- [ ] Low confidence detected and handled
- [ ] Response structure correct

### Performance
- [ ] Language detection < 10ms per query
- [ ] Parser processes queries efficiently
- [ ] Translation cache provides speedup
- [ ] No memory leaks in long runs

### Integration
- [ ] End-to-end pipeline works
- [ ] Multiple languages work together
- [ ] Uncertainty triggers clarification
- [ ] Components integrate smoothly

---

## Success Criteria

The implementation is considered successful if:

1. **Language Detection**: >90% accuracy for supported languages
2. **Parsing**: All 8 languages parse queries correctly
3. **Translation**: >80% success rate for common concepts
4. **Knowledge Sharing**: Concepts accessible in 5+ languages
5. **Uncertainty**: Properly detected and triggers clarification
6. **Performance**: Meets or exceeds performance targets
7. **Integration**: All components work together seamlessly

---

## Next Steps After Testing

Once testing is complete:

1. **Document Results**: Record all test results and metrics
2. **Fix Issues**: Address any failures or performance problems
3. **Optimize**: Improve slow components
4. **Expand**: Add more language-specific patterns if needed
5. **Deploy**: Move to production when ready

---

## Support and Resources

- **Documentation**: See `doc/MULTILANGUAGE_IMPLEMENTATION_STATUS.md`
- **Architecture**: See `doc/ARCHITECTURE.md`
- **Issues**: Report in GitHub issue tracker
- **Questions**: Contact development team

---

**Testing Complete! 🎉**

Your multi-language system is ready for production use once all tests pass!
