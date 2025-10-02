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


class FrenchParser(LanguageSpecificParser):
    """French language parser"""
    
    def __init__(self):
        super().__init__(Language.FRENCH)
    
    def _initialize_patterns(self):
        """Initialize French-specific patterns"""
        self.intent_patterns = {
            'define': [
                (r'\b(?:qu\'est-ce que|qu\'est-ce qu\'|définition de|sens de)\b', 1.0),
                (r'\b(?:définir|définition)\b', 1.0),
                (r'\b(?:explique ce que|parle-moi de|dis-moi)\b', 0.8),
                (r'\b(?:décris|description de)\b', 0.7)
            ],
            'analyze_historical_context': [
                (r'\b(?:historique|histoire|passé|évolution|développement)\b', 1.0),
                (r'\b(?:quand est-ce que|comment s\'est développé|chronologie)\b', 0.9),
                (r'\b(?:origine|a commencé|débuté)\b', 0.8)
            ],
            'explain_impact': [
                (r'\b(?:impact|effet|influence|conséquence|résultat)\b', 1.0),
                (r'\b(?:pourquoi.*important|signification|rôle)\b', 0.9),
                (r'\b(?:changé|transformé|affecté)\b', 0.7)
            ],
            'compare': [
                (r'\b(?:comparer|comparaison|versus|différence|similaire)\b', 1.0),
                (r'\b(?:meilleur que|pire que|avantages|inconvénients)\b', 0.9)
            ],
            'calculate': [
                (r'\b(?:calculer|calcul|mathématiques|nombre|quantité)\b', 1.0),
                (r'\b(?:combien|total|somme)\b', 0.9)
            ],
            'summarize': [
                (r'\b(?:résumer|résumé|aperçu|bref|plan)\b', 1.0),
                (r'\b(?:points principaux|aspects clés|en bref)\b', 0.9)
            ]
        }
        
        self.concept_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
            r'\b(?:ampoule|usine|usines|industriel|électricité|technologie)\b',  # Domain-specific
            r'\b\w+(?:tion|sion|ment|ité|age|ance|ence)\b'  # Abstract concepts
        ]
        
        self.relationship_patterns = {
            'causal': [r'\b(?:parce que|à cause de|causé par|résulté en|a conduit à)\b'],
            'temporal': [r'\b(?:avant|après|pendant|quand|tandis que)\b'],
            'comparative': [r'\b(?:que|versus|comparé à|contrairement à)\b'],
            'functional': [r'\b(?:utilisé pour|but|fonction|rôle)\b']
        }
    
    def _extract_primary_intent(self, query: str) -> str:
        """Extract the primary intent from the query"""
        query_lower = query.lower()
        
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, query_lower))
                score += matches * weight
            intent_scores[intent] = score
        
        if intent_scores and max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        return 'define'
    
    def _extract_language_specific_data(self, query: str) -> Dict[str, Any]:
        """Extract French-specific data from the query"""
        return {
            'has_accents': bool(re.search(r'[àâäæçéèêëïîôùûüÿœÀÂÄÆÇÉÈÊËÏÎÔÙÛÜŸŒ]', query)),
            'formal_level': self._detect_formality_level(query),
            'has_elision': bool(re.search(r'\b\w+\'\w+\b', query))
        }
    
    def _get_stopwords(self) -> List[str]:
        """Get French stopwords"""
        return {'le', 'la', 'de', 'un', 'une', 'et', 'à', 'est', 'en', 'que', 'les', 'des', 'dans', 'il', 'elle', 'pour', 'ce', 'qui', 'au', 'sur', 'se', 'ne', 'pas', 'plus', 'peut', 'sont', 'avec', 'par', 'ont', 'du', 'ou', 'mais', 'son', 'sa', 'ses', 'nous', 'vous', 'ils', 'elles', 'tout', 'tous', 'toute', 'toutes', 'être', 'avoir', 'faire', 'comme', 'sans', 'aussi', 'bien', 'très', 'où', 'quand', 'comment', 'pourquoi'}
    
    def _get_question_words(self) -> List[str]:
        """Get French question words"""
        return ['pourquoi', 'comment', 'quand', 'où', 'que', 'quel', 'quelle', 'quels', 'quelles', 'qui', 'qu\'est-ce que', 'qu\'est-ce qui']
    
    def _get_language_features(self) -> Dict[str, Any]:
        """Get French language features"""
        return {
            'word_order': 'subject-verb-object',
            'has_articles': True,
            'has_gendered_nouns': True,
            'has_case_system': False,
            'has_verb_conjugations': True,
            'has_elision': True
        }
    
    def _detect_formality_level(self, query: str) -> str:
        """Detect formality level of the query"""
        formal_indicators = ['s\'il vous plaît', 'pourriez-vous', 'voudriez-vous', 'auriez-vous']
        informal_indicators = ['salut', 'sympa', 'cool', 'vas-y']
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in query.lower())
        informal_count = sum(1 for indicator in informal_indicators if indicator in query.lower())
        
        if formal_count > informal_count:
            return 'formal'
        elif informal_count > 0:
            return 'informal'
        else:
            return 'neutral'


