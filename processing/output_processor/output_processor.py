"""
Enhanced Output Processor - The "Motor Cortex"
Implements Task 3.2.3: Protocol Message Processing

This is the main Output Processor that consumes "Orchestrator-to-OutputProcessor 
(Collected Results)" messages, parses agent_responses with confidence weights,
applies synthesis_parameters, and generates coherent final responses with proper citation.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

from .synthesizer import AdvancedSynthesizer, SynthesisParameters, SynthesisResult
from .formatter import MultiFormatFormatter, FormattingParameters, FormattedResponse, OutputFormat, TargetLength, EvidenceLevel

@dataclass
class CollectedResults:
    """Structured representation of collected results from Orchestrator"""
    query_id: str
    collected_results: Dict[str, Dict[str, Any]]
    query_metadata: Optional[Dict[str, Any]] = None

@dataclass
class SynthesisRequest:
    """Enhanced synthesis request per PROTOCOLS.md"""
    query_metadata: Dict[str, Any]
    agent_responses: Dict[str, Dict[str, Any]]
    synthesis_parameters: Dict[str, Any]

@dataclass
class FinalResponse:
    """Final response from the Output Processor"""
    response_id: str
    query_id: str
    final_content: str
    confidence_score: float
    response_metadata: Dict[str, Any]
    processing_time_ms: int
    status: str = "success"

class EnhancedOutputProcessor:
    """
    Enhanced Output Processor implementing the complete "Motor Cortex" functionality
    
    This processor:
    1. Consumes "Orchestrator-to-OutputProcessor (Collected Results)" messages
    2. Parses agent_responses with individual confidence and contribution weights
    3. Applies synthesis_parameters for customized output generation
    4. Generates coherent final responses with proper citation and confidence metrics
    5. Supports both basic and enhanced protocol formats
    """
    
    def __init__(self):
        """Initialize the Enhanced Output Processor with components"""
        self.synthesizer = AdvancedSynthesizer()
        self.formatter = MultiFormatFormatter()
        
        # Default parameters
        self.default_synthesis_params = SynthesisParameters(
            output_format="explanatory_paragraph",
            target_length="standard",
            evidence_level="standard",
            causal_chain_emphasis=False,
            confidence_threshold=0.5,
            max_agents_to_cite=5
        )
        
        self.default_formatting_params = FormattingParameters(
            output_format=OutputFormat.EXPLANATORY_PARAGRAPH,
            target_length=TargetLength.STANDARD,
            evidence_level=EvidenceLevel.STANDARD,
            include_confidence=True,
            include_warnings=True
        )
    
    def process_collected_results(self, collected_results: Dict[str, Any]) -> FinalResponse:
        """
        Process basic collected results format from current Orchestrator
        
        Args:
            collected_results: Basic format with query_id and collected_results
            
        Returns:
            FinalResponse with synthesized and formatted content
        """
        start_time = datetime.now()
        
        # Convert basic format to structured format
        structured_results = CollectedResults(
            query_id=collected_results.get('query_id', f'unknown_{uuid.uuid4().hex[:8]}'),
            collected_results=collected_results.get('collected_results', {}),
            query_metadata={}
        )
        
        # Use default parameters for basic processing
        synthesis_params = self.default_synthesis_params
        formatting_params = self.default_formatting_params
        
        # Process through synthesis and formatting pipeline
        final_response = self._process_pipeline(
            structured_results, synthesis_params, formatting_params, start_time
        )
        
        return final_response
    
    def process_synthesis_request(self, synthesis_request: Dict[str, Any]) -> FinalResponse:
        """
        Process enhanced synthesis request per PROTOCOLS.md
        
        Args:
            synthesis_request: Enhanced format with full synthesis parameters
            
        Returns:
            FinalResponse with synthesized and formatted content
        """
        start_time = datetime.now()
        
        # Extract components from synthesis request
        query_metadata = synthesis_request.get('query_metadata', {})
        agent_responses = synthesis_request.get('agent_responses', {})
        synthesis_params_dict = synthesis_request.get('synthesis_parameters', {})
        
        # Convert to structured format
        structured_results = CollectedResults(
            query_id=query_metadata.get('query_id', f'enhanced_{uuid.uuid4().hex[:8]}'),
            collected_results=agent_responses,
            query_metadata=query_metadata
        )
        
        # Parse synthesis parameters
        synthesis_params = self._parse_synthesis_parameters(synthesis_params_dict)
        formatting_params = self._parse_formatting_parameters(synthesis_params_dict)
        
        # Process through synthesis and formatting pipeline
        final_response = self._process_pipeline(
            structured_results, synthesis_params, formatting_params, start_time
        )
        
        return final_response
    
    def _process_pipeline(self, structured_results: CollectedResults,
                         synthesis_params: SynthesisParameters,
                         formatting_params: FormattingParameters,
                         start_time: datetime) -> FinalResponse:
        """Process through the complete synthesis and formatting pipeline"""
        
        # Step 1: Synthesize agent responses
        synthesis_result = self.synthesizer.synthesize_responses(
            agent_responses=structured_results.collected_results,
            synthesis_parameters=synthesis_params,
            query_metadata=structured_results.query_metadata or {}
        )
        
        # Step 2: Format the synthesized content
        formatted_response = self.formatter.format_response(
            synthesized_content=synthesis_result.synthesized_content,
            evidence_sources=synthesis_result.evidence_sources,
            confidence_score=synthesis_result.confidence_score,
            synthesis_metadata=synthesis_result.synthesis_metadata,
            formatting_parameters=formatting_params,
            warnings=synthesis_result.warnings
        )
        
        # Step 3: Create final response
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        response_metadata = self._create_response_metadata(
            synthesis_result, formatted_response, synthesis_params, formatting_params
        )
        
        final_response = FinalResponse(
            response_id=f"resp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}",
            query_id=structured_results.query_id,
            final_content=formatted_response.content,
            confidence_score=synthesis_result.confidence_score,
            response_metadata=response_metadata,
            processing_time_ms=processing_time,
            status="success"
        )
        
        return final_response
    
    def _parse_synthesis_parameters(self, params_dict: Dict[str, Any]) -> SynthesisParameters:
        """Parse synthesis parameters from dictionary"""
        return SynthesisParameters(
            output_format=params_dict.get('output_format', 'explanatory_paragraph'),
            target_length=params_dict.get('target_length', 'standard'),
            evidence_level=params_dict.get('evidence_level', 'standard'),
            causal_chain_emphasis=params_dict.get('causal_chain_emphasis', False),
            confidence_threshold=params_dict.get('confidence_threshold', 0.5),
            max_agents_to_cite=params_dict.get('max_agents_to_cite', 5)
        )
    
    def _parse_formatting_parameters(self, params_dict: Dict[str, Any]) -> FormattingParameters:
        """Parse formatting parameters from dictionary"""
        # Map string values to enums
        output_format_map = {
            'explanatory_paragraph': OutputFormat.EXPLANATORY_PARAGRAPH,
            'structured_list': OutputFormat.STRUCTURED_LIST,
            'comparative_analysis': OutputFormat.COMPARATIVE_ANALYSIS,
            'technical_summary': OutputFormat.TECHNICAL_SUMMARY,
            'narrative': OutputFormat.NARRATIVE
        }
        
        target_length_map = {
            'brief': TargetLength.BRIEF,
            'standard': TargetLength.STANDARD,
            'detailed': TargetLength.DETAILED
        }
        
        evidence_level_map = {
            'minimal': EvidenceLevel.MINIMAL,
            'standard': EvidenceLevel.STANDARD,
            'detailed': EvidenceLevel.DETAILED,
            'academic': EvidenceLevel.ACADEMIC
        }
        
        return FormattingParameters(
            output_format=output_format_map.get(
                params_dict.get('output_format', 'explanatory_paragraph'),
                OutputFormat.EXPLANATORY_PARAGRAPH
            ),
            target_length=target_length_map.get(
                params_dict.get('target_length', 'standard'),
                TargetLength.STANDARD
            ),
            evidence_level=evidence_level_map.get(
                params_dict.get('evidence_level', 'standard'),
                EvidenceLevel.STANDARD
            ),
            include_confidence=params_dict.get('include_confidence', True),
            include_warnings=params_dict.get('include_warnings', True)
        )
    
    def _create_response_metadata(self, synthesis_result: SynthesisResult,
                                formatted_response: FormattedResponse,
                                synthesis_params: SynthesisParameters,
                                formatting_params: FormattingParameters) -> Dict[str, Any]:
        """Create comprehensive response metadata"""
        return {
            'processor_info': {
                'processor_name': 'Enhanced_Output_Processor',
                'processor_version': '1.0.0',
                'processing_timestamp': datetime.now().isoformat()
            },
            'synthesis_info': {
                'synthesis_metadata': synthesis_result.synthesis_metadata,
                'synthesis_parameters': asdict(synthesis_params),
                'warnings': synthesis_result.warnings or []
            },
            'formatting_info': {
                'formatting_metadata': formatted_response.metadata,
                'formatting_parameters': {
                    'output_format': formatting_params.output_format.value,
                    'target_length': formatting_params.target_length.value,
                    'evidence_level': formatting_params.evidence_level.value
                },
                'final_word_count': formatted_response.word_count,
                'citations': formatted_response.citations
            },
            'quality_metrics': {
                'confidence_score': synthesis_result.confidence_score,
                'evidence_sources_count': len(synthesis_result.evidence_sources),
                'response_completeness': self._assess_completeness(formatted_response),
                'coherence_score': self._assess_coherence(formatted_response)
            }
        }
    
    def _assess_completeness(self, formatted_response: FormattedResponse) -> float:
        """Assess the completeness of the response"""
        # Simple heuristic based on word count and citations
        word_count = formatted_response.word_count
        citation_count = len(formatted_response.citations)
        
        # Base score from word count (assuming 100+ words is complete)
        word_score = min(word_count / 100.0, 1.0)
        
        # Boost for having citations
        citation_boost = min(citation_count * 0.1, 0.3)
        
        return min(word_score + citation_boost, 1.0)
    
    def _assess_coherence(self, formatted_response: FormattedResponse) -> float:
        """Assess the coherence of the response"""
        content = formatted_response.content
        
        # Simple coherence metrics
        sentences = len([s for s in content.split('.') if len(s.strip()) > 5])
        words = len(content.split())
        
        if sentences == 0:
            return 0.0
        
        # Average sentence length (coherent responses have reasonable sentence length)
        avg_sentence_length = words / sentences
        
        # Optimal range is 10-25 words per sentence
        if 10 <= avg_sentence_length <= 25:
            length_score = 1.0
        elif avg_sentence_length < 10:
            length_score = avg_sentence_length / 10.0
        else:
            length_score = max(0.5, 25.0 / avg_sentence_length)
        
        # Check for transition words (indicates good flow)
        transition_words = ['however', 'therefore', 'furthermore', 'additionally', 'moreover']
        transition_count = sum(1 for word in transition_words if word in content.lower())
        transition_score = min(transition_count * 0.2, 0.5)
        
        return min(length_score + transition_score, 1.0)
    
    def to_basic_response_format(self, final_response: FinalResponse) -> Dict[str, Any]:
        """
        Convert final response to basic format for backward compatibility
        
        This maintains compatibility with systems expecting simple string responses
        """
        return {
            "status": final_response.status,
            "query_id": final_response.query_id,
            "final_answer": final_response.final_content,
            "confidence": final_response.confidence_score,
            "processing_time_ms": final_response.processing_time_ms
        }
    
    def to_enhanced_response_format(self, final_response: FinalResponse) -> Dict[str, Any]:
        """
        Convert final response to enhanced format with full metadata
        
        This provides comprehensive information for advanced systems
        """
        return {
            "status": final_response.status,
            "response_id": final_response.response_id,
            "query_id": final_response.query_id,
            "final_response": {
                "content": final_response.final_content,
                "confidence_score": final_response.confidence_score,
                "processing_time_ms": final_response.processing_time_ms
            },
            "response_metadata": final_response.response_metadata
        }
