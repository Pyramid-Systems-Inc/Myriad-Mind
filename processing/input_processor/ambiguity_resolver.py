"""
Ambiguity Resolver for the Enhanced Input Processor
Implements Task 3.1.3: Ambiguity Resolver with user interaction capabilities

This module detects ambiguous concepts, generates clarification requests,
and provides context-based disambiguation with confidence indicators.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class AmbiguityType(Enum):
    """Types of ambiguity that can be detected"""
    CONCEPT_AMBIGUITY = "concept_ambiguity"  # Multiple meanings for a concept
    INTENT_AMBIGUITY = "intent_ambiguity"    # Unclear what user wants to do
    CONTEXT_AMBIGUITY = "context_ambiguity"  # Missing context for proper interpretation
    SCOPE_AMBIGUITY = "scope_ambiguity"      # Unclear scope or specificity level

@dataclass
class AmbiguityDetection:
    """Result of ambiguity detection"""
    is_ambiguous: bool
    ambiguity_type: Optional[AmbiguityType]
    ambiguous_elements: List[str]
    confidence: float
    suggested_clarifications: List[str]

@dataclass
class DisambiguationResult:
    """Result of disambiguation process"""
    resolved: bool
    chosen_interpretation: Optional[str]
    confidence: float
    fallback_interpretation: Optional[str]
    reasoning: str

class AmbiguityResolver:
    """
    Advanced Ambiguity Resolver with user interaction capabilities
    
    Features:
    - Detect ambiguous concepts and generate clarification requests
    - Context-based disambiguation using previous query history
    - Fallback to most likely interpretation with confidence indicators
    - Support for multiple types of ambiguity
    """
    
    def __init__(self):
        """Initialize the ambiguity resolver with knowledge bases"""
        
        # Known ambiguous concepts and their possible meanings
        self.ambiguous_concepts = {
            'drive': {
                'meanings': [
                    {'interpretation': 'computer_storage', 'keywords': ['hard', 'disk', 'storage', 'computer', 'data']},
                    {'interpretation': 'vehicle_operation', 'keywords': ['car', 'vehicle', 'road', 'license', 'traffic']},
                    {'interpretation': 'motivation', 'keywords': ['motivation', 'ambition', 'goal', 'desire', 'push']}
                ],
                'default': 'computer_storage'
            },
            'bank': {
                'meanings': [
                    {'interpretation': 'financial_institution', 'keywords': ['money', 'account', 'loan', 'credit', 'finance']},
                    {'interpretation': 'river_bank', 'keywords': ['river', 'water', 'shore', 'edge', 'stream']}
                ],
                'default': 'financial_institution'
            },
            'light': {
                'meanings': [
                    {'interpretation': 'illumination', 'keywords': ['bulb', 'lamp', 'bright', 'dark', 'illuminate']},
                    {'interpretation': 'weight', 'keywords': ['heavy', 'weight', 'mass', 'pound', 'kilogram']},
                    {'interpretation': 'color_shade', 'keywords': ['color', 'shade', 'pale', 'bright', 'dark']}
                ],
                'default': 'illumination'
            },
            'factory': {
                'meanings': [
                    {'interpretation': 'manufacturing_facility', 'keywords': ['production', 'manufacturing', 'industrial', 'workers']},
                    {'interpretation': 'design_pattern', 'keywords': ['software', 'pattern', 'programming', 'code', 'object']}
                ],
                'default': 'manufacturing_facility'
            }
        }
        
        # Intent ambiguity patterns
        self.intent_ambiguity_indicators = [
            r'\b(?:tell me about|about)\b',  # Very general request
            r'\b(?:information|info)\b',     # Vague information request
            r'\b(?:help|assist)\b'           # General help request
        ]
        
        # Context requirements for different concepts
        self.context_requirements = {
            'historical_concepts': ['when', 'where', 'time period', 'era'],
            'technical_concepts': ['how it works', 'technical details', 'specifications'],
            'comparative_concepts': ['compared to what', 'in what context', 'which aspect']
        }
        
        # Confidence thresholds
        self.ambiguity_threshold = 0.7  # Above this, we're confident it's ambiguous
        self.resolution_threshold = 0.6  # Above this, we're confident in resolution
    
    def detect_ambiguity(self, query: str, concepts: List[str], intent_result: Any) -> AmbiguityDetection:
        """
        Detect various types of ambiguity in the query
        
        Args:
            query: The original query string
            concepts: List of extracted concepts
            intent_result: Result from intent recognition
            
        Returns:
            AmbiguityDetection with details about detected ambiguity
        """
        ambiguous_elements = []
        ambiguity_types = []
        suggested_clarifications = []
        
        # Check for concept ambiguity
        concept_ambiguity = self._detect_concept_ambiguity(query, concepts)
        if concept_ambiguity['is_ambiguous']:
            ambiguous_elements.extend(concept_ambiguity['elements'])
            ambiguity_types.append(AmbiguityType.CONCEPT_AMBIGUITY)
            suggested_clarifications.extend(concept_ambiguity['clarifications'])
        
        # Check for intent ambiguity
        intent_ambiguity = self._detect_intent_ambiguity(query, intent_result)
        if intent_ambiguity['is_ambiguous']:
            ambiguous_elements.extend(intent_ambiguity['elements'])
            ambiguity_types.append(AmbiguityType.INTENT_AMBIGUITY)
            suggested_clarifications.extend(intent_ambiguity['clarifications'])
        
        # Check for context ambiguity
        context_ambiguity = self._detect_context_ambiguity(query, concepts)
        if context_ambiguity['is_ambiguous']:
            ambiguous_elements.extend(context_ambiguity['elements'])
            ambiguity_types.append(AmbiguityType.CONTEXT_AMBIGUITY)
            suggested_clarifications.extend(context_ambiguity['clarifications'])
        
        # Determine overall ambiguity
        is_ambiguous = len(ambiguity_types) > 0
        primary_ambiguity_type = ambiguity_types[0] if ambiguity_types else None
        
        # Calculate confidence in ambiguity detection
        confidence = self._calculate_ambiguity_confidence(ambiguous_elements, ambiguity_types)
        
        return AmbiguityDetection(
            is_ambiguous=is_ambiguous,
            ambiguity_type=primary_ambiguity_type,
            ambiguous_elements=list(set(ambiguous_elements)),
            confidence=confidence,
            suggested_clarifications=suggested_clarifications[:3]  # Limit to top 3
        )
    
    def resolve_ambiguity(self, query: str, ambiguity_detection: AmbiguityDetection, 
                         context: Optional[Dict] = None) -> DisambiguationResult:
        """
        Attempt to resolve detected ambiguity using context
        
        Args:
            query: The original query
            ambiguity_detection: Result from ambiguity detection
            context: Optional context including previous queries, user preferences
            
        Returns:
            DisambiguationResult with resolution attempt
        """
        if not ambiguity_detection.is_ambiguous:
            return DisambiguationResult(
                resolved=True,
                chosen_interpretation=None,
                confidence=1.0,
                fallback_interpretation=None,
                reasoning="No ambiguity detected"
            )
        
        # Try context-based resolution
        context_resolution = self._resolve_with_context(query, ambiguity_detection, context)
        if context_resolution['resolved']:
            return DisambiguationResult(
                resolved=True,
                chosen_interpretation=context_resolution['interpretation'],
                confidence=context_resolution['confidence'],
                fallback_interpretation=None,
                reasoning=context_resolution['reasoning']
            )
        
        # Fall back to most likely interpretation
        fallback_resolution = self._resolve_with_fallback(query, ambiguity_detection)
        
        return DisambiguationResult(
            resolved=False,  # Not fully resolved, using fallback
            chosen_interpretation=fallback_resolution['interpretation'],
            confidence=fallback_resolution['confidence'],
            fallback_interpretation=fallback_resolution['interpretation'],
            reasoning=fallback_resolution['reasoning']
        )
    
    def _detect_concept_ambiguity(self, query: str, concepts: List[str]) -> Dict[str, Any]:
        """Detect ambiguity in extracted concepts"""
        ambiguous_concepts = []
        clarifications = []
        
        query_lower = query.lower()
        
        for concept in concepts:
            if concept in self.ambiguous_concepts:
                # Check if context provides disambiguation
                meanings = self.ambiguous_concepts[concept]['meanings']
                context_scores = []
                
                for meaning in meanings:
                    score = sum(1 for keyword in meaning['keywords'] if keyword in query_lower)
                    context_scores.append(score)
                
                # If no clear winner, it's ambiguous
                max_score = max(context_scores) if context_scores else 0
                if max_score == 0 or context_scores.count(max_score) > 1:
                    ambiguous_concepts.append(concept)
                    
                    # Generate clarification
                    options = [meaning['interpretation'] for meaning in meanings]
                    clarification = f"Do you mean '{concept}' as {' or '.join(options)}?"
                    clarifications.append(clarification)
        
        return {
            'is_ambiguous': len(ambiguous_concepts) > 0,
            'elements': ambiguous_concepts,
            'clarifications': clarifications
        }
    
    def _detect_intent_ambiguity(self, query: str, intent_result: Any) -> Dict[str, Any]:
        """Detect ambiguity in user intent"""
        import re
        
        # Check if intent confidence is low or if there are competing intents
        is_ambiguous = False
        elements = []
        clarifications = []
        
        if hasattr(intent_result, 'is_ambiguous') and intent_result.is_ambiguous:
            is_ambiguous = True
            elements.append('user_intent')
            
            # Generate clarification based on alternative intents
            if hasattr(intent_result, 'alternative_intents') and intent_result.alternative_intents:
                top_alternatives = intent_result.alternative_intents[:2]
                intent_options = [intent for intent, _ in top_alternatives]
                clarification = f"Do you want to {intent_result.primary_intent} or {' or '.join(intent_options)}?"
                clarifications.append(clarification)
        
        # Check for vague intent indicators
        query_lower = query.lower()
        for pattern in self.intent_ambiguity_indicators:
            if re.search(pattern, query_lower):
                is_ambiguous = True
                elements.append('vague_request')
                clarifications.append("Could you be more specific about what you'd like to know?")
                break
        
        return {
            'is_ambiguous': is_ambiguous,
            'elements': elements,
            'clarifications': clarifications
        }
    
    def _detect_context_ambiguity(self, query: str, concepts: List[str]) -> Dict[str, Any]:
        """Detect missing context that could lead to ambiguity"""
        missing_context = []
        clarifications = []
        
        # Check if concepts require additional context
        for concept in concepts:
            if any(hist_word in concept.lower() for hist_word in ['historical', 'history', 'past']):
                if not any(ctx in query.lower() for ctx in self.context_requirements['historical_concepts']):
                    missing_context.append(f"{concept}_time_context")
                    clarifications.append(f"What time period are you interested in for {concept}?")
        
        return {
            'is_ambiguous': len(missing_context) > 0,
            'elements': missing_context,
            'clarifications': clarifications
        }
    
    def _calculate_ambiguity_confidence(self, elements: List[str], types: List[AmbiguityType]) -> float:
        """Calculate confidence in ambiguity detection"""
        base_confidence = 0.5
        
        # More ambiguous elements = higher confidence in ambiguity
        element_factor = min(len(elements) * 0.2, 0.3)
        
        # Multiple types of ambiguity = higher confidence
        type_factor = min(len(types) * 0.1, 0.2)
        
        return min(base_confidence + element_factor + type_factor, 1.0)
    
    def _resolve_with_context(self, query: str, ambiguity_detection: AmbiguityDetection, 
                            context: Optional[Dict]) -> Dict[str, Any]:
        """Attempt to resolve ambiguity using available context"""
        if not context:
            return {'resolved': False}
        
        # Use previous queries for context
        if 'previous_queries' in context and context['previous_queries']:
            # Simple heuristic: look for related concepts in previous queries
            prev_query_text = ' '.join(context['previous_queries'])
            
            for element in ambiguity_detection.ambiguous_elements:
                if element in self.ambiguous_concepts:
                    meanings = self.ambiguous_concepts[element]['meanings']
                    
                    for meaning in meanings:
                        context_score = sum(1 for keyword in meaning['keywords'] 
                                          if keyword in prev_query_text.lower())
                        if context_score > 0:
                            return {
                                'resolved': True,
                                'interpretation': meaning['interpretation'],
                                'confidence': min(0.7 + context_score * 0.1, 0.9),
                                'reasoning': f"Based on previous query context mentioning {meaning['keywords']}"
                            }
        
        return {'resolved': False}
    
    def _resolve_with_fallback(self, query: str, ambiguity_detection: AmbiguityDetection) -> Dict[str, Any]:
        """Provide fallback interpretation for ambiguous elements"""
        # Use most common interpretation as fallback
        for element in ambiguity_detection.ambiguous_elements:
            if element in self.ambiguous_concepts:
                default_interpretation = self.ambiguous_concepts[element]['default']
                return {
                    'interpretation': default_interpretation,
                    'confidence': 0.5,  # Low confidence since it's a fallback
                    'reasoning': f"Using most common interpretation of '{element}' as {default_interpretation}"
                }
        
        # Generic fallback
        return {
            'interpretation': 'general_interpretation',
            'confidence': 0.3,
            'reasoning': "Using general interpretation due to unresolved ambiguity"
        }