class GermanParser(LanguageSpecificParser):
    """German language parser"""
    
    def __init__(self):
        super().__init__(Language.GERMAN)
    
    def _initialize_patterns(self):
        """Initialize German-specific patterns"""
        self.intent_patterns = {
            'define': [
                (r'\b(?:was ist|Definition von|Bedeutung von)\b', 1.0),
                (r'\b(?:definiere|definieren|Definition)\b', 1.0),
                (r'\b(?:erkläre was|erzähl mir über|sage mir)\b', 0.8),
                (r'\b(?:beschreibe|Beschreibung von)\b', 0.7)
            ],
            'analyze_historical_context': [
                (r'\b(?:historisch|Geschichte|Vergangenheit|Entwicklung|Evolution)\b', 1.0),
                (r'\b(?:wann|wie entwickelte sich|Zeitlinie|Zeitstrahl)\b', 0.9),
                (r'\b(?:Ursprung|entstand|begann)\b', 0.8)
            ],
            'explain_impact': [
                (r'\b(?:Auswirkung|Effekt|Einfluss|Folge|Ergebnis)\b', 1.0),
                (r'\b(?:warum.*wichtig|Bedeutung|Rolle)\b', 0.9),
                (r'\b(?:veränderte|verwandelte|beeinflusste)\b', 0.7)
            ],
            'compare': [
                (r'\b(?:vergleichen|Vergleich|versus|Unterschied|ähnlich)\b', 1.0),
                (r'\b(?:besser als|schlechter als|Vorteile|Nachteile)\b', 0.9)
            ],
            'calculate': [
                (r'\b(?:berechnen|rechnen|Mathematik|Zahl|Menge)\b', 1.0),
                (r'\b(?:wie viel|wie viele|gesamt|Summe)\b', 0.9)
            ],
            'summarize': [
                (r'\b(?:zusammenfassen|Zusammenfassung|Überblick|kurz|Gliederung)\b', 1.0),
                (r'\b(?:Hauptpunkte|wichtigste Aspekte|kurz gesagt)\b', 0.9)
            ]
        }
        
        self.concept_patterns = [
            r'\b[A-ZÄÖÜ][a-zäöüß]+(?:[A-ZÄÖÜ][a-zäöüß]+)*\b',  # German compound nouns (capitalized)
            r'\b(?:Glühbirne|Fabrik|Fabriken|industriell|Elektrizität|Technologie)\b',  # Domain-specific
            r'\b[A-ZÄÖÜ]\w+(?:ung|heit|keit|schaft|tät|tum)\b'  # Abstract concepts
        ]
        
        self.relationship_patterns = {
            'causal': [r'\b(?:weil|aufgrund|verursacht durch|führte zu|resultierte in)\b'],
            'temporal': [r'\b(?:vor|nach|während|wenn|als|währenddessen)\b'],
            'comparative': [r'\b(?:als|versus|im Vergleich zu|im Gegensatz zu)\b'],
            'functional': [r'\b(?:verwendet für|Zweck|Funktion|Rolle)\b']
        }
    
    def _extract_primary_intent(self, query: str) -> str:
        """Extract the primary intent from the query"""
        # German is case-sensitive, so we need to be careful with case
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, query, re.IGNORECASE))
                score += matches * weight
            intent_scores[intent] = score
        
        if intent_scores and max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        return 'define'
    
    def _extract_language_specific_data(self, query: str) -> Dict[str, Any]:
        """Extract German-specific data from the query"""
        return {
            'has_umlauts': bool(re.search(r'[äöüÄÖÜß]', query)),
            'formal_level': self._detect_formality_level(query),
            'has_compound_words': self._detect_compound_words(query),
            'has_capitalized_nouns': bool(re.search(r'\b[A-ZÄÖÜ][a-zäöüß]+\b', query))
        }
    
    def _get_stopwords(self) -> List[str]:
        """Get German stopwords"""
        return {'der', 'die', 'das', 'den', 'dem', 'des', 'ein', 'eine', 'einer', 'eines', 'einem', 'einen', 'und', 'oder', 'aber', 'ist', 'sind', 'war', 'waren', 'sein', 'haben', 'hat', 'hatte', 'hatten', 'wird', 'werden', 'wurde', 'wurden', 'in', 'an', 'auf', 'zu', 'von', 'mit', 'für', 'bei', 'aus', 'nach', 'über', 'unter', 'durch', 'nicht', 'auch', 'nur', 'noch', 'sehr', 'mehr', 'wie', 'wenn', 'als', 'weil', 'dass', 'ob', 'wo', 'wer', 'was', 'welche', 'welcher', 'welches'}
    
    def _get_question_words(self) -> List[str]:
        """Get German question words"""
        return ['warum', 'wie', 'wann', 'wo', 'was', 'welche', 'welcher', 'welches', 'wer', 'wessen', 'wem', 'wen']
    
    def _get_language_features(self) -> Dict[str, Any]:
        """Get German language features"""
        return {
            'word_order': 'subject-verb-object (main), verb-final (subordinate)',
            'has_articles': True,
            'has_gendered_nouns': True,
            'has_case_system': True,
            'has_verb_conjugations': True,
            'has_compound_words': True,
            'noun_capitalization': True
        }
    
    def _detect_formality_level(self, query: str) -> str:
        """Detect formality level of the query"""
        # German has formal 'Sie' vs informal 'du'
        formal_indicators = ['Sie', 'Ihnen', 'Ihr', 'bitte', 'könnten Sie', 'würden Sie']
        informal_indicators = ['du', 'dir', 'dein', 'hey', 'cool']
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in query)
        informal_count = sum(1 for indicator in informal_indicators if indicator in query)
        
        if formal_count > informal_count:
            return 'formal'
        elif informal_count > 0:
            return 'informal'
        else:
            return 'neutral'
    
    def _detect_compound_words(self, query: str) -> bool:
        """Detect if the query contains compound words (common in German)"""
        # German compound words are typically long capitalized words
        compound_pattern = r'\b[A-ZÄÖÜ][a-zäöüß]{10,}\b'
        return bool(re.search(compound_pattern, query))


