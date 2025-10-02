"""
Translation Service for Myriad Cognitive Architecture
====================================================

This module provides translation capabilities to support cross-language
knowledge sharing and query understanding.

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Translation Service)
Date: 2025-10-02
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re
from abc import ABC, abstractmethod

from .language_detector import Language

@dataclass
class TranslationResult:
    """Result of a translation operation"""
    source_language: Language
    target_language: Language
    source_text: str
    translated_text: str
    confidence: float
    method: str  # 'dictionary', 'api', 'cached'
    
class TranslationProvider(ABC):
    """Abstract base class for translation providers"""
    
    @abstractmethod
    def translate(self, text: str, source_lang: Language, target_lang: Language) -> TranslationResult:
        """Translate text from source language to target language"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this translation provider is available"""
        pass

class DictionaryTranslationProvider(TranslationProvider):
    """
    Dictionary-based translation for common concepts
    
    This provider uses pre-defined dictionaries for translating
    common concepts and terms. Fast but limited coverage.
    """
    
    def __init__(self):
        """Initialize with common concept dictionaries"""
        self.concept_dictionaries = self._load_concept_dictionaries()
    
    def _load_concept_dictionaries(self) -> Dict[str, Dict[Language, str]]:
        """Load common concept translations"""
        return {
            # Technology concepts
            'lightbulb': {
                Language.ENGLISH: 'lightbulb',
                Language.SPANISH: 'bombilla',
                Language.FRENCH: 'ampoule',
                Language.GERMAN: 'Glühbirne',
                Language.CHINESE: '灯泡',
                Language.PORTUGUESE: 'lâmpada',
                Language.ITALIAN: 'lampadina',
                Language.RUSSIAN: 'лампочка'
            },
            'factory': {
                Language.ENGLISH: 'factory',
                Language.SPANISH: 'fábrica',
                Language.FRENCH: 'usine',
                Language.GERMAN: 'Fabrik',
                Language.CHINESE: '工厂',
                Language.PORTUGUESE: 'fábrica',
                Language.ITALIAN: 'fabbrica',
                Language.RUSSIAN: 'фабрика'
            },
            'electricity': {
                Language.ENGLISH: 'electricity',
                Language.SPANISH: 'electricidad',
                Language.FRENCH: 'électricité',
                Language.GERMAN: 'Elektrizität',
                Language.CHINESE: '电力',
                Language.PORTUGUESE: 'eletricidade',
                Language.ITALIAN: 'elettricità',
                Language.RUSSIAN: 'электричество'
            },
            'technology': {
                Language.ENGLISH: 'technology',
                Language.SPANISH: 'tecnología',
                Language.FRENCH: 'technologie',
                Language.GERMAN: 'Technologie',
                Language.CHINESE: '技术',
                Language.PORTUGUESE: 'tecnologia',
                Language.ITALIAN: 'tecnologia',
                Language.RUSSIAN: 'технология'
            },
            'history': {
                Language.ENGLISH: 'history',
                Language.SPANISH: 'historia',
                Language.FRENCH: 'histoire',
                Language.GERMAN: 'Geschichte',
                Language.CHINESE: '历史',
                Language.PORTUGUESE: 'história',
                Language.ITALIAN: 'storia',
                Language.RUSSIAN: 'история'
            },
            'impact': {
                Language.ENGLISH: 'impact',
                Language.SPANISH: 'impacto',
                Language.FRENCH: 'impact',
                Language.GERMAN: 'Auswirkung',
                Language.CHINESE: '影响',
                Language.PORTUGUESE: 'impacto',
                Language.ITALIAN: 'impatto',
                Language.RUSSIAN: 'влияние'
            },
            'invention': {
                Language.ENGLISH: 'invention',
                Language.SPANISH: 'invención',
                Language.FRENCH: 'invention',
                Language.GERMAN: 'Erfindung',
                Language.CHINESE: '发明',
                Language.PORTUGUESE: 'invenção',
                Language.ITALIAN: 'invenzione',
                Language.RUSSIAN: 'изобретение'
            },
            'development': {
                Language.ENGLISH: 'development',
                Language.SPANISH: 'desarrollo',
                Language.FRENCH: 'développement',
                Language.GERMAN: 'Entwicklung',
                Language.CHINESE: '发展',
                Language.PORTUGUESE: 'desenvolvimento',
                Language.ITALIAN: 'sviluppo',
                Language.RUSSIAN: 'развитие'
            },
            'industrial': {
                Language.ENGLISH: 'industrial',
                Language.SPANISH: 'industrial',
                Language.FRENCH: 'industriel',
                Language.GERMAN: 'industriell',
                Language.CHINESE: '工业',
                Language.PORTUGUESE: 'industrial',
                Language.ITALIAN: 'industriale',
                Language.RUSSIAN: 'промышленный'
            },
            'revolution': {
                Language.ENGLISH: 'revolution',
                Language.SPANISH: 'revolución',
                Language.FRENCH: 'révolution',
                Language.GERMAN: 'Revolution',
                Language.CHINESE: '革命',
                Language.PORTUGUESE: 'revolução',
                Language.ITALIAN: 'rivoluzione',
                Language.RUSSIAN: 'революция'
            }
        }
    
    def translate(self, text: str, source_lang: Language, target_lang: Language) -> Optional[TranslationResult]:
        """Translate using dictionary lookup"""
        text_lower = text.lower().strip()
        
        # Look for exact match in dictionaries
        for concept_key, translations in self.concept_dictionaries.items():
            source_term = translations.get(source_lang, '').lower()
            if source_term == text_lower:
                target_term = translations.get(target_lang)
                if target_term:
                    return TranslationResult(
                        source_language=source_lang,
                        target_language=target_lang,
                        source_text=text,
                        translated_text=target_term,
                        confidence=1.0,
                        method='dictionary'
                    )
        
        return None
    
    def is_available(self) -> bool:
        """Dictionary is always available"""
        return True
    
    def get_all_translations(self, concept: str, source_lang: Language) -> Dict[Language, str]:
        """Get translations of a concept in all supported languages"""
        concept_lower = concept.lower().strip()
        
        for concept_key, translations in self.concept_dictionaries.items():
            source_term = translations.get(source_lang, '').lower()
            if source_term == concept_lower:
                return translations
        
        return {}


