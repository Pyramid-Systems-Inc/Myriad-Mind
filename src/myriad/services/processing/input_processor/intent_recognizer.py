"""
Intent Recognizer for the Enhanced Input Processor
Implements Task 3.1.2: Intent Recognizer with support for multiple intent types

This module provides sophisticated intent recognition with context-aware detection,
confidence scoring, and ambiguity detection capabilities.
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class IntentType(Enum):
    """Supported intent types as specified in the roadmap"""
    DEFINE = "define"
    ANALYZE_HISTORICAL_CONTEXT = "analyze_historical_context"
    EXPLAIN_IMPACT = "explain_impact"
    COMPARE = "compare"
    CALCULATE = "calculate"
    SUMMARIZE = "summarize"

@dataclass
class IntentResult:
    """Result of intent recognition"""
    primary_intent: str
    confidence: float
    alternative_intents: List[Tuple[str, float]]
    is_ambiguous: bool
    context_factors: Dict[str, float]

class IntentRecognizer:
    """
    Advanced Intent Recognizer with context-aware detection
    
    Features:
    - Multi-intent support as specified in roadmap
    - Context-aware intent detection based on query complexity and domain
    - Intent confidence scoring and ambiguity detection
    - Support for compound queries with multiple intents
    """
    
    def __init__(self):
        """Initialize the intent recognizer with patterns and weights"""
        
        # Enhanced intent patterns with weights
        self.intent_patterns = {
            IntentType.DEFINE.value: {
                'primary': [
                    (r'\b(?:what is|what are)\b', 1.0),
                    (r'\b(?:define|definition of)\b', 1.0),
                    (r'\b(?:meaning of|means)\b', 0.9),
                    (r'\b(?:explain what|tell me about)\b', 0.8),
                    (r'\b(?:describe|description of)\b', 0.7)
                ],
                'secondary': [
                    (r'\?$', 0.3),  # Question mark
                    (r'\b(?:concept|term|word)\b', 0.2)
                ]
            },
            
            IntentType.ANALYZE_HISTORICAL_CONTEXT.value: {
                'primary': [
                    (r'\b(?:historical|history|past)\b', 1.0),
                    (r'\b(?:evolution|development|timeline)\b', 0.9),
                    (r'\b(?:when did|how did.*develop)\b', 0.9),
                    (r'\b(?:origin|originated|began)\b', 0.8),
                    (r'\b(?:background|context)\b', 0.7)
                ],
                'secondary': [
                    (r'\b(?:century|decade|year|era)\b', 0.3),
                    (r'\b(?:before|after|during)\b', 0.2)
                ]
            },
            
            IntentType.EXPLAIN_IMPACT.value: {
                'primary': [
                    (r'\b(?:impact|effect|influence)\b', 1.0),
                    (r'\b(?:consequence|result|outcome)\b', 0.9),
                    (r'\b(?:why.*important|significance)\b', 0.9),
                    (r'\b(?:role|purpose|function)\b', 0.8),
                    (r'\b(?:changed|transformed|affected)\b', 0.7)
                ],
                'secondary': [
                    (r'\b(?:because|due to|caused)\b', 0.3),
                    (r'\b(?:led to|resulted in)\b', 0.3)
                ]
            },
            
            IntentType.COMPARE.value: {
                'primary': [
                    (r'\b(?:compare|comparison|versus|vs)\b', 1.0),
                    (r'\b(?:difference|different|differ)\b', 0.9),
                    (r'\b(?:similar|similarity|alike)\b', 0.8),
                    (r'\b(?:better than|worse than)\b', 0.9),
                    (r'\b(?:advantages|disadvantages)\b', 0.8)
                ],
                'secondary': [
                    (r'\b(?:both|either|neither)\b', 0.2),
                    (r'\b(?:contrast|unlike)\b', 0.3)
                ]
            },
            
            IntentType.CALCULATE.value: {
                'primary': [
                    (r'\b(?:calculate|compute|math)\b', 1.0),
                    (r'\b(?:how much|how many)\b', 0.9),
                    (r'\b(?:total|sum|amount)\b', 0.8),
                    (r'\b(?:number|quantity|count)\b', 0.7),
                    (r'\b(?:percentage|percent|ratio)\b', 0.8)
                ],
                'secondary': [
                    (r'\d+', 0.4),  # Contains numbers
                    (r'[+\-*/=]', 0.3)  # Mathematical operators
                ]
            },
            
            IntentType.SUMMARIZE.value: {
                'primary': [
                    (r'\b(?:summarize|summary|overview)\b', 1.0),
                    (r'\b(?:brief|briefly|outline)\b', 0.9),
                    (r'\b(?:main points|key aspects)\b', 0.9),
                    (r'\b(?:in short|in brief)\b', 0.8),
                    (r'\b(?:highlights|key features)\b', 0.7)
                ],
                'secondary': [
                    (r'\b(?:list|points|aspects)\b', 0.2),
                    (r'\b(?:overall|general)\b', 0.2)
                ]
            }
        }
        
        # Context factors that influence intent detection
        self.context_weights = {
            'query_length': {
                'short': {'define': 0.2, 'calculate': 0.1},  # Short queries often definitions
                'medium': {'explain_impact': 0.1, 'compare': 0.1},
                'long': {'analyze_historical_context': 0.2, 'summarize': 0.1}
            },
            'domain_indicators': {
                'historical': {'analyze_historical_context': 0.3, 'explain_impact': 0.1},
                'technical': {'define': 0.2, 'explain_impact': 0.1},
                'comparative': {'compare': 0.3},
                'quantitative': {'calculate': 0.4}
            }
        }
        
        # Ambiguity thresholds
        self.ambiguity_threshold = 0.3  # If top two intents are within this range, it's ambiguous
        self.confidence_threshold = 0.6  # Minimum confidence for clear intent
    
    def recognize_intent(self, query: str, context: Optional[Dict] = None) -> IntentResult:
        """
        Recognize the primary intent of a query with confidence scoring
        
        Args:
            query: The input query string
            context: Optional context information (domain, previous queries, etc.)
            
        Returns:
            IntentResult with primary intent, confidence, and alternatives
        """
        query_lower = query.lower().strip()
        
        # Calculate base scores for each intent
        intent_scores = self._calculate_base_scores(query_lower)
        
        # Apply context factors
        context_factors = self._analyze_context_factors(query, context)
        intent_scores = self._apply_context_weights(intent_scores, context_factors)
        
        # Sort intents by score
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Determine primary intent and confidence
        primary_intent = sorted_intents[0][0]
        primary_score = sorted_intents[0][1]
        
        # Normalize confidence (convert raw score to 0-1 range)
        confidence = min(primary_score / 2.0, 1.0)  # Assuming max possible score is ~2.0
        
        # Check for ambiguity
        is_ambiguous = False
        if len(sorted_intents) > 1:
            second_score = sorted_intents[1][1]
            score_difference = primary_score - second_score
            is_ambiguous = score_difference < self.ambiguity_threshold
        
        # Prepare alternative intents
        alternative_intents = [
            (intent, min(score / 2.0, 1.0)) 
            for intent, score in sorted_intents[1:4]  # Top 3 alternatives
            if score > 0.1
        ]
        
        return IntentResult(
            primary_intent=primary_intent,
            confidence=confidence,
            alternative_intents=alternative_intents,
            is_ambiguous=is_ambiguous,
            context_factors=context_factors
        )
    
    def _calculate_base_scores(self, query: str) -> Dict[str, float]:
        """Calculate base scores for each intent based on pattern matching"""
        scores = {intent.value: 0.0 for intent in IntentType}
        
        for intent, pattern_groups in self.intent_patterns.items():
            # Primary patterns (stronger indicators)
            for pattern, weight in pattern_groups['primary']:
                matches = len(re.findall(pattern, query))
                scores[intent] += matches * weight
            
            # Secondary patterns (weaker indicators)
            for pattern, weight in pattern_groups['secondary']:
                matches = len(re.findall(pattern, query))
                scores[intent] += matches * weight
        
        return scores
    
    def _analyze_context_factors(self, query: str, context: Optional[Dict]) -> Dict[str, float]:
        """Analyze contextual factors that influence intent detection"""
        factors = {}
        
        # Query length factor
        word_count = len(query.split())
        if word_count <= 5:
            factors['query_length'] = 'short'
        elif word_count <= 15:
            factors['query_length'] = 'medium'
        else:
            factors['query_length'] = 'long'
        
        # Domain indicators
        domain_keywords = {
            'historical': ['history', 'historical', 'past', 'century', 'era', 'timeline'],
            'technical': ['technology', 'technical', 'system', 'process', 'mechanism'],
            'comparative': ['versus', 'vs', 'compare', 'than', 'better', 'worse'],
            'quantitative': ['number', 'amount', 'calculate', 'how much', 'how many']
        }
        
        query_lower = query.lower()
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                factors[f'domain_{domain}'] = 1.0
        
        # Context from previous queries (if available)
        if context and 'previous_queries' in context:
            # This would analyze patterns in previous queries
            # For now, we'll keep it simple
            factors['has_context'] = len(context['previous_queries']) > 0
        
        return factors
    
    def _apply_context_weights(self, base_scores: Dict[str, float], context_factors: Dict[str, float]) -> Dict[str, float]:
        """Apply context-based weights to base scores"""
        adjusted_scores = base_scores.copy()
        
        # Apply query length weights
        if 'query_length' in context_factors:
            length_category = context_factors['query_length']
            if length_category in self.context_weights['query_length']:
                for intent, weight in self.context_weights['query_length'][length_category].items():
                    adjusted_scores[intent] += weight
        
        # Apply domain weights
        for factor_key, factor_value in context_factors.items():
            if factor_key.startswith('domain_') and factor_value > 0:
                domain = factor_key.replace('domain_', '')
                if domain in self.context_weights['domain_indicators']:
                    for intent, weight in self.context_weights['domain_indicators'][domain].items():
                        adjusted_scores[intent] += weight * factor_value
        
        return adjusted_scores
