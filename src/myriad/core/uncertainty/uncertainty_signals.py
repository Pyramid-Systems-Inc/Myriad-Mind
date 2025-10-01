"""
Uncertainty Signaling System for Myriad Cognitive Architecture
==========================================================

This module provides the uncertainty signaling mechanism that allows agents
to recognize and communicate their own uncertainty about interpretations,
knowledge, or relationships.

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Uncertainty Signaling)
Date: 2025-01-01
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json
import time

class UncertaintyType(Enum):
    """Types of uncertainty that can be signaled"""
    KNOWLEDGE_GAP = "knowledge_gap"  # Missing information
    CONFLICTING_INFO = "conflicting_info"  # Contradictory data
    LOW_CONFIDENCE = "low_confidence"  # Low confidence in interpretation
    AMBIGUOUS_CONCEPT = "ambiguous_concept"  # Multiple possible meanings
    INSUFFICIENT_CONTEXT = "insufficient_context"  # Missing context for proper interpretation
    TEMPORAL_UNCERTAINTY = "temporal_uncertainty"  # Uncertainty about timing or sequence
    CAUSAL_UNCERTAINTY = "causal_uncertainty"  # Uncertainty about cause-effect relationships

class UncertaintyLevel(Enum):
    """Levels of uncertainty"""
    VERY_LOW = 0.1    # Almost certain
    LOW = 0.3         # Fairly confident
    MEDIUM = 0.5      # Moderately uncertain
    HIGH = 0.7        # Quite uncertain
    VERY_HIGH = 0.9   # Very uncertain

@dataclass
class UncertaintySignal:
    """A single uncertainty signal"""
    uncertainty_type: UncertaintyType
    level: UncertaintyLevel
    description: str
    affected_elements: List[str]  # Concepts, relationships, or data affected
    suggested_clarifications: List[str]
    confidence_in_uncertainty: float  # How confident we are about this uncertainty
    timestamp: float
    source_agent: str

@dataclass
class UncertaintyAssessment:
    """Complete uncertainty assessment for a response"""
    overall_uncertainty: UncertaintyLevel
    uncertainty_signals: List[UncertaintySignal]
    recommended_action: str  # "proceed", "clarify", "research", "decline"
    confidence_in_assessment: float
    metadata: Dict[str, Any]

class UncertaintyDetector:
    """
    Detects various types of uncertainty in agent responses and knowledge
    
    This detector analyzes:
    - Knowledge gaps in agent responses
    - Conflicting information from multiple sources
    - Low confidence in interpretations
    - Ambiguous concepts or relationships
    """
    
    def __init__(self):
        """Initialize the uncertainty detector with thresholds and patterns"""
        
        # Uncertainty detection thresholds
        self.confidence_thresholds = {
            'high_confidence': 0.8,
            'medium_confidence': 0.6,
            'low_confidence': 0.4,
            'very_low_confidence': 0.2
        }
        
        # Patterns that indicate uncertainty
        self.uncertainty_indicators = {
            'knowledge_gap': [
                'no information available',
                'insufficient data',
                'cannot determine',
                'unknown',
                'unclear',
                'not specified'
            ],
            'conflicting_info': [
                'however',
                'on the other hand',
                'contradicts',
                'conflicts with',
                'disagrees with',
                'alternatively'
            ],
            'low_confidence': [
                'might be',
                'could be',
                'possibly',
                'perhaps',
                'likely',
                'probably'
            ]
        }
        
        # Concept ambiguity indicators
        self.ambiguous_concepts = {
            'drive': ['computer_storage', 'vehicle_operation', 'motivation'],
            'bank': ['financial_institution', 'river_bank'],
            'light': ['illumination', 'weight', 'color_shade'],
            'factory': ['manufacturing_facility', 'design_pattern']
        }
    
    def assess_uncertainty(self, response_data: Dict[str, Any], 
                          agent_name: str = "unknown") -> UncertaintyAssessment:
        """
        Assess uncertainty in an agent response
        
        Args:
            response_data: The response data from an agent
            agent_name: Name of the agent providing the response
            
        Returns:
            UncertaintyAssessment with detailed uncertainty analysis
        """
        uncertainty_signals = []
        
        # Check for knowledge gaps
        knowledge_gap_signals = self._detect_knowledge_gaps(response_data, agent_name)
        uncertainty_signals.extend(knowledge_gap_signals)
        
        # Check for conflicting information
        conflict_signals = self._detect_conflicting_information(response_data, agent_name)
        uncertainty_signals.extend(conflict_signals)
        
        # Check for low confidence indicators
        confidence_signals = self._detect_low_confidence(response_data, agent_name)
        uncertainty_signals.extend(confidence_signals)
        
        # Check for ambiguous concepts
        ambiguity_signals = self._detect_ambiguous_concepts(response_data, agent_name)
        uncertainty_signals.extend(ambiguity_signals)
        
        # Calculate overall uncertainty level
        overall_uncertainty = self._calculate_overall_uncertainty(uncertainty_signals)
        
        # Determine recommended action
        recommended_action = self._determine_recommended_action(overall_uncertainty, uncertainty_signals)
        
        # Calculate confidence in assessment
        confidence_in_assessment = self._calculate_assessment_confidence(uncertainty_signals)
        
        return UncertaintyAssessment(
            overall_uncertainty=overall_uncertainty,
            uncertainty_signals=uncertainty_signals,
            recommended_action=recommended_action,
            confidence_in_assessment=confidence_in_assessment,
            metadata={
                'assessment_timestamp': time.time(),
                'agent_name': agent_name,
                'signal_count': len(uncertainty_signals)
            }
        )
    
    def _detect_knowledge_gaps(self, response_data: Dict[str, Any], 
                             agent_name: str) -> List[UncertaintySignal]:
        """Detect knowledge gaps in the response"""
        signals = []
        
        # Extract text content from response
        text_content = self._extract_text_content(response_data)
        
        # Check for uncertainty indicators
        for indicator in self.uncertainty_indicators['knowledge_gap']:
            if indicator.lower() in text_content.lower():
                signals.append(UncertaintySignal(
                    uncertainty_type=UncertaintyType.KNOWLEDGE_GAP,
                    level=UncertaintyLevel.MEDIUM,
                    description=f"Knowledge gap detected: '{indicator}'",
                    affected_elements=self._extract_concepts_from_text(text_content),
                    suggested_clarifications=[
                        "Can you provide more specific information?",
                        "Is there additional context that would help?"
                    ],
                    confidence_in_uncertainty=0.7,
                    timestamp=time.time(),
                    source_agent=agent_name
                ))
        
        # Check for empty or minimal responses
        if len(text_content.strip()) < 20:
            signals.append(UncertaintySignal(
                uncertainty_type=UncertaintyType.KNOWLEDGE_GAP,
                level=UncertaintyLevel.HIGH,
                description="Minimal response suggests insufficient knowledge",
                affected_elements=[],
                suggested_clarifications=[
                    "Could you provide more details about this topic?",
                    "Is there a specific aspect you'd like me to focus on?"
                ],
                confidence_in_uncertainty=0.8,
                timestamp=time.time(),
                source_agent=agent_name
            ))
        
        return signals
    
    def _detect_conflicting_information(self, response_data: Dict[str, Any], 
                                      agent_name: str) -> List[UncertaintySignal]:
        """Detect conflicting information in the response"""
        signals = []
        
        # Extract text content from response
        text_content = self._extract_text_content(response_data)
        
        # Check for conflict indicators
        conflict_count = 0
        for indicator in self.uncertainty_indicators['conflicting_info']:
            conflict_count += text_content.lower().count(indicator.lower())
        
        if conflict_count > 0:
            signals.append(UncertaintySignal(
                uncertainty_type=UncertaintyType.CONFLICTING_INFO,
                level=UncertaintyLevel.MEDIUM if conflict_count == 1 else UncertaintyLevel.HIGH,
                description=f"Conflicting information detected ({conf_count} indicators)",
                affected_elements=self._extract_concepts_from_text(text_content),
                suggested_clarifications=[
                    "There seems to be conflicting information. Which perspective should I prioritize?",
                    "Can you help resolve the apparent contradictions?"
                ],
                confidence_in_uncertainty=0.6 + (conflict_count * 0.1),
                timestamp=time.time(),
                source_agent=agent_name
            ))
        
        return signals
    
    def _detect_low_confidence(self, response_data: Dict[str, Any], 
                             agent_name: str) -> List[UncertaintySignal]:
        """Detect low confidence indicators in the response"""
        signals = []
        
        # Check explicit confidence score if available
        if 'confidence' in response_data:
            confidence = response_data['confidence']
            if confidence < self.confidence_thresholds['low_confidence']:
                signals.append(UncertaintySignal(
                    uncertainty_type=UncertaintyType.LOW_CONFIDENCE,
                    level=UncertaintyLevel.HIGH if confidence < self.confidence_thresholds['very_low_confidence'] else UncertaintyLevel.MEDIUM,
                    description=f"Low confidence score: {confidence}",
                    affected_elements=self._extract_concepts_from_data(response_data),
                    suggested_clarifications=[
                        "I'm not confident about this information. Can you provide additional context?",
                        "Would you like me to research this topic further?"
                    ],
                    confidence_in_uncertainty=0.8,
                    timestamp=time.time(),
                    source_agent=agent_name
                ))
        
        # Check for confidence indicators in text
        text_content = self._extract_text_content(response_data)
        confidence_indicators = 0
        for indicator in self.uncertainty_indicators['low_confidence']:
            confidence_indicators += text_content.lower().count(indicator.lower())
        
        if confidence_indicators > 0:
            signals.append(UncertaintySignal(
                uncertainty_type=UncertaintyType.LOW_CONFIDENCE,
                level=UncertaintyLevel.MEDIUM,
                description=f"Low confidence indicators detected ({confidence_indicators} instances)",
                affected_elements=self._extract_concepts_from_text(text_content),
                suggested_clarifications=[
                    "I'm not entirely certain about this. Can you provide more specific information?",
                    "Would you like me to seek additional sources?"
                ],
                confidence_in_uncertainty=0.6,
                timestamp=time.time(),
                source_agent=agent_name
            ))
        
        return signals
    
    def _detect_ambiguous_concepts(self, response_data: Dict[str, Any], 
                                 agent_name: str) -> List[UncertaintySignal]:
        """Detect ambiguous concepts in the response"""
        signals = []
        
        # Extract concepts from response
        concepts = self._extract_concepts_from_data(response_data)
        
        # Check against known ambiguous concepts
        for concept in concepts:
            if concept.lower() in self.ambiguous_concepts:
                possible_meanings = self.ambiguous_concepts[concept.lower()]
                if len(possible_meanings) > 1:
                    signals.append(UncertaintySignal(
                        uncertainty_type=UncertaintyType.AMBIGUOUS_CONCEPT,
                        level=UncertaintyLevel.MEDIUM,
                        description=f"Ambiguous concept '{concept}' with {len(possible_meanings)} possible meanings",
                        affected_elements=[concept],
                        suggested_clarifications=[
                            f"When you mention '{concept}', do you mean:",
                            *[f"  {i+1}. {meaning}" for i, meaning in enumerate(possible_meanings)]
                        ],
                        confidence_in_uncertainty=0.7,
                        timestamp=time.time(),
                        source_agent=agent_name
                    ))
        
        return signals
    
    def _extract_text_content(self, data: Any) -> str:
        """Extract text content from response data"""
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            # Look for common text fields
            for field in ['response', 'data', 'content', 'text', 'message']:
                if field in data and isinstance(data[field], str):
                    return data[field]
            # If no direct text field, convert dict to string
            return json.dumps(data)
        elif isinstance(data, list):
            return " ".join(str(item) for item in data)
        else:
            return str(data)
    
    def _extract_concepts_from_text(self, text: str) -> List[str]:
        """Extract concepts from text content"""
        # Simple concept extraction - could be enhanced with NLP
        import re
        
        # Extract quoted terms
        quoted_terms = re.findall(r'"([^"]+)"', text)
        
        # Extract capitalized terms (potential concepts)
        capitalized_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Combine and deduplicate
        all_concepts = list(set(quoted_terms + capitalized_terms))
        
        # Filter out common words
        common_words = {'The', 'This', 'That', 'These', 'Those', 'When', 'Where', 'What', 'How', 'Why'}
        return [concept for concept in all_concepts if concept not in common_words and len(concept) > 2]
    
    def _extract_concepts_from_data(self, data: Any) -> List[str]:
        """Extract concepts from response data"""
        if isinstance(data, dict):
            concepts = []
            # Look for concept fields
            for field in ['concepts', 'entities', 'topics', 'subjects']:
                if field in data:
                    if isinstance(data[field], list):
                        concepts.extend(data[field])
                    elif isinstance(data[field], str):
                        concepts.append(data[field])
            
            # If no explicit concepts, extract from text
            if not concepts:
                text_content = self._extract_text_content(data)
                concepts = self._extract_concepts_from_text(text_content)
            
            return concepts
        else:
            return self._extract_concepts_from_text(str(data))
    
    def _calculate_overall_uncertainty(self, signals: List[UncertaintySignal]) -> UncertaintyLevel:
        """Calculate overall uncertainty level from individual signals"""
        if not signals:
            return UncertaintyLevel.VERY_LOW
        
        # Calculate weighted average of signal levels
        total_weight = 0
        weighted_sum = 0
        
        for signal in signals:
            weight = signal.confidence_in_uncertainty
            level_value = signal.level.value
            weighted_sum += level_value * weight
            total_weight += weight
        
        if total_weight == 0:
            return UncertaintyLevel.VERY_LOW
        
        average_level = weighted_sum / total_weight
        
        # Convert back to enum
        if average_level < 0.2:
            return UncertaintyLevel.VERY_LOW
        elif average_level < 0.4:
            return UncertaintyLevel.LOW
        elif average_level < 0.6:
            return UncertaintyLevel.MEDIUM
        elif average_level < 0.8:
            return UncertaintyLevel.HIGH
        else:
            return UncertaintyLevel.VERY_HIGH
    
    def _determine_recommended_action(self, overall_uncertainty: UncertaintyLevel, 
                                    signals: List[UncertaintySignal]) -> str:
        """Determine recommended action based on uncertainty assessment"""
        if overall_uncertainty == UncertaintyLevel.VERY_LOW:
            return "proceed"
        elif overall_uncertainty == UncertaintyLevel.LOW:
            return "proceed"
        elif overall_uncertainty == UncertaintyLevel.MEDIUM:
            # Check if we have specific clarification suggestions
            has_clarifications = any(signal.suggested_clarifications for signal in signals)
            return "clarify" if has_clarifications else "proceed"
        elif overall_uncertainty == UncertaintyLevel.HIGH:
            # Check for knowledge gaps vs other uncertainty types
            has_knowledge_gaps = any(signal.uncertainty_type == UncertaintyType.KNOWLEDGE_GAP for signal in signals)
            return "research" if has_knowledge_gaps else "clarify"
        else:  # VERY_HIGH
            return "decline"
    
    def _calculate_assessment_confidence(self, signals: List[UncertaintySignal]) -> float:
        """Calculate confidence in the uncertainty assessment"""
        if not signals:
            return 0.5  # Neutral confidence when no signals
        
        # Base confidence on number and strength of signals
        signal_count = len(signals)
        avg_confidence = sum(signal.confidence_in_uncertainty for signal in signals) / signal_count
        
        # Adjust based on signal count (more signals = higher confidence)
        count_factor = min(signal_count / 5.0, 1.0)  # Cap at 5 signals
        
        return (avg_confidence * 0.7) + (count_factor * 0.3)


# Global uncertainty detector instance
uncertainty_detector = UncertaintyDetector()


def get_uncertainty_detector() -> UncertaintyDetector:
    """Get the global uncertainty detector instance"""
    return uncertainty_detector