class CachedTranslationProvider(TranslationProvider):
    """
    Cached translation provider to reduce API calls
    
    This provider caches translation results to avoid
    redundant API calls for the same translations.
    """
    
    def __init__(self, backend_provider: TranslationProvider):
        """Initialize with a backend translation provider"""
        self.backend_provider = backend_provider
        self.cache: Dict[Tuple[str, Language, Language], TranslationResult] = {}
        self.cache_hits = 0
        self.cache_misses = 0
    
    def translate(self, text: str, source_lang: Language, target_lang: Language) -> TranslationResult:
        """Translate with caching"""
        cache_key = (text, source_lang, target_lang)
        
        # Check cache first
        if cache_key in self.cache:
            self.cache_hits += 1
            cached_result = self.cache[cache_key]
            # Update method to indicate it was cached
            return TranslationResult(
                source_language=cached_result.source_language,
                target_language=cached_result.target_language,
                source_text=cached_result.source_text,
                translated_text=cached_result.translated_text,
                confidence=cached_result.confidence,
                method='cached'
            )
        
        # Cache miss - use backend
        self.cache_misses += 1
        result = self.backend_provider.translate(text, source_lang, target_lang)
        
        # Cache the result
        if result:
            self.cache[cache_key] = result
        
        return result
    
    def is_available(self) -> bool:
        """Available if backend is available"""
        return self.backend_provider.is_available()
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return {
            'cache_size': len(self.cache),
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate': self.cache_hits / max(self.cache_hits + self.cache_misses, 1)
        }
    
    def clear_cache(self):
        """Clear the translation cache"""
        self.cache.clear()
        self.cache_hits = 0
        self.cache_misses = 0