class ChineseParser(LanguageSpecificParser):
    """Chinese language parser (Simplified and Traditional)"""
    
    def __init__(self):
        super().__init__(Language.CHINESE)
    
    def _initialize_patterns(self):
        """Initialize Chinese-specific patterns"""
        self.intent_patterns = {
            'define': [
                (r'(?:什么是|定义|含义|意思)', 1.0),
                (r'(?:解释|说明|介绍)', 0.8),
                (r'(?:描述|讲述)', 0.7)
            ],
            'analyze_historical_context': [
                (r'(?:历史|过去|演变|发展|起源)', 1.0),
                (r'(?:什么时候|如何发展|时间线)', 0.9),
                (r'(?:开始|起源|诞生)', 0.8)
            ],
            'explain_impact': [
                (r'(?:影响|效果|作用|后果|结果)', 1.0),
                (r'(?:为什么.*重要|意义|角色)', 0.9),
                (r'(?:改变|转变|影响了)', 0.7)
            ],
            'compare': [
                (r'(?:比较|对比|差异|相似|区别)', 1.0),
                (r'(?:更好|更差|优点|缺点|优势|劣势)', 0.9)
            ],
            'calculate': [
                (r'(?:计算|算|数学|数字|数量)', 1.0),
                (r'(?:多少|总共|总和|总计)', 0.9)
            ],
            'summarize': [
                (r'(?:总结|摘要|概述|概括|简述)', 1.0),
                (r'(?:要点|关键点|简而言之)', 0.9)
            ]
        }
        
        # Chinese concepts are typically 2-4 character compounds
        self.concept_patterns = [
            r'[\u4e00-\u9fff]{2,4}',  # 2-4 character Chinese words
            r'(?:灯泡|工厂|电力|技术|发明)',  # Domain-specific
        ]
        
        self.relationship_patterns = {
            'causal': [r'(?:因为|由于|导致|造成|使得)'],
            'temporal': [r'(?:之前|之后|期间|当|在.*时候)'],
            'comparative': [r'(?:比|与.*相比|不同于|相对于)'],
            'functional': [r'(?:用于|目的|功能|作用)']
        }
    
    def _extract_primary_intent(self, query: str) -> str:
        """Extract the primary intent from the query"""
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, query))
                score += matches * weight
            intent_scores[intent] = score
        
        if intent_scores and max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        return 'define'
    
    def _extract_concepts(self, query: str) -> List[str]:
        """Extract concepts from Chinese query - overridden for Chinese-specific handling"""
        concepts = []
        
        # Extract using patterns
        for pattern in self.concept_patterns:
            matches = re.findall(pattern, query)
            concepts.extend(matches)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_concepts = []
        for concept in concepts:
            if concept not in seen and concept not in self._get_stopwords():
                seen.add(concept)
                unique_concepts.append(concept)
        
        return unique_concepts[:10]  # Limit to top 10 concepts
    
    def _extract_language_specific_data(self, query: str) -> Dict[str, Any]:
        """Extract Chinese-specific data from the query"""
        return {
            'script_type': self._detect_script_type(query),
            'character_count': len(query),
            'has_punctuation': bool(re.search(r'[，。！？；：、]', query)),
            'formality_markers': self._detect_formality_markers(query)
        }
    
    def _get_stopwords(self) -> List[str]:
        """Get Chinese stopwords"""
        return {'的', '了', '和', '是', '在', '有', '我', '他', '她', '它', '们', '这', '那', '个', '中', '为', '与', '就', '都', '而', '及', '以', '于', '对', '从', '由', '等', '与', '把', '被', '将', '让', '使', '给', '向', '到', '着', '过', '去', '来', '不', '没', '没有', '也', '还', '更', '很', '太', '最', '非常', '如何', '怎么', '什么', '哪个', '谁', '为什么', '何时', '哪里'}
    
    def _get_question_words(self) -> List[str]:
        """Get Chinese question words"""
        return ['为什么', '怎么', '如何', '什么时候', '哪里', '什么', '哪个', '哪些', '谁', '多少']
    
    def _get_language_features(self) -> Dict[str, Any]:
        """Get Chinese language features"""
        return {
            'word_order': 'subject-verb-object',
            'has_articles': False,
            'has_gendered_nouns': False,
            'has_case_system': False,
            'has_verb_conjugations': False,
            'has_tones': True,
            'no_spaces': True,
            'logographic': True
        }
    
    def _detect_script_type(self, query: str) -> str:
        """Detect if the text is Simplified or Traditional Chinese"""
        # Common Traditional characters not in Simplified
        traditional_chars = r'[繁體國際電腦網絡時間]'
        # Common Simplified characters not in Traditional
        simplified_chars = r'[简体国际电脑网络时间]'
        
        traditional_count = len(re.findall(traditional_chars, query))
        simplified_count = len(re.findall(simplified_chars, query))
        
        if traditional_count > simplified_count:
            return 'traditional'
        elif simplified_count > 0:
            return 'simplified'
        else:
            return 'unknown'
    
    def _detect_formality_markers(self, query: str) -> str:
        """Detect formality level in Chinese"""
        formal_markers = ['请', '敬请', '您', '贵', '尊']
        informal_markers = ['吧', '呢', '啊', '哦', '嘛']
        
        formal_count = sum(1 for marker in formal_markers if marker in query)
        informal_count = sum(1 for marker in informal_markers if marker in query)
        
        if formal_count > informal_count:
            return 'formal'
        elif informal_count > 0:
            return 'informal'
        else:
            return 'neutral'


