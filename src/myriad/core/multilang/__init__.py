"""
Multi-Language Support Module for Myriad Cognitive Architecture
==============================================================

This module provides comprehensive multi-language support including:
- Language detection (11+ languages)
- Language-specific query parsing
- Translation services
- Cross-language knowledge sharing

Author: Myriad Cognitive Architecture Team
Version: 1.0
Date: 2025-10-02
"""

from .language_detector import (
    Language,
    LanguageDetectionResult,
    LanguageDetector,
    get_language_detector
)

from .multilang_parser import (
    ParsedQuery,
    QueryMetadata,
    Parser,
    get_multilang_parser,
    get_parser
)

from .translation_service import (
    TranslationResult,
    CompositeTranslationService,
    get_translation_service,
    translate
)

from .cross_language_knowledge import (
    ConceptNode,
    ConceptMapping,
    CrossLanguageKnowledgeManager,
    get_cross_language_knowledge_manager
)

__all__ = [
    # Language Detection
    'Language',
    'LanguageDetectionResult',
    'LanguageDetector',
    'get_language_detector',
    
    # Multi-Language Parsing
    'ParsedQuery',
    'QueryMetadata',
    'Parser',
    'get_multilang_parser',
    'get_parser',
    
    # Translation
    'TranslationResult',
    'CompositeTranslationService',
    'get_translation_service',
    'translate',
    
    # Cross-Language Knowledge
    'ConceptNode',
    'ConceptMapping',
    'CrossLanguageKnowledgeManager',
    'get_cross_language_knowledge_manager'
]

__version__ = '1.0.0'