class MockAPITranslationProvider(TranslationProvider):
    """
    Mock API translation provider for testing
    
    In production, this would be replaced with actual translation APIs
    like Google Translate, Azure Translator, or DeepL.
    """
    
    def __init__(self):
        """Initialize mock translator"""
        self.call_count = 0
    
    def translate(self, text: str, source_lang: Language, target_lang: Language) -> TranslationResult:
        """
        Mock translation - returns a placeholder
        
        In production, this would call a real translation API
        """
        self.call_count += 1
        
        # For now, just return a mock translation
        # In production, replace with actual API call
        return TranslationResult(
            source_language=source_lang,
            target_language=target_lang,
            source_text=text,
            translated_text=f"[{target_lang.value}] {text}",
            confidence=0.8,
            method='mock_api'
        )
    
    def is_available(self) -> bool:
        """Mock API is always available"""
        return True


class CompositeTranslationService:
    """
    Composite translation service that tries multiple providers
    
    This service attempts translation using multiple providers in order:
    1. Dictionary-based (fast, high confidence for known concepts)
    2. Cached translations (fast, previously translated)
    3. API-based (slower, lower confidence, but broad coverage)
    """
    
    def __init__(self):
        """Initialize with multiple translation providers"""
        self.dictionary_provider = DictionaryTranslationProvider()
        
        # In production, use real API provider
        # For now, use mock
        api_provider = MockAPITranslationProvider()
        self.cached_api_provider = CachedTranslationProvider(api_provider)
        
        self.translation_attempts = 0
        self.successful_translations = 0
    
    def translate(self, text: str, source_lang: Language, target_lang: Language) -> Optional[TranslationResult]:
        """
        Translate text using the best available method
        
        Args:
            text: Text to translate
            source_lang: Source language
            target_lang: Target language
            
        Returns:
            TranslationResult or None if translation failed
        """
        self.translation_attempts += 1
        
        # Skip if source and target are the same
        if source_lang == target_lang:
            return TranslationResult(
                source_language=source_lang,
                target_language=target_lang,
                source_text=text,
                translated_text=text,
                confidence=1.0,
                method='same_language'
            )
        
        # Try dictionary first (fastest, most accurate for known concepts)
        dict_result = self.dictionary_provider.translate(text, source_lang, target_lang)
        if dict_result:
            self.successful_translations += 1
            return dict_result
        
        # Try cached API (fast for repeated translations)
        try:
            api_result = self.cached_api_provider.translate(text, source_lang, target_lang)
            if api_result:
                self.successful_translations += 1
                return api_result
        except Exception as e:
            print(f"Translation API error: {e}")
        
        return None
    
    def translate_batch(self, texts: List[str], source_lang: Language, 
                       target_lang: Language) -> List[Optional[TranslationResult]]:
        """
        Translate multiple texts efficiently
        
        Args:
            texts: List of texts to translate
            source_lang: Source language
            target_lang: Target language
            
        Returns:
            List of TranslationResult objects (or None for failed translations)
        """
        return [self.translate(text, source_lang, target_lang) for text in texts]
    
    def get_all_translations(self, concept: str, source_lang: Language) -> Dict[Language, str]:
        """
        Get translations of a concept in all supported languages
        
        Args:
            concept: Concept to translate
            source_lang: Source language
            
        Returns:
            Dictionary mapping Language to translated text
        """
        return self.dictionary_provider.get_all_translations(concept, source_lang)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get translation service statistics"""
        stats = {
            'total_attempts': self.translation_attempts,
            'successful_translations': self.successful_translations,
            'success_rate': self.successful_translations / max(self.translation_attempts, 1)
        }
        
        # Add cache stats
        stats['cache_stats'] = self.cached_api_provider.get_cache_stats()
        
        return stats


# Global translation service instance
_global_translation_service = None


def get_translation_service() -> CompositeTranslationService:
    """
    Get the global translation service instance (singleton pattern)
    
    Returns:
        CompositeTranslationService: The global translation service
    """
    global _global_translation_service
    if _global_translation_service is None:
        _global_translation_service = CompositeTranslationService()
    return _global_translation_service


def translate(text: str, source_lang: str, target_lang: str) -> Optional[str]:
    """
    Convenience function to translate text
    
    Args:
        text: Text to translate
        source_lang: Source language code (e.g., 'en', 'es')
        target_lang: Target language code
        
    Returns:
        Translated text or None if translation failed
    """
    service = get_translation_service()
    
    try:
        source = Language(source_lang)
        target = Language(target_lang)
        result = service.translate(text, source, target)
        return result.translated_text if result else None
    except ValueError:
        return None