class PortugueseParser(LanguageSpecificParser):
    """Portuguese language parser"""
    
    def __init__(self):
        super().__init__(Language.PORTUGUESE)
    
    def _initialize_patterns(self):
        """Initialize Portuguese-specific patterns"""
        self.intent_patterns = {
            'define': [
                (r'\b(?:o que é|definição de|significado de)\b', 1.0),
                (r'\b(?:definir|definição)\b', 1.0),
                (r'\b(?:explica o que|fala sobre|me diz)\b', 0.8),
                (r'\b(?:descreve|descrição de)\b', 0.7)
            ],
            'analyze_historical_context': [
                (r'\b(?:histórico|história|passado|evolução|desenvolvimento)\b', 1.0),
                (r'\b(?:quando|como se desenvolveu|linha do tempo)\b', 0.9),
                (r'\b(?:origem|originou|começou)\b', 0.8)
            ],
            'explain_impact': [
                (r'\b(?:impacto|efeito|influência|consequência|resultado)\b', 1.0),
                (r'\b(?:por que.*importante|significado|papel)\b', 0.9),
                (r'\b(?:mudou|transformou|afetou)\b', 0.7)
            ],
            'compare': [
                (r'\b(?:comparar|comparação|versus|diferença|similar)\b', 1.0),
                (r'\b(?:melhor que|pior que|vantagens|desvantagens)\b', 0.9)
            ],
            'calculate': [
                (r'\b(?:calcular|computar|matemática|número|quantidade)\b', 1.0),
                (r'\b(?:quanto|quantos|total|soma)\b', 0.9)
            ],
            'summarize': [
                (r'\b(?:resumir|resumo|visão geral|breve|esquema)\b', 1.0),
                (r'\b(?:pontos principais|aspectos chave|em resumo)\b', 0.9)
            ]
        }
        
        self.concept_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
            r'\b(?:lâmpada|fábrica|fábricas|industrial|eletricidade|tecnologia)\b',  # Domain-specific
            r'\b\w+(?:ção|são|mento|dade|eza|ismo)\b'  # Abstract concepts
        ]
        
        self.relationship_patterns = {
            'causal': [r'\b(?:porque|devido a|causado por|resultou em|levou a)\b'],
            'temporal': [r'\b(?:antes|depois|durante|quando|enquanto)\b'],
            'comparative': [r'\b(?:que|versus|comparado com|ao contrário de)\b'],
            'functional': [r'\b(?:usado para|propósito|função|papel)\b']
        }
    
    def _extract_primary_intent(self, query: str) -> str:
        """Extract the primary intent from the query"""
        query_lower = query.lower()
        
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, query_lower))
                score += matches * weight
            intent_scores[intent] = score
        
        if intent_scores and max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        return 'define'
    
    def _extract_language_specific_data(self, query: str) -> Dict[str, Any]:
        """Extract Portuguese-specific data from the query"""
        return {
            'has_accents': bool(re.search(r'[áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ]', query)),
            'formal_level': self._detect_formality_level(query),
            'variant': self._detect_variant(query)
        }
    
    def _get_stopwords(self) -> List[str]:
        """Get Portuguese stopwords"""
        return {'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 'nos', 'nas', 'por', 'para', 'com', 'sem', 'sob', 'sobre', 'e', 'ou', 'mas', 'que', 'qual', 'quais', 'é', 'são', 'foi', 'eram', 'ser', 'estar', 'ter', 'haver', 'não', 'também', 'só', 'mais', 'menos', 'muito', 'pouco', 'todo', 'toda', 'todos', 'todas', 'este', 'esta', 'estes', 'estas', 'esse', 'essa', 'esses', 'essas', 'aquele', 'aquela', 'aqueles', 'aquelas'}
    
    def _get_question_words(self) -> List[str]:
        """Get Portuguese question words"""
        return ['por que', 'porque', 'como', 'quando', 'onde', 'o que', 'qual', 'quais', 'quem', 'quanto', 'quantos', 'quantas']
    
    def _get_language_features(self) -> Dict[str, Any]:
        """Get Portuguese language features"""
        return {
            'word_order': 'subject-verb-object',
            'has_articles': True,
            'has_gendered_nouns': True,
            'has_case_system': False,
            'has_verb_conjugations': True
        }
    
    def _detect_formality_level(self, query: str) -> str:
        """Detect formality level of the query"""
        formal_indicators = ['por favor', 'poderia', 'gostaria', 'senhor', 'senhora']
        informal_indicators = ['ei', 'tipo', 'cara', 'beleza', 'valeu']
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in query.lower())
        informal_count = sum(1 for indicator in informal_indicators if indicator in query.lower())
        
        if formal_count > informal_count:
            return 'formal'
        elif informal_count > 0:
            return 'informal'
        else:
            return 'neutral'
    
    def _detect_variant(self, query: str) -> str:
        """Detect Brazilian or European Portuguese"""
        # Brazilian indicators
        brazilian_indicators = ['você', 'vocês', 'gente', 'trem', 'ônibus']
        # European indicators
        european_indicators = ['vós', 'comboio', 'autocarro']
        
        brazilian_count = sum(1 for indicator in brazilian_indicators if indicator in query.lower())
        european_count = sum(1 for indicator in european_indicators if indicator in query.lower())
        
        if brazilian_count > european_count:
            return 'brazilian'
        elif european_count > 0:
            return 'european'
        else:
            return 'unknown'


