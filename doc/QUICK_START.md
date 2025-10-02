# Multi-Language System - Quick Start Guide 🚀

**For rapid deployment and testing**

---

## ⚡ Quick Setup (2 Minutes)

### 1. Verify Installation

```bash
cd "d:\My Dev Life\AI Development\Myriad-Mind"
python -c "from myriad.core.multilang import *; print('✓ Ready!')"
```

### 2. Run Quick Test

```python
from myriad.core.multilang import get_multilang_parser

parser = get_multilang_parser()

# Test in multiple languages
queries = [
    "What is a lightbulb?",                          # English
    "¿Qué es una bombilla?",                         # Spanish
    "Qu'est-ce qu'une ampoule?",                     # French
    "Was ist eine Glühbirne?",                       # German
]

for query in queries:
    metadata, parsed = parser.parse_query(query)
    print(f"✓ {metadata.detected_language.value}: {parsed.primary_intent}")
```

**Expected Output:**
```
✓ en: define
✓ es: define
✓ fr: define
✓ de: define
```

---

## 🎯 Common Use Cases

### Use Case 1: Process Multi-Language Queries

```python
from myriad.core.multilang import get_multilang_parser

parser = get_multilang_parser()

# User query (any language)
user_query = "¿Cuál es el impacto de la tecnología?"

# Parse
metadata, parsed = parser.parse_query(user_query)

print(f"Language: {metadata.detected_language.value}")
print(f"Intent: {parsed.primary_intent}")
print(f"Concepts: {parsed.concepts}")
```

### Use Case 2: Translate Concepts

```python
from myriad.core.multilang import get_translation_service, Language

translator = get_translation_service()

# Translate
result = translator.translate('lightbulb', Language.ENGLISH, Language.SPANISH)
print(f"Translation: {result.translated_text}")  # bombilla
```

### Use Case 3: Cross-Language Knowledge

```python
from myriad.core.multilang import get_cross_language_knowledge_manager, Language

km = get_cross_language_knowledge_manager()

# Add concept
concept_id = km.add_concept('technology', Language.ENGLISH)

# Get in any language
spanish = km.get_concept_in_language(concept_id, Language.SPANISH)
french = km.get_concept_in_language(concept_id, Language.FRENCH)

print(f"Spanish: {spanish}")  # tecnología
print(f"French: {french}")    # technologie
```

### Use Case 4: Handle Uncertainty

```python
from myriad.services.processing.output_processor.output_processor import EnhancedOutputProcessor

processor = EnhancedOutputProcessor()

# Process with uncertainty
response = processor.process_collected_results({
    'query_id': 'q001',
    'collected_results': {'agent1': {'confidence': 0.15}},
    'query_metadata': {
        'original_query': 'What is quantum physics?',
        'clarification_needed': True,
        'language_info': {'detected_language': 'en'},
        'uncertainty_info': {
            'primary_uncertainty_type': 'knowledge_gap',
            'uncertainty_level': 'high',
            'uncertainty_score': 0.85
        }
    }
})

if response.requires_clarification:
    for q in response.clarification_questions:
        print(f"Q: {q['question_text']}")
```

---

## 📊 Supported Languages

| Language | Code | Detection | Parsing | Translation |
|----------|------|-----------|---------|-------------|
| English | en | ✅ | ✅ | ✅ |
| Spanish | es | ✅ | ✅ | ✅ |
| French | fr | ✅ | ✅ | ✅ |
| German | de | ✅ | ✅ | ✅ |
| Chinese | zh | ✅ | ✅ | ✅ |
| Portuguese | pt | ✅ | ✅ | ✅ |
| Italian | it | ✅ | ✅ | ✅ |
| Russian | ru | ✅ | ✅ | ✅ |
| Japanese | ja | ✅ | ⏳ | ⏳ |
| Korean | ko | ✅ | ⏳ | ⏳ |
| Arabic | ar | ✅ | ⏳ | ⏳ |

✅ Fully implemented | ⏳ Detection only (parser coming)

---

## 🧪 Quick Tests

### Test 1: Language Detection (30 seconds)

```python
from myriad.core.multilang import get_language_detector

detector = get_language_detector()

tests = [
    ("Hello world", "en"),
    ("Hola mundo", "es"),
    ("Bonjour monde", "fr"),
    ("Hallo Welt", "de"),
    ("你好世界", "zh"),
]

for text, expected in tests:
    result = detector.detect_language(text)
    status = "✓" if result.detected_language.value == expected else "✗"
    print(f"{status} {text} → {result.detected_language.value}")
```

### Test 2: Full Pipeline (1 minute)

```bash
python tests\test_multilanguage_system.py
```

---

## 🔧 Configuration

### Set Python Path (if needed)

```powershell
$env:PYTHONPATH = "d:\My Dev Life\AI Development\Myriad-Mind\src;$env:PYTHONPATH"
```

### Import Shortcuts

```python
# Instead of long imports
from myriad.core.multilang.language_detector import Language, get_language_detector
from myriad.core.multilang.multilang_parser import get_multilang_parser

# Use module import
from myriad.core.multilang import (
    Language, 
    get_language_detector, 
    get_multilang_parser,
    get_translation_service,
    get_cross_language_knowledge_manager
)
```

---

## 📚 Documentation

- **Full Details**: `doc/IMPLEMENTATION_COMPLETE.md`
- **Testing Guide**: `doc/TESTING_GUIDE.md`
- **Status**: `doc/MULTILANGUAGE_IMPLEMENTATION_STATUS.md`

---

## ⚠️ Troubleshooting

### Issue: Import Error

```python
# Add to sys.path
import sys
sys.path.insert(0, r'd:\My Dev Life\AI Development\Myriad-Mind\src')
```

### Issue: No translations found

```python
# Use dictionary concepts
concepts = ['lightbulb', 'factory', 'technology', 'electricity']
# These have pre-defined translations
```

### Issue: Low confidence

```python
# System will automatically request clarification
# Check response.requires_clarification == True
```

---

## 🎯 Performance Targets

- Language Detection: <10ms
- Query Parsing: <50ms
- Translation (dict): <1ms
- Translation (cached): <5ms
- Knowledge Lookup: <1ms

---

## 📞 Need Help?

1. Check `doc/TESTING_GUIDE.md` for detailed instructions
2. Run automated tests: `python tests\test_multilanguage_system.py`
3. Review examples in `doc/IMPLEMENTATION_COMPLETE.md`

---

**You're ready to use the multi-language system! 🎉**
