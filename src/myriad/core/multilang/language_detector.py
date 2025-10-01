"""
Language Detection System for Myriad Cognitive Architecture
=========================================================

This module provides language detection capabilities to identify the language
of user queries, enabling multi-language support throughout the system.

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Language Detection)
Date: 2025-01-01
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import re
import unicodedata

class Language(Enum):
    """Supported languages"""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    ARABIC = "ar"
    PORTUGUESE = "pt"
    ITALIAN = "it"
    RUSSIAN = "ru"
    UNKNOWN = "unknown"

@dataclass
class LanguageDetectionResult:
    """Result of language detection"""
    detected_language: Language
    confidence: float  # 0.0 to 1.0
    alternatives: List[Tuple[Language, float]]
    text_sample: str
    detection_method: str

class LanguageDetector:
    """
    Detects the language of input text using multiple methods
    
    This detector uses:
    - Character set detection for CJK languages, Arabic, Cyrillic, etc.
    - Statistical language models for European languages
    - Keyword detection for language-specific markers
    - N-gram analysis for pattern recognition
    """
    
    def __init__(self):
        """Initialize the language detector"""
        
        # Language character ranges
        self.character_ranges = {
            Language.CHINESE: [
                (0x4E00, 0x9FFF),   # CJK Unified Ideographs
                (0x3400, 0x4DBF),   # CJK Unified Ideographs Extension A
                (0x20000, 0x2A6DF), # CJK Unified Ideographs Extension B
                (0x2A700, 0x2B73F), # CJK Unified Ideographs Extension C
                (0x2B740, 0x2B81F), # CJK Unified Ideographs Extension D
                (0x2B820, 0x2CEAF), # CJK Unified Ideographs Extension E
                (0x2CEB0, 0x2EBEF), # CJK Unified Ideographs Extension F
                (0x3000, 0x303F),   # CJK Symbols and Punctuation
                (0xFF00, 0xFFEF)    # Halfwidth and Fullwidth Forms
            ],
            Language.JAPANESE: [
                (0x3040, 0x309F),   # Hiragana
                (0x30A0, 0x30FF),   # Katakana
                (0x31F0, 0x31FF),   # Katakana Phonetic Extensions
                (0xFF00, 0xFFEF),    # Halfwidth and Fullwidth Forms
                (0x4E00, 0x9FFF)    # Kanji (shared with Chinese)
            ],
            Language.KOREAN: [
                (0xAC00, 0xD7AF),   # Hangul Syllables
                (0x1100, 0x11FF),   # Hangul Jamo
                (0x3130, 0x318F),   # Hangul Compatibility Jamo
                (0xFF00, 0xFFEF)    # Halfwidth and Fullwidth Forms
            ],
            Language.ARABIC: [
                (0x0600, 0x06FF),   # Arabic
                (0x0750, 0x077F),   # Arabic Supplement
                (0x08A0, 0x08FF),   # Arabic Extended-A
                (0xFB50, 0xFDFF),   # Arabic Presentation Forms-A
                (0xFE70, 0xFEFF)    # Arabic Presentation Forms-B
            ],
            Language.RUSSIAN: [
                (0x0400, 0x04FF),   # Cyrillic
                (0x0500, 0x052F),   # Cyrillic Supplement
            ]
        }
        
        # Language-specific keywords
        self.language_keywords = {
            Language.ENGLISH: {
                'common': ['the', 'and', 'is', 'are', 'was', 'were', 'be', 'have', 'has', 'had', 'do', 'does', 'did'],
                'questions': ['what', 'where', 'when', 'why', 'how', 'who', 'which', 'whose'],
                'determiners': ['a', 'an', 'this', 'that', 'these', 'those']
            },
            Language.SPANISH: {
                'common': ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le'],
                'questions': ['qué', 'dónde', 'cuándo', 'por qué', 'cómo', 'quién', 'cuál', 'cuyo'],
                'determiners': ['un', 'una', 'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas']
            },
            Language.FRENCH: {
                'common': ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir', 'que', 'pour'],
                'questions': ['quoi', 'où', 'quand', 'pourquoi', 'comment', 'qui', 'lequel'],
                'determiners': ['un', 'une', 'ce', 'cet', 'cette', 'ces', 'le', 'la', 'les']
            },
            Language.GERMAN: {
                'common': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich', 'des', 'auf'],
                'questions': ['was', 'wo', 'wann', 'warum', 'wie', 'wer', 'welcher'],
                'determiners': ['ein', 'eine', 'dieser', 'diese', 'dieses', 'jener', 'jene', 'jenes']
            },
            Language.PORTUGUESE: {
                'common': ['o', 'de', 'a', 'e', 'do', 'da', 'em', 'um', 'ser', 'estar', 'que'],
                'questions': ['o que', 'onde', 'quando', 'por que', 'como', 'quem', 'qual'],
                'determiners': ['um', 'uma', 'este', 'esta', 'estes', 'estas', 'esse', 'essa']
            },
            Language.ITALIAN: {
                'common': ['il', 'di', 'e', 'la', 'un', 'in', 'per', 'non', 'con', 'da', 'del'],
                'questions': ['cosa', 'dove', 'quando', 'perché', 'come', 'chi', 'quale'],
                'determiners': ['un', 'una', 'questo', 'questa', 'questi', 'queste', 'quello', 'quella']
            }
        }
        
        # Character n-grams for statistical analysis
        self._build_ngram_models()
    
    def _build_ngram_models(self):
        """Build n-gram models for statistical language detection"""
        # Common character n-grams for different languages
        self.ngram_models = {
            Language.ENGLISH: {
                'bigrams': ['th', 'he', 'in', 'er', 'an', 're', 'ed', 'nd', 'on', 'en'],
                'trigrams': ['the', 'and', 'ing', 'her', 'ere', 'ere', 'ent', 'tha', 'nth', 'ion']
            },
            Language.SPANISH: {
                'bigrams': ['de', 'en', 'la', 'el', 'que', 'os', 'es', 'un', 'as', 'con'],
                'trigrams': ['que', 'los', 'del', 'con', 'las', 'por', 'una', 'para', 'est', 'son']
            },
            Language.FRENCH: {
                'bigrams': ['de', 'le', 'en', 'et', 'la', 'les', 'on', 'es', 'un', 'ce'],
                'trigrams': ['les', 'que', 'est', 'pas', 'une', 'des', 'dans', 'pour', 'avec', 'par']
            },
            Language.GERMAN: {
                'bigrams': ['er', 'en', 'ch', 'te', 'de', 'nd', 'ie', 'ge', 'in', 'es'],
                'trigrams': ['der', 'die', 'und', 'den', 'ein', 'ich', 'mit', 'sich', 'das', 'für']
            },
            Language.ITALIAN: {
                'bigrams': ['di', 'la', 'il', 'le', 'de', 'in', 'un', 'gl', 'al', 're'],
                'trigrams': ['del', 'della', 'con', 'per', 'una', 'nel', 'alla', 'dall', 'che', 'non']
            },
            Language.PORTUGUESE: {
                'bigrams': ['de', 'a', 'o', 'e', 's', 'do', 'da', 'em', 'um', 'os'],
                'trigrams': ['que', 'dos', 'das', 'com', 'para', 'uma', 'pela', 'pelo', 'nos', 'est']
            }
        }
    
    def detect_language(self, text: str) -> LanguageDetectionResult:
        """
        Detect the language of the input text
        
        Args:
            text: The text to analyze
            
        Returns:
            LanguageDetectionResult with detected language and confidence
        """
        if not text or not text.strip():
            return LanguageDetectionResult(
                detected_language=Language.UNKNOWN,
                confidence=0.0,
                alternatives=[],
                text_sample="",
                detection_method="empty_input"
            )
        
        # Clean and prepare text
        clean_text = self._prepare_text(text)
        
        # Try character set detection first (fast path for non-Latin scripts)
        char_result = self._detect_by_character_set(clean_text)
        if char_result.confidence > 0.8:
            return char_result
        
        # Try keyword detection
        keyword_result = self._detect_by_keywords(clean_text)
        if keyword_result.confidence > 0.7:
            return keyword_result
        
        # Try n-gram statistical analysis
        ngram_result = self._detect_by_ngrams(clean_text)
        
        # Combine results
        return self._combine_detection_results([char_result, keyword_result, ngram_result], clean_text)
    
    def _prepare_text(self, text: str) -> str:
        """Prepare text for analysis"""
        # Normalize Unicode characters
        text = unicodedata.normalize('NFKC', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Convert to lowercase for analysis
        text = text.lower()
        
        return text
    
    def _detect_by_character_set(self, text: str) -> LanguageDetectionResult:
        """Detect language based on character sets"""
        # Count characters in each language range
        language_counts = {}
        total_chars = len(text)
        
        for char in text:
            char_code = ord(char)
            
            for language, ranges in self.character_ranges.items():
                for start, end in ranges:
                    if start <= char_code <= end:
                        language_counts[language] = language_counts.get(language, 0) + 1
                        break
        
        if not language_counts:
            return LanguageDetectionResult(
                detected_language=Language.ENGLISH,  # Default assumption
                confidence=0.1,
                alternatives=[],
                text_sample=text[:100],
                detection_method="character_set_no_match"
            )
        
        # Calculate confidence based on character distribution
        best_language = max(language_counts.items(), key=lambda x: x[1])
        best_lang, best_count = best_language
        confidence = best_count / total_chars
        
        # Create alternatives
        alternatives = [(lang, count / total_chars) for lang, count in language_counts.items() if lang != best_lang]
        alternatives.sort(key=lambda x: x[1], reverse=True)
        
        return LanguageDetectionResult(
            detected_language=best_lang,
            confidence=confidence,
            alternatives=alternatives,
            text_sample=text[:100],
            detection_method="character_set"
        )
    
    def _detect_by_keywords(self, text: str) -> LanguageDetectionResult:
        """Detect language based on keyword matching"""
        language_scores = {}
        
        for language, keyword_groups in self.language_keywords.items():
            score = 0
            total_keywords = 0
            
            for group_name, keywords in keyword_groups.items():
                for keyword in keywords:
                    total_keywords += 1
                    if keyword in text:
                        score += 1
            
            # Normalize score
            if total_keywords > 0:
                language_scores[language] = score / total_keywords
        
        if not language_scores:
            return LanguageDetectionResult(
                detected_language=Language.ENGLISH,  # Default assumption
                confidence=0.1,
                alternatives=[],
                text_sample=text[:100],
                detection_method="keywords_no_match"
            )
        
        # Find best match
        best_language = max(language_scores.items(), key=lambda x: x[1])
        best_lang, best_score = best_language
        
        # Adjust confidence based on score
        confidence = min(best_score * 2, 1.0)  # Scale up but cap at 1.0
        
        # Create alternatives
        alternatives = [(lang, score) for lang, score in language_scores.items() if lang != best_lang]
        alternatives.sort(key=lambda x: x[1], reverse=True)
        
        return LanguageDetectionResult(
            detected_language=best_lang,
            confidence=confidence,
            alternatives=alternatives,
            text_sample=text[:100],
            detection_method="keywords"
        )
    
    def _detect_by_ngrams(self, text: str) -> LanguageDetectionResult:
        """Detect language based on n-gram statistical analysis"""
        language_scores = {}
        
        for language, ngram_model in self.ngram_models.items():
            score = 0
            total_ngrams = 0
            
            # Check bigrams
            for bigram in ngram_model.get('bigrams', []):
                total_ngrams += 1
                if bigram in text:
                    score += 1
            
            # Check trigrams
            for trigram in ngram_model.get('trigrams', []):
                total_ngrams += 1
                if trigram in text:
                    score += 1
            
            # Normalize score
            if total_ngrams > 0:
                language_scores[language] = score / total_ngrams
        
        if not language_scores:
            return LanguageDetectionResult(
                detected_language=Language.ENGLISH,  # Default assumption
                confidence=0.1,
                alternatives=[],
                text_sample=text[:100],
                detection_method="ngrams_no_match"
            )
        
        # Find best match
        best_language = max(language_scores.items(), key=lambda x: x[1])
        best_lang, best_score = best_language
        
        # Adjust confidence
        confidence = min(best_score * 1.5, 1.0)  # Scale up but cap at 1.0
        
        # Create alternatives
        alternatives = [(lang, score) for lang, score in language_scores.items() if lang != best_lang]
        alternatives.sort(key=lambda x: x[1], reverse=True)
        
        return LanguageDetectionResult(
            detected_language=best_lang,
            confidence=confidence,
            alternatives=alternatives,
            text_sample=text[:100],
            detection_method="ngrams"
        )
    
    def _combine_detection_results(self, results: List[LanguageDetectionResult], 
                                 text: str) -> LanguageDetectionResult:
        """Combine results from multiple detection methods"""
        # Weight different detection methods
        method_weights = {
            "character_set": 0.5,  # Most reliable for non-Latin scripts
            "keywords": 0.3,        # Good for short texts
            "ngrams": 0.2           # Good for longer texts
        }
        
        # Calculate weighted scores
        language_scores = {}
        
        for result in results:
            weight = method_weights.get(result.detection_method, 0.1)
            language = result.detected_language
            confidence = result.confidence
            
            language_scores[language] = language_scores.get(language, 0) + (confidence * weight)
        
        if not language_scores:
            return LanguageDetectionResult(
                detected_language=Language.ENGLISH,
                confidence=0.1,
                alternatives=[],
                text_sample=text[:100],
                detection_method="combined_no_match"
            )
        
        # Find best match
        best_language = max(language_scores.items(), key=lambda x: x[1])
        best_lang, best_score = best_language
        
        # Normalize confidence
        max_possible_score = sum(method_weights.values())
        confidence = min(best_score / max_possible_score, 1.0)
        
        # Create alternatives
        alternatives = [(lang, score / max_possible_score) for lang, score in language_scores.items() if lang != best_lang]
        alternatives.sort(key=lambda x: x[1], reverse=True)
        
        return LanguageDetectionResult(
            detected_language=best_lang,
            confidence=confidence,
            alternatives=alternatives,
            text_sample=text[:100],
            detection_method="combined"
        )
    
    def get_language_name(self, language: Language) -> str:
        """Get the human-readable name of a language"""
        language_names = {
            Language.ENGLISH: "English",
            Language.SPANISH: "Español",
            Language.FRENCH: "Français",
            Language.GERMAN: "Deutsch",
            Language.CHINESE: "中文",
            Language.JAPANESE: "日本語",
            Language.KOREAN: "한국어",
            Language.ARABIC: "عربي",
            Language.PORTUGUESE: "Português",
            Language.ITALIAN: "Italiano",
            Language.RUSSIAN: "Русский",
            Language.UNKNOWN: "Unknown"
        }
        return language_names.get(language, "Unknown")
    
    def is_supported(self, language: Language) -> bool:
        """Check if a language is supported"""
        return language != Language.UNKNOWN


# Global language detector instance
language_detector = LanguageDetector()


def get_language_detector() -> LanguageDetector:
    """Get the global language detector instance"""
    return language_detector


def detect_language(text: str) -> LanguageDetectionResult:
    """
    Convenience function to detect language of text
    
    Args:
        text: The text to analyze
        
    Returns:
        LanguageDetectionResult with detected language and confidence
    """
    detector = get_language_detector()
    return detector.detect_language(text)