class ItalianParser(LanguageSpecificParser):
    """Italian language parser"""
    
    def __init__(self):
        super().__init__(Language.ITALIAN)
    
    def _initialize_patterns(self):
        """Initialize Italian-specific patterns"""
        self.intent_patterns = {
            'define': [
                (r'\b(?:cos\'è|che cos\'è|definizione di|significato di)\b', 1.0),
                (r'\b(?:definire|definisci)\b', 1.0),
                (r'\b(?:spiega cosa|parlami di|dimmi)\b', 0.8),
                (r'\b(?:descrivi|descrizione di)\b', 0.7)
            ],
            'analyze_historical_context': [
                (r'\b(?:storico|storia|passato|evoluzione|sviluppo)\b', 1.0),
                (r'\b(?:quando|come si è sviluppato|cronologia)\b', 0.9),
                (r'\b(?:origine|ha avuto origine|è iniziato)\b', 0.8)
            ],
            'explain_impact': [
                (r'\b(?:impatto|effetto|influenza|conseguenza|risultato)\b', 1.0),
                (r'\b(?:perché.*importante|significato|ruolo)\b', 0.9),
                (r'\b(?:cambiato|trasformato|influenzato)\b', 0.7)
            ],
            'compare': [
                (r'\b(?:confrontare|confronto|versus|differenza|simile)\b', 1.0),
                (r'\b(?:meglio di|peggio di|vantaggi|svantaggi)\b', 0.9)
            ],
            'calculate': [
                (r'\b(?:calcolare|calcolo|matematica|numero|quantità)\b', 1.0),
                (r'\b(?:quanto|quanti|totale|somma)\b', 0.9)
            ],
            'summarize': [
                (r'\b(?:riassumere|riassunto|panoramica|breve|schema)\b', 1.0),
                (r'\b(?:punti principali|aspetti chiave|in breve)\b', 0.9)
            ]
        }
        
        self.concept_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
            r'\b(?:lampadina|fabbrica|fabbriche|industriale|elettricità|tecnologia)\b',  # Domain-specific
            r'\b\w+(?:zione|sione|mento|tà|ezza|ismo)\b'  # Abstract concepts
        ]
        
        self.relationship_patterns = {
            'causal': [r'\b(?:perché|a causa di|causato da|ha portato a|è risultato in)\b'],
            'temporal': [r'\b(?:prima|dopo|durante|quando|mentre)\b'],
            'comparative': [r'\b(?:di|versus|rispetto a|a differenza di)\b'],
            'functional': [r'\b(?:usato per|scopo|funzione|ruolo)\b']
        }
    
    def _extract_primary_intent(self, query: str) -> str:
        """Extract the primary intent from the query"""
        query_lower = query.lower()
        
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, query_lower))
                score += matches * weight
            intent_scores[intent] = score
        
        if intent_scores and max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        return 'define'
    
    def _extract_language_specific_data(self, query: str) -> Dict[str, Any]:
        """Extract Italian-specific data from the query"""
        return {
            'has_accents': bool(re.search(r'[àèéìòùÀÈÉÌÒÙ]', query)),
            'formal_level': self._detect_formality_level(query),
            'has_apostrophes': bool(re.search(r'\b\w+\'\w+\b', query))
        }
    
    def _get_stopwords(self) -> List[str]:
        """Get Italian stopwords"""
        return {'il', 'lo', 'la', 'i', 'gli', 'le', 'un', 'uno', 'una', 'di', 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra', 'e', 'o', 'ma', 'che', 'chi', 'cui', 'è', 'sono', 'era', 'erano', 'essere', 'avere', 'ha', 'hanno', 'aveva', 'avevano', 'fare', 'non', 'anche', 'solo', 'più', 'meno', 'molto', 'poco', 'tutto', 'tutti', 'tutta', 'tutte', 'questo', 'questa', 'questi', 'queste', 'quello', 'quella', 'quelli', 'quelle', 'dove', 'quando', 'come', 'perché'}
    
    def _get_question_words(self) -> List[str]:
        """Get Italian question words"""
        return ['perché', 'come', 'quando', 'dove', 'cosa', 'che cosa', 'quale', 'quali', 'chi', 'quanto', 'quanti', 'quante']
    
    def _get_language_features(self) -> Dict[str, Any]:
        """Get Italian language features"""
        return {
            'word_order': 'subject-verb-object',
            'has_articles': True,
            'has_gendered_nouns': True,
            'has_case_system': False,
            'has_verb_conjugations': True,
            'has_apostrophes': True
        }
    
    def _detect_formality_level(self, query: str) -> str:
        """Detect formality level of the query"""
        formal_indicators = ['per favore', 'potrebbe', 'vorrebbe', 'gentilmente', 'lei']
        informal_indicators = ['ciao', 'tu', 'hey', 'ok', 'cool']
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in query.lower())
        informal_count = sum(1 for indicator in informal_indicators if indicator in query.lower())
        
        if formal_count > informal_count:
            return 'formal'
        elif informal_count > 0:
            return 'informal'
        else:
            return 'neutral'


