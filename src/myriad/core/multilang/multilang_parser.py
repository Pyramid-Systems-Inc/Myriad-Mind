"""
Parser Framework for Myriad Cognitive Architecture
============================================

This module provides a framework for parsing queries in multiple languages,
with language-specific parsers that understand the nuances of each supported language.

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Parser Framework)
Date: 2025-01-01
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re
import uuid
from datetime import datetime

from .language_detector import Language, LanguageDetector, get_language_detector

@dataclass
class ParsedQuery:
    """Language-agnostic parsed query structure"""
    primary_intent: str
    concepts: List[str]
    relationships: List[Dict[str, str]]
    complexity_score: float
    estimated_agents_needed: int
    language: Language
    language_specific_data: Dict[str, Any]

@dataclass
class QueryMetadata:
    """Metadata about the query session"""
    query_id: str
    original_query: str
    detected_language: Language
    language_confidence: float
    timestamp: str
    user_context: Dict[str, Any]

class LanguageSpecificParser(ABC):
    """Abstract base class for language-specific parsers"""
    
    def __init__(self, language: Language):
        """Initialize the language-specific parser"""
        self.language = language
        self.intent_patterns = {}
        self.concept_patterns = []
        self.relationship_patterns = {}
        self._initialize_patterns()
    
    @abstractmethod
    def _initialize_patterns(self):
        """Initialize language-specific patterns"""
        pass
    
    def parse_query(self, query: str, user_context: Optional[Dict] = None) -> Tuple[ParsedQuery, Dict[str, Any]]:
        """
        Parse a query in the specific language
        
        Args:
            query: The raw query string
            user_context: Optional user context information
            
        Returns:
            Tuple of (ParsedQuery, language-specific metadata)
        """
        # Extract primary intent
        primary_intent = self._extract_primary_intent(query)
        
        # Extract concepts
        concepts = self._extract_concepts(query)
        
        # Extract relationships
        relationships = self._extract_relationships(query, concepts)
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity_score(query, concepts, relationships)
        
        # Estimate agents needed
        estimated_agents_needed = self._estimate_agents_needed(concepts, relationships, complexity_score)
        
        # Create parsed query
        parsed_query = ParsedQuery(
            primary_intent=primary_intent,
            concepts=concepts,
            relationships=relationships,
            complexity_score=complexity_score,
            estimated_agents_needed=estimated_agents_needed,
            language=self.language,
            language_specific_data=self._extract_language_specific_data(query)
        )
        
        # Create language-specific metadata
        metadata = {
            'language': self.language.value,
            'parser_version': '1.0',
            'language_specific_features': self._get_language_features()
        }
        
        return parsed_query, metadata
    
    @abstractmethod
    def _extract_primary_intent(self, query: str) -> str:
        """Extract the primary intent from the query"""
        pass
    
    def _extract_concepts(self, query: str) -> List[str]:
        """Extract key concepts from the query"""
        concepts = set()
        
        # Extract using language-specific patterns
        for pattern in self.concept_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            concepts.update([match.lower() for match in matches if len(match) > 2])
        
        # Filter out common words and return unique concepts
        stopwords = self._get_stopwords()
        filtered_concepts = [concept for concept in concepts if concept not in stopwords]
        
        return sorted(list(set(filtered_concepts)))[:10]  # Limit to top 10 concepts
    
    def _extract_relationships(self, query: str, concepts: List[str]) -> List[Dict[str, str]]:
        """Extract relationships between concepts"""
        relationships = []
        query_lower = query.lower()
        
        # Look for relationship patterns
        for rel_type, patterns in self.relationship_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    # For simplicity, create relationships between first two concepts
                    if len(concepts) >= 2:
                        relationships.append({
                            "type": rel_type,
                            "subject": concepts[0],
                            "object": concepts[1]
                        })
                        break
        
        return relationships
    
    def _calculate_complexity_score(self, query: str, concepts: List[str], relationships: List[Dict]) -> float:
        """Calculate complexity score based on query characteristics"""
        base_score = 0.1
        
        # Length factor
        length_factor = min(len(query.split()) / 20.0, 0.3)
        
        # Concept factor
        concept_factor = min(len(concepts) / 10.0, 0.3)
        
        # Relationship factor
        relationship_factor = min(len(relationships) / 5.0, 0.2)
        
        # Question complexity factor
        question_words = self._get_question_words()
        question_factor = sum(1 for word in question_words if word in query.lower()) * 0.1
        
        complexity_score = base_score + length_factor + concept_factor + relationship_factor + question_factor
        return min(complexity_score, 1.0)  # Cap at 1.0
    
    def _estimate_agents_needed(self, concepts: List[str], relationships: List[Dict], complexity_score: float) -> int:
        """Estimate number of agents needed to answer the query"""
        base_agents = 1
        
        # One agent per major concept
        concept_agents = len(concepts)
        
        # Additional agents for relationships
        relationship_agents = len(relationships)
        
        # Complexity multiplier
        complexity_multiplier = 1 + complexity_score
        
        estimated = int((base_agents + concept_agents + relationship_agents) * complexity_multiplier)
        return max(1, min(estimated, 10))  # Between 1 and 10 agents
    
    @abstractmethod
    def _extract_language_specific_data(self, query: str) -> Dict[str, Any]:
        """Extract language-specific data from the query"""
        pass
    
    @abstractmethod
    def _get_stopwords(self) -> List[str]:
        """Get list of stopwords for this language"""
        pass
    
    @abstractmethod
    def _get_question_words(self) -> List[str]:
        """Get list of question words for this language"""
        pass
    
    @abstractmethod
    def _get_language_features(self) -> Dict[str, Any]:
        """Get language-specific features"""
        pass


class EnglishParser(LanguageSpecificParser):
    """English language parser"""
    
    def __init__(self):
        super().__init__(Language.ENGLISH)
    
    def _initialize_patterns(self):
        """Initialize English-specific patterns"""
        self.intent_patterns = {
            'define': [
                (r'\b(?:what is|define|definition of|meaning of)\b', 1.0),
                (r'\b(?:explain what|tell me about)\b', 0.8),
                (r'\b(?:describe|description of)\b', 0.7)
            ],
            'analyze_historical_context': [
                (r'\b(?:historical|history|past|evolution|development)\b', 1.0),
                (r'\b(?:when did|how did.*develop|timeline)\b', 0.9),
                (r'\b(?:origin|originated|began)\b', 0.8)
            ],
            'explain_impact': [
                (r'\b(?:impact|effect|influence|consequence|result)\b', 1.0),
                (r'\b(?:why.*important|significance|role)\b', 0.9),
                (r'\b(?:changed|transformed|affected)\b', 0.7)
            ],
            'compare': [
                (r'\b(?:compare|comparison|versus|vs|difference|similar)\b', 1.0),
                (r'\b(?:better than|worse than|advantages|disadvantages)\b', 0.9)
            ],
            'calculate': [
                (r'\b(?:calculate|compute|math|number|quantity)\b', 1.0),
                (r'\b(?:how much|how many|total|sum)\b', 0.9)
            ],
            'summarize': [
                (r'\b(?:summarize|summary|overview|brief|outline)\b', 1.0),
                (r'\b(?:main points|key aspects|in short)\b', 0.9)
            ]
        }
        
        self.concept_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
            r'\b(?:lightbulb|factory|factories|industrial|electricity|technology)\b',  # Domain-specific
            r'\b\w+(?:ing|tion|ness|ment|ity)\b'  # Abstract concepts
        ]
        
        self.relationship_patterns = {
            'causal': [r'\b(?:because|due to|caused by|resulted in|led to)\b'],
            'temporal': [r'\b(?:before|after|during|when|while)\b'],
            'comparative': [r'\b(?:than|versus|compared to|unlike)\b'],
            'functional': [r'\b(?:used for|purpose|function|role)\b']
        }
    
    def _extract_primary_intent(self, query: str) -> str:
        """Extract the primary intent from the query"""
        query_lower = query.lower()
        
        # Score each intent based on pattern matches
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, query_lower))
                score += matches * weight
            intent_scores[intent] = score
        
        # Return the highest scoring intent, default to 'define'
        if intent_scores and max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        return 'define'
    
    def _extract_language_specific_data(self, query: str) -> Dict[str, Any]:
        """Extract English-specific data from the query"""
        return {
            'has_contractions': bool(re.search(r'\b\w+\'\w+\b', query)),
            'formal_level': self._detect_formality_level(query),
            'tense': self._detect_primary_tense(query)
        }
    
    def _get_stopwords(self) -> List[str]:
        """Get English stopwords"""
        return {'the', 'and', 'for', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 'will', 'would', 'could', 'should', 'a', 'an', 'in', 'on', 'at', 'to', 'from', 'with', 'by', 'of', 'as', 'is', 'be', 'been', 'being'}
    
    def _get_question_words(self) -> List[str]:
        """Get English question words"""
        return ['why', 'how', 'when', 'where', 'what', 'which', 'who', 'whose', 'whom']
    
    def _get_language_features(self) -> Dict[str, Any]:
        """Get English language features"""
        return {
            'word_order': 'subject-verb-object',
            'has_articles': True,
            'has_gendered_nouns': False,
            'has_case_system': False
        }
    
    def _detect_formality_level(self, query: str) -> str:
        """Detect formality level of the query"""
        formal_indicators = ['please', 'could you', 'would you', 'kindly']
        informal_indicators = ['hey', 'yo', 'what\'s up', 'gonna', 'wanna']
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in query.lower())
        informal_count = sum(1 for indicator in informal_indicators if indicator in query.lower())
        
        if formal_count > informal_count:
            return 'formal'
        elif informal_count > 0:
            return 'informal'
        else:
            return 'neutral'
    
    def _detect_primary_tense(self, query: str) -> str:
        """Detect primary tense of the query"""
        past_tense_indicators = ['was', 'were', 'did', 'had', 'been']
        present_tense_indicators = ['is', 'are', 'do', 'have', 'has', 'be']
        future_tense_indicators = ['will', 'shall', 'going to']
        
        past_count = sum(1 for indicator in past_tense_indicators if indicator in query.lower())
        present_count = sum(1 for indicator in present_tense_indicators if indicator in query.lower())
        future_count = sum(1 for indicator in future_tense_indicators if indicator in query.lower())
        
        if past_count >= present_count and past_count >= future_count:
            return 'past'
        elif future_count > present_count:
            return 'future'
        else:
            return 'present'


class SpanishParser(LanguageSpecificParser):
    """Spanish language parser"""
    
    def __init__(self):
        super().__init__(Language.SPANISH)
    
    def _initialize_patterns(self):
        """Initialize Spanish-specific patterns"""
        self.intent_patterns = {
            'define': [
                (r'\b(?:qué es|definición de|significado de)\b', 1.0),
                (r'\b(?:define|definir)\b', 1.0),
                (r'\b(?:explica qué|háblame de)\b', 0.8),
                (r'\b(?:describe|descripción de)\b', 0.7)
            ],
            'analyze_historical_context': [
                (r'\b(?:histórico|historia|pasado|evolución|desarrollo)\b', 1.0),
                (r'\b(?:cuándo ocurrió|cómo se desarrolló|línea de tiempo)\b', 0.9),
                (r'\b(?:origen|se originó|comenzó)\b', 0.8)
            ],
            'explain_impact': [
                (r'\b(?:impacto|efecto|influencia|consecuencia|resultado)\b', 1.0),
                (r'\b(?:por qué.*importante|significado|rol)\b', 0.9),
                (r'\b(?:cambió|transformó|afectó)\b', 0.7)
            ],
            'compare': [
                (r'\b(?:comparar|comparación|versus|diferencia|similar)\b', 1.0),
                (r'\b(?:mejor que|peor que|ventajas|desventajas)\b', 0.9)
            ],
            'calculate': [
                (r'\b(?:calcular|computar|matemáticas|número|cantidad)\b', 1.0),
                (r'\b(?:cuánto|cuántos|total|suma)\b', 0.9)
            ],
            'summarize': [
                (r'\b(?:resumir|resumen|vista general|breve|esquema)\b', 1.0),
                (r'\b(?:puntos principales|aspectos clave|en resumen)\b', 0.9)
            ]
        }
        
        self.concept_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
            r'\b(?:bombilla|fábrica|fábricas|industrial|electricidad|tecnología)\b',  # Domain-specific
            r'\b\w+(?:ando|iendo|ción|sión|miento|dad|tad)\b'  # Abstract concepts
        ]
        
        self.relationship_patterns = {
            'causal': [r'\b(?:porque|debido a|causado por|resultó en|llevó a)\b'],
            'temporal': [r'\b(?:antes|después|durante|cuando|mientras)\b'],
            'comparative': [r'\b(?:que|versus|comparado con|a diferencia de)\b'],
            'functional': [r'\b(?:usado para|propósito|función|rol)\b']
        }
    
    def _extract_primary_intent(self, query: str) -> str:
        """Extract the primary intent from the query"""
        query_lower = query.lower()
        
        # Score each intent based on pattern matches
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, query_lower))
                score += matches * weight
            intent_scores[intent] = score
        
        # Return the highest scoring intent, default to 'define'
        if intent_scores and max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        return 'define'
    
    def _extract_language_specific_data(self, query: str) -> Dict[str, Any]:
        """Extract Spanish-specific data from the query"""
        return {
            'has_accents': bool(re.search(r'[áéíóúñüÁÉÍÓÚÑÜ]', query)),
            'formal_level': self._detect_formality_level(query),
            'verb_conjugation': self._detect_verb_conjugation(query)
        }
    
    def _get_stopwords(self) -> List[str]:
        """Get Spanish stopwords"""
        return {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'como', 'las', 'del', 'los', 'una', 'han', 'sin', 'este', 'muy', 'sobre', 'ser', 'han', 'mi', 'bien', 'aunque', 'fue', 'siendo', 'están', 'está', 'estar', 'han', 'hasta', 'hacia', 'según', 'sin', 'solo', 'sí', 'tan', 'tanto', 'todos', 'todo', 'trabajar', 'tras', 'tres', 'un', 'uno', 'usa', 'usas', 'usan', 'uso', 'usted', 'ustedes', 'van', 'vamos', 'viendo', 'vez', 'vez', 'y', 'yo', 'él'}
    
    def _get_question_words(self) -> List[str]:
        """Get Spanish question words"""
        return ['por qué', 'cómo', 'cuándo', 'dónde', 'qué', 'cuál', 'quién', 'cuyo', 'cuya', 'cuáles', 'quiénes']
    
    def _get_language_features(self) -> Dict[str, Any]:
        """Get Spanish language features"""
        return {
            'word_order': 'subject-verb-object',
            'has_articles': True,
            'has_gendered_nouns': True,
            'has_case_system': False,
            'has_verb_conjugations': True
        }
    
    def _detect_formality_level(self, query: str) -> str:
        """Detect formality level of the query"""
        formal_indicators = ['por favor', 'podría', 'quisiera', 'amablemente']
        informal_indicators = ['oye', 'chévere', 'qué onda', 'vamos']
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in query.lower())
        informal_count = sum(1 for indicator in informal_indicators if indicator in query.lower())
        
        if formal_count > informal_count:
            return 'formal'
        elif informal_count > 0:
            return 'informal'
        else:
            return 'neutral'
    
    def _detect_verb_conjugation(self, query: str) -> str:
        """Detect primary verb conjugation in the query"""
        # Simple detection of common conjugations
        if re.search(r'\b(?:estoy|estás|está|estamos|estáis|están)\b', query):
            return 'present_continuous'
        elif re.search(r'\b(?:fui|fuiste|fue|fuimos|fuisteis|fueron)\b', query):
            return 'past_simple'
        elif re.search(r'\b(?:seré|serás|será|seremos|seréis|serán)\b', query):
            return 'future_simple'
        else:
            return 'other'


class Parser:
    """
    Multi-language parser that delegates to language-specific parsers
    
    This parser:
    - Detects the language of the input query
    - Delegates parsing to the appropriate language-specific parser
    - Provides a unified interface for all supported languages
    """
    
    def __init__(self):
        """Initialize the multi-language parser"""
        self.language_detector = get_language_detector()
        self.parsers = {
            Language.ENGLISH: EnglishParser(),
            Language.SPANISH: SpanishParser(),
            # Additional parsers can be added here
        }
    
    def parse_query(self, query: str, user_context: Optional[Dict] = None) -> Tuple[QueryMetadata, ParsedQuery]:
        """
        Parse a query using the appropriate language-specific parser
        
        Args:
            query: The raw query string
            user_context: Optional user context information
            
        Returns:
            Tuple of (QueryMetadata, ParsedQuery)
        """
        # Detect language
        language_result = self.language_detector.detect_language(query)
        detected_language = language_result.detected_language
        
        # Get appropriate parser
        parser = self.parsers.get(detected_language, self.parsers[Language.ENGLISH])  # Fallback to English
        
        # Parse the query
        parsed_query, language_metadata = parser.parse_query(query, user_context)
        
        # Create query metadata
        query_metadata = QueryMetadata(
            query_id=f"q_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}",
            original_query=query,
            detected_language=detected_language,
            language_confidence=language_result.confidence,
            timestamp=datetime.now().isoformat(),
            user_context=user_context or {
                "session_id": f"sess_{str(uuid.uuid4())[:8]}",
                "previous_queries": [],
                "preferred_detail_level": "standard"
            }
        )
        
        # Add language metadata to query metadata
        query_metadata.user_context.update(language_metadata)
        
        return query_metadata, parsed_query


# Global parser instance
parser = Parser()


def get_parser() -> Parser:
    """Get the global parser instance"""
    return parser