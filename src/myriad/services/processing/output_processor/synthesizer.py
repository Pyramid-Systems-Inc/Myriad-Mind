"""
Advanced Synthesizer for the Enhanced Output Processor
Implements Task 3.2.1: Advanced Synthesizer for structured data processing

This module processes synthesis_request with weighted agent contributions,
handles multi-agent response correlation and confidence weighting, and
supports causal chain emphasis per PROTOCOLS.md.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SynthesisStrategy(Enum):
    """Different synthesis strategies for combining agent responses"""
    WEIGHTED_AVERAGE = "weighted_average"
    CONFIDENCE_BASED = "confidence_based"
    CAUSAL_CHAIN = "causal_chain"
    HIERARCHICAL = "hierarchical"
    COMPARATIVE = "comparative"

@dataclass
class AgentResponse:
    """Structured representation of an agent response"""
    agent_id: str
    task_id: str
    content: str
    confidence: float
    contribution_weight: float
    response_type: str = "text"
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class SynthesisParameters:
    """Parameters controlling the synthesis process"""
    output_format: str = "explanatory_paragraph"
    target_length: str = "medium"
    evidence_level: str = "standard"
    causal_chain_emphasis: bool = False
    confidence_threshold: float = 0.5
    max_agents_to_cite: int = 5

@dataclass
class SynthesisResult:
    """Result of the synthesis process"""
    synthesized_content: str
    confidence_score: float
    evidence_sources: List[str]
    synthesis_metadata: Dict[str, Any]
    warnings: List[str] = None

class AdvancedSynthesizer:
    """
    Advanced Synthesizer for combining multi-agent responses
    
    Features:
    - Weighted agent contribution processing
    - Multi-agent response correlation and confidence weighting
    - Causal chain emphasis and evidence level configuration
    - Support for different synthesis strategies
    - Confidence-based filtering and validation
    """
    
    def __init__(self):
        """Initialize the synthesizer with configuration"""
        
        # Synthesis strategy mappings
        self.strategy_mappings = {
            "explain_importance": SynthesisStrategy.CAUSAL_CHAIN,
            "define": SynthesisStrategy.WEIGHTED_AVERAGE,
            "compare": SynthesisStrategy.COMPARATIVE,
            "analyze_historical_context": SynthesisStrategy.HIERARCHICAL,
            "calculate": SynthesisStrategy.CONFIDENCE_BASED,
            "summarize": SynthesisStrategy.HIERARCHICAL
        }
        
        # Content correlation patterns
        self.correlation_patterns = {
            'reinforcement': [
                r'\b(?:also|additionally|furthermore|moreover)\b',
                r'\b(?:confirms?|supports?|validates?)\b'
            ],
            'contradiction': [
                r'\b(?:however|but|although|despite)\b',
                r'\b(?:contradicts?|opposes?|differs?)\b'
            ],
            'causation': [
                r'\b(?:because|due to|caused by|resulted in)\b',
                r'\b(?:therefore|thus|consequently|hence)\b'
            ],
            'temporal': [
                r'\b(?:before|after|during|when|while)\b',
                r'\b(?:first|then|next|finally)\b'
            ]
        }
        
        # Evidence strength indicators
        self.evidence_indicators = {
            'strong': ['proven', 'demonstrated', 'established', 'confirmed'],
            'moderate': ['suggests', 'indicates', 'implies', 'appears'],
            'weak': ['possibly', 'might', 'could', 'perhaps']
        }
    
    def synthesize_responses(self, agent_responses: Dict[str, Dict], 
                           synthesis_parameters: SynthesisParameters,
                           query_metadata: Dict[str, Any]) -> SynthesisResult:
        """
        Synthesize multiple agent responses into a coherent result
        
        Args:
            agent_responses: Dictionary of agent responses with task IDs as keys
            synthesis_parameters: Parameters controlling synthesis behavior
            query_metadata: Metadata about the original query
            
        Returns:
            SynthesisResult with synthesized content and metadata
        """
        # Convert to structured format
        structured_responses = self._structure_responses(agent_responses)
        
        # Filter by confidence threshold
        filtered_responses = self._filter_by_confidence(
            structured_responses, synthesis_parameters.confidence_threshold
        )
        
        if not filtered_responses:
            return SynthesisResult(
                synthesized_content="Unable to synthesize response - insufficient confident data.",
                confidence_score=0.0,
                evidence_sources=[],
                synthesis_metadata={"error": "no_confident_responses"},
                warnings=["All agent responses below confidence threshold"]
            )
        
        # Determine synthesis strategy
        synthesis_intent = query_metadata.get('synthesis_intent', 'explain_importance')
        strategy = self.strategy_mappings.get(synthesis_intent, SynthesisStrategy.WEIGHTED_AVERAGE)
        
        # Analyze response correlations
        correlations = self._analyze_correlations(filtered_responses)
        
        # Apply synthesis strategy
        synthesized_content = self._apply_synthesis_strategy(
            filtered_responses, strategy, synthesis_parameters, correlations
        )
        
        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(
            filtered_responses, correlations
        )
        
        # Extract evidence sources
        evidence_sources = self._extract_evidence_sources(filtered_responses)
        
        # Generate metadata
        synthesis_metadata = self._generate_synthesis_metadata(
            filtered_responses, strategy, correlations, synthesis_parameters
        )
        
        # Check for warnings
        warnings = self._generate_warnings(filtered_responses, correlations)
        
        return SynthesisResult(
            synthesized_content=synthesized_content,
            confidence_score=overall_confidence,
            evidence_sources=evidence_sources,
            synthesis_metadata=synthesis_metadata,
            warnings=warnings
        )
    
    def _structure_responses(self, agent_responses: Dict[str, Dict]) -> List[AgentResponse]:
        """Convert raw agent responses to structured format"""
        structured = []
        
        for task_id, response_data in agent_responses.items():
            # Handle both basic and enhanced response formats
            if 'agent_id' in response_data:
                # Enhanced format
                structured_response = AgentResponse(
                    agent_id=response_data['agent_id'],
                    task_id=task_id,
                    content=response_data.get('content', ''),
                    confidence=response_data.get('confidence', 0.8),
                    contribution_weight=response_data.get('contribution_weight', 1.0),
                    response_type=response_data.get('response_type', 'text'),
                    metadata=response_data.get('metadata', {})
                )
            else:
                # Basic format (current system)
                structured_response = AgentResponse(
                    agent_id=response_data.get('agent_name', 'unknown_agent'),
                    task_id=task_id,
                    content=response_data.get('data', ''),
                    confidence=0.8,  # Default confidence for basic format
                    contribution_weight=1.0,  # Equal weight for basic format
                    response_type='text',
                    metadata={'status': response_data.get('status', 'unknown')}
                )
            
            structured.append(structured_response)
        
        return structured
    
    def _filter_by_confidence(self, responses: List[AgentResponse], 
                            threshold: float) -> List[AgentResponse]:
        """Filter responses by confidence threshold"""
        return [r for r in responses if r.confidence >= threshold]
    
    def _analyze_correlations(self, responses: List[AgentResponse]) -> Dict[str, Any]:
        """Analyze correlations and relationships between responses"""
        correlations = {
            'reinforcement_pairs': [],
            'contradiction_pairs': [],
            'causal_chains': [],
            'temporal_sequences': [],
            'content_overlap': {}
        }
        
        # Analyze pairwise correlations
        for i, resp1 in enumerate(responses):
            for j, resp2 in enumerate(responses[i+1:], i+1):
                correlation = self._analyze_response_pair(resp1, resp2)
                
                if correlation['type'] == 'reinforcement':
                    correlations['reinforcement_pairs'].append((i, j, correlation['strength']))
                elif correlation['type'] == 'contradiction':
                    correlations['contradiction_pairs'].append((i, j, correlation['strength']))
                elif correlation['type'] == 'causation':
                    correlations['causal_chains'].append((i, j, correlation['direction']))
                elif correlation['type'] == 'temporal':
                    correlations['temporal_sequences'].append((i, j, correlation['order']))
                
                # Calculate content overlap
                overlap = self._calculate_content_overlap(resp1.content, resp2.content)
                correlations['content_overlap'][(i, j)] = overlap
        
        return correlations
    
    def _analyze_response_pair(self, resp1: AgentResponse, resp2: AgentResponse) -> Dict[str, Any]:
        """Analyze the relationship between two responses"""
        content1 = resp1.content.lower()
        content2 = resp2.content.lower()
        
        # Check for different correlation types
        for corr_type, patterns in self.correlation_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content1) or re.search(pattern, content2):
                    strength = self._calculate_correlation_strength(content1, content2, pattern)
                    return {
                        'type': corr_type,
                        'strength': strength,
                        'pattern': pattern
                    }
        
        # Default to neutral if no specific pattern found
        return {'type': 'neutral', 'strength': 0.0}
    
    def _calculate_correlation_strength(self, content1: str, content2: str, pattern: str) -> float:
        """Calculate the strength of correlation between two pieces of content"""
        # Simple heuristic based on pattern frequency and content similarity
        pattern_count = len(re.findall(pattern, content1 + " " + content2))
        content_similarity = self._calculate_content_overlap(content1, content2)
        
        return min((pattern_count * 0.3) + (content_similarity * 0.7), 1.0)
    
    def _calculate_content_overlap(self, content1: str, content2: str) -> float:
        """Calculate content overlap between two responses"""
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _apply_synthesis_strategy(self, responses: List[AgentResponse], 
                                strategy: SynthesisStrategy,
                                parameters: SynthesisParameters,
                                correlations: Dict[str, Any]) -> str:
        """Apply the selected synthesis strategy"""
        
        if strategy == SynthesisStrategy.CAUSAL_CHAIN:
            return self._synthesize_causal_chain(responses, parameters, correlations)
        elif strategy == SynthesisStrategy.COMPARATIVE:
            return self._synthesize_comparative(responses, parameters, correlations)
        elif strategy == SynthesisStrategy.HIERARCHICAL:
            return self._synthesize_hierarchical(responses, parameters, correlations)
        elif strategy == SynthesisStrategy.CONFIDENCE_BASED:
            return self._synthesize_confidence_based(responses, parameters)
        else:  # WEIGHTED_AVERAGE
            return self._synthesize_weighted_average(responses, parameters)
    
    def _synthesize_causal_chain(self, responses: List[AgentResponse], 
                               parameters: SynthesisParameters,
                               correlations: Dict[str, Any]) -> str:
        """Synthesize responses emphasizing causal relationships"""
        # Sort responses by causal importance
        causal_chains = correlations.get('causal_chains', [])
        
        # Build causal narrative
        synthesis = []
        
        # Start with foundational facts
        fact_responses = [r for r in responses if 'define' in r.agent_id.lower() or 'fact' in r.agent_id.lower()]
        if fact_responses:
            synthesis.append(f"To understand this relationship, {fact_responses[0].content}")
        
        # Add causal connections
        for i, j, direction in causal_chains:
            if direction == 'forward':
                synthesis.append(f"This led to {responses[j].content}")
            else:
                synthesis.append(f"As a result, {responses[i].content}")
        
        # Add supporting evidence
        remaining_responses = [r for r in responses if r not in fact_responses]
        for response in remaining_responses[:2]:  # Limit to avoid verbosity
            synthesis.append(f"Furthermore, {response.content}")
        
        return " ".join(synthesis)
    
    def _synthesize_weighted_average(self, responses: List[AgentResponse], 
                                   parameters: SynthesisParameters) -> str:
        """Synthesize using weighted average approach"""
        # Sort by contribution weight and confidence
        weighted_responses = sorted(responses, 
                                  key=lambda r: r.contribution_weight * r.confidence, 
                                  reverse=True)
        
        synthesis_parts = []
        total_weight = sum(r.contribution_weight for r in weighted_responses)
        
        for response in weighted_responses:
            weight_ratio = response.contribution_weight / total_weight
            if weight_ratio > 0.1:  # Only include significant contributions
                synthesis_parts.append(response.content)
        
        return " ".join(synthesis_parts)
    
    def _synthesize_comparative(self, responses: List[AgentResponse], 
                              parameters: SynthesisParameters,
                              correlations: Dict[str, Any]) -> str:
        """Synthesize responses for comparative analysis"""
        synthesis = []
        
        # Group responses by similarity
        reinforcement_pairs = correlations.get('reinforcement_pairs', [])
        contradiction_pairs = correlations.get('contradiction_pairs', [])
        
        # Present similarities first
        if reinforcement_pairs:
            synthesis.append("Several sources agree that:")
            for i, j, strength in reinforcement_pairs[:2]:
                synthesis.append(f"- {responses[i].content}")
        
        # Present differences
        if contradiction_pairs:
            synthesis.append("However, there are different perspectives:")
            for i, j, strength in contradiction_pairs[:2]:
                synthesis.append(f"- While {responses[i].content}, {responses[j].content}")
        
        return " ".join(synthesis)
    
    def _synthesize_hierarchical(self, responses: List[AgentResponse], 
                               parameters: SynthesisParameters,
                               correlations: Dict[str, Any]) -> str:
        """Synthesize responses in hierarchical order"""
        # Sort by confidence and importance
        sorted_responses = sorted(responses, 
                                key=lambda r: (r.confidence, r.contribution_weight), 
                                reverse=True)
        
        synthesis = []
        
        # Main point from highest confidence response
        if sorted_responses:
            synthesis.append(f"The primary finding is that {sorted_responses[0].content}")
        
        # Supporting points
        for response in sorted_responses[1:3]:
            synthesis.append(f"Additionally, {response.content}")
        
        return " ".join(synthesis)
    
    def _synthesize_confidence_based(self, responses: List[AgentResponse], 
                                   parameters: SynthesisParameters) -> str:
        """Synthesize based purely on confidence levels"""
        high_confidence = [r for r in responses if r.confidence > 0.8]
        medium_confidence = [r for r in responses if 0.6 <= r.confidence <= 0.8]
        
        synthesis = []
        
        if high_confidence:
            synthesis.append(f"With high confidence: {high_confidence[0].content}")
        
        if medium_confidence:
            synthesis.append(f"With moderate confidence: {medium_confidence[0].content}")
        
        return " ".join(synthesis)
    
    def _calculate_overall_confidence(self, responses: List[AgentResponse], 
                                    correlations: Dict[str, Any]) -> float:
        """Calculate overall confidence in the synthesized result"""
        if not responses:
            return 0.0
        
        # Base confidence from weighted average
        total_weight = sum(r.contribution_weight for r in responses)
        weighted_confidence = sum(r.confidence * r.contribution_weight for r in responses) / total_weight
        
        # Boost confidence for reinforcing responses
        reinforcement_boost = len(correlations.get('reinforcement_pairs', [])) * 0.05
        
        # Reduce confidence for contradictions
        contradiction_penalty = len(correlations.get('contradiction_pairs', [])) * 0.1
        
        final_confidence = weighted_confidence + reinforcement_boost - contradiction_penalty
        return max(0.0, min(1.0, final_confidence))
    
    def _extract_evidence_sources(self, responses: List[AgentResponse]) -> List[str]:
        """Extract evidence sources from responses"""
        sources = []
        for response in responses:
            if response.confidence > 0.7:  # Only include high-confidence sources
                sources.append(response.agent_id)
        return list(set(sources))  # Remove duplicates
    
    def _generate_synthesis_metadata(self, responses: List[AgentResponse], 
                                   strategy: SynthesisStrategy,
                                   correlations: Dict[str, Any],
                                   parameters: SynthesisParameters) -> Dict[str, Any]:
        """Generate metadata about the synthesis process"""
        return {
            'synthesis_strategy': strategy.value,
            'total_responses': len(responses),
            'avg_confidence': sum(r.confidence for r in responses) / len(responses),
            'reinforcement_pairs': len(correlations.get('reinforcement_pairs', [])),
            'contradiction_pairs': len(correlations.get('contradiction_pairs', [])),
            'causal_chains': len(correlations.get('causal_chains', [])),
            'synthesis_parameters': {
                'output_format': parameters.output_format,
                'target_length': parameters.target_length,
                'evidence_level': parameters.evidence_level
            }
        }
    
    def _generate_warnings(self, responses: List[AgentResponse], 
                         correlations: Dict[str, Any]) -> List[str]:
        """Generate warnings about potential issues in synthesis"""
        warnings = []
        
        # Check for low confidence responses
        low_confidence = [r for r in responses if r.confidence < 0.6]
        if low_confidence:
            warnings.append(f"{len(low_confidence)} responses have low confidence")
        
        # Check for contradictions
        contradictions = correlations.get('contradiction_pairs', [])
        if contradictions:
            warnings.append(f"{len(contradictions)} contradictory response pairs detected")
        
        # Check for insufficient data
        if len(responses) < 2:
            warnings.append("Synthesis based on limited data - single response")
        
        return warnings