class RussianParser(LanguageSpecificParser):
    """Russian language parser"""
    
    def __init__(self):
        super().__init__(Language.RUSSIAN)
    
    def _initialize_patterns(self):
        """Initialize Russian-specific patterns"""
        self.intent_patterns = {
            'define': [
                (r'(?:что такое|определение|значение)', 1.0),
                (r'(?:определить|объяснить что)', 0.8),
                (r'(?:описать|описание)', 0.7)
            ],
            'analyze_historical_context': [
                (r'(?:исторический|история|прошлое|эволюция|развитие)', 1.0),
                (r'(?:когда|как развивался|хронология)', 0.9),
                (r'(?:происхождение|возник|начался)', 0.8)
            ],
            'explain_impact': [
                (r'(?:влияние|эффект|воздействие|последствие|результат)', 1.0),
                (r'(?:почему.*важно|значение|роль)', 0.9),
                (r'(?:изменил|преобразовал|повлиял)', 0.7)
            ],
            'compare': [
                (r'(?:сравнить|сравнение|разница|похожий)', 1.0),
                (r'(?:лучше чем|хуже чем|преимущества|недостатки)', 0.9)
            ],
            'calculate': [
                (r'(?:вычислить|рассчитать|математика|число|количество)', 1.0),
                (r'(?:сколько|всего|сумма)', 0.9)
            ],
            'summarize': [
                (r'(?:резюмировать|резюме|обзор|краткий|схема)', 1.0),
                (r'(?:основные моменты|ключевые аспекты|вкратце)', 0.9)
            ]
        }
        
        self.concept_patterns = [
            r'[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)*',  # Proper nouns in Cyrillic
            r'(?:лампочка|фабрика|фабрики|промышленный|электричество|технология)',  # Domain-specific
            r'[А-ЯЁа-яё]+(?:ние|ость|ство|ция)'  # Abstract concepts
        ]
        
        self.relationship_patterns = {
            'causal': [r'(?:потому что|из-за|вызвано|привело к|в результате)'],
            'temporal': [r'(?:до|после|во время|когда|пока)'],
            'comparative': [r'(?:чем|по сравнению с|в отличие от)'],
            'functional': [r'(?:используется для|цель|функция|роль)']
        }
    
    def _extract_primary_intent(self, query: str) -> str:
        """Extract the primary intent from the query"""
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern, weight in patterns:
                matches = len(re.findall(pattern, query))
                score += matches * weight
            intent_scores[intent] = score
        
        if intent_scores and max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        return 'define'
    
    def _extract_language_specific_data(self, query: str) -> Dict[str, Any]:
        """Extract Russian-specific data from the query"""
        return {
            'has_cyrillic': bool(re.search(r'[А-Яа-яЁё]', query)),
            'formal_level': self._detect_formality_level(query),
            'has_cases': True  # Russian has 6 cases
        }
    
    def _get_stopwords(self) -> List[str]:
        """Get Russian stopwords"""
        return {'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 'между'}
    
    def _get_question_words(self) -> List[str]:
        """Get Russian question words"""
        return ['почему', 'как', 'когда', 'где', 'что', 'какой', 'какая', 'какие', 'кто', 'чей', 'сколько']
    
    def _get_language_features(self) -> Dict[str, Any]:
        """Get Russian language features"""
        return {
            'word_order': 'flexible (subject-verb-object most common)',
            'has_articles': False,
            'has_gendered_nouns': True,
            'has_case_system': True,
            'has_verb_conjugations': True,
            'number_of_cases': 6
        }
    
    def _detect_formality_level(self, query: str) -> str:
        """Detect formality level of the query"""
        # Russian has formal 'Вы' vs informal 'ты'
        formal_indicators = ['Вы', 'Вас', 'Вам', 'пожалуйста', 'будьте любезны']
        informal_indicators = ['ты', 'тебя', 'тебе', 'привет', 'пока']
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in query)
        informal_count = sum(1 for indicator in informal_indicators if indicator in query)
        
        if formal_count > informal_count:
            return 'formal'
        elif informal_count > 0:
            return 'informal'
        else:
            return 'neutral'


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
            Language.FRENCH: FrenchParser(),
            Language.GERMAN: GermanParser(),
            Language.CHINESE: ChineseParser(),
            Language.PORTUGUESE: PortugueseParser(),
            Language.ITALIAN: ItalianParser(),
            Language.RUSSIAN: RussianParser(),
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
_global_parser = None


def get_multilang_parser() -> Parser:
    """
    Get the global multi-language parser instance (singleton pattern)
    
    Returns:
        Parser: The global parser instance
    """
    global _global_parser
    if _global_parser is None:
        _global_parser = Parser()
    return _global_parser


def get_parser() -> Parser:
    """Get the global parser instance (legacy compatibility)"""
    return get_multilang_parser()