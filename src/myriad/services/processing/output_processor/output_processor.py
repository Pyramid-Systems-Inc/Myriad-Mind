"""
Enhanced Output Processor - The "Motor Cortex" with Uncertainty & Clarification Support
Implements Task 3.2.3: Protocol Message Processing

This is the main Output Processor that consumes "Orchestrator-to-OutputProcessor 
(Collected Results)" messages, parses agent_responses with confidence weights,
applies synthesis_parameters, and generates coherent final responses with proper citation.

Now includes:
- Uncertainty-aware response generation
- Socratic dialogue integration for clarifications
- Multi-language response formatting
"""

import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

from .synthesizer import AdvancedSynthesizer, SynthesisParameters, SynthesisResult
from .formatter import MultiFormatFormatter, FormattingParameters, FormattedResponse, OutputFormat, TargetLength, EvidenceLevel

# Import uncertainty and multi-language components
from myriad.core.uncertainty.uncertainty_signals import UncertaintyAssessment, UncertaintyLevel
from myriad.core.socratic.socratic_questioning import get_socratic_dialogue_manager, DialogueSession, SocraticQuestion

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
    requires_clarification: bool = False
    clarification_questions: Optional[List[Dict[str, Any]]] = None
    dialogue_session_id: Optional[str] = None
    language: str = "en"
    uncertainty_info: Optional[Dict[str, Any]] = None

class EnhancedOutputProcessor:
    """
    Enhanced Output Processor implementing the complete "Motor Cortex" functionality
    
    This processor:
    1. Consumes "Orchestrator-to-OutputProcessor (Collected Results)" messages
    2. Parses agent_responses with individual confidence and contribution weights
    3. Applies synthesis_parameters for customized output generation
    4. Generates coherent final responses with proper citation and confidence metrics
    5. Supports both basic and enhanced protocol formats
    6. Handles uncertainty-driven clarification dialogues
    7. Formats Socratic questions for user interaction
    8. Processes user responses to clarification questions
    """
    
    def __init__(self):
        """Initialize the Enhanced Output Processor with components"""
        self.synthesizer = AdvancedSynthesizer()
        self.formatter = MultiFormatFormatter()
        self.socratic_dialogue_manager = get_socratic_dialogue_manager()
        
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
        
        # Uncertainty thresholds for clarification
        self.uncertainty_threshold_high = 0.7  # High uncertainty - always clarify
        self.uncertainty_threshold_medium = 0.4  # Medium uncertainty - clarify if important
        self.min_confidence_for_response = 0.3  # Below this, must clarify
    
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
        """Process through the complete synthesis and formatting pipeline with uncertainty handling"""
        
        # Step 1: Extract uncertainty information from query metadata
        query_metadata = structured_results.query_metadata or {}
        uncertainty_info = query_metadata.get('uncertainty_info', {})
        clarification_needed = query_metadata.get('clarification_needed', False)
        language = query_metadata.get('language_info', {}).get('detected_language', 'en')
        
        # Step 2: Check if clarification is needed before synthesis
        if clarification_needed and uncertainty_info:
            return self._handle_clarification_request(
                structured_results, uncertainty_info, language, start_time
            )
        
        # Step 3: Synthesize agent responses
        synthesis_result = self.synthesizer.synthesize_responses(
            agent_responses=structured_results.collected_results,
            synthesis_parameters=synthesis_params,
            query_metadata=query_metadata
        )
        
        # Step 4: Check if synthesis confidence is too low
        if synthesis_result.confidence_score < self.min_confidence_for_response:
            return self._handle_low_confidence_response(
                structured_results, synthesis_result, language, start_time
            )
        
        # Step 5: Format the synthesized content
        formatted_response = self.formatter.format_response(
            synthesized_content=synthesis_result.synthesized_content,
            evidence_sources=synthesis_result.evidence_sources,
            confidence_score=synthesis_result.confidence_score,
            synthesis_metadata=synthesis_result.synthesis_metadata,
            formatting_parameters=formatting_params,
            warnings=synthesis_result.warnings
        )
        
        # Step 6: Create final response
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        response_metadata = self._create_response_metadata(
            synthesis_result, formatted_response, synthesis_params, formatting_params
        )
        
        # Add uncertainty information if present
        if uncertainty_info:
            response_metadata['uncertainty_info'] = uncertainty_info
        
        final_response = FinalResponse(
            response_id=f"resp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}",
            query_id=structured_results.query_id,
            final_content=formatted_response.content,
            confidence_score=synthesis_result.confidence_score,
            response_metadata=response_metadata,
            processing_time_ms=processing_time,
            status="success",
            language=language,
            uncertainty_info=uncertainty_info if uncertainty_info else None
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
        response_dict = {
            "status": final_response.status,
            "response_id": final_response.response_id,
            "query_id": final_response.query_id,
            "final_response": {
                "content": final_response.final_content,
                "confidence_score": final_response.confidence_score,
                "processing_time_ms": final_response.processing_time_ms,
                "language": final_response.language
            },
            "response_metadata": final_response.response_metadata
        }
        
        # Add clarification information if present
        if final_response.requires_clarification:
            response_dict["clarification"] = {
                "requires_clarification": True,
                "dialogue_session_id": final_response.dialogue_session_id,
                "questions": final_response.clarification_questions,
                "uncertainty_info": final_response.uncertainty_info
            }
        
        return response_dict
    
    def _handle_clarification_request(self, structured_results: CollectedResults,
                                     uncertainty_info: Dict[str, Any],
                                     language: str,
                                     start_time: datetime) -> FinalResponse:
        """
        Handle a request that needs clarification due to uncertainty
        
        Args:
            structured_results: The collected results
            uncertainty_info: Information about the uncertainty
            language: Language for generating questions
            start_time: Processing start time
            
        Returns:
            FinalResponse with clarification questions
        """
        query_metadata = structured_results.query_metadata or {}
        original_query = query_metadata.get('original_query', '')
        
        # Get or create uncertainty assessment
        uncertainty_assessment = self._extract_uncertainty_assessment(uncertainty_info)
        
        # Initiate Socratic dialogue
        dialogue_session = self.socratic_dialogue_manager.initiate_dialogue(
            original_query=original_query,
            uncertainty_assessment=uncertainty_assessment,
            language=language
        )
        
        # Format clarification questions
        clarification_questions = self._format_clarification_questions(
            dialogue_session.questions_asked,
            language
        )
        
        # Create clarification message
        clarification_message = self._generate_clarification_message(
            uncertainty_assessment,
            clarification_questions,
            language
        )
        
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return FinalResponse(
            response_id=f"resp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}",
            query_id=structured_results.query_id,
            final_content=clarification_message,
            confidence_score=0.0,  # No answer yet, needs clarification
            response_metadata={
                'processor_info': {
                    'processor_name': 'Enhanced_Output_Processor',
                    'processor_version': '1.0.0',
                    'processing_timestamp': datetime.now().isoformat()
                },
                'clarification_reason': uncertainty_assessment.primary_uncertainty_type.value if uncertainty_assessment else 'unknown'
            },
            processing_time_ms=processing_time,
            status="needs_clarification",
            requires_clarification=True,
            clarification_questions=clarification_questions,
            dialogue_session_id=dialogue_session.session_id,
            language=language,
            uncertainty_info=uncertainty_info
        )
    
    def _handle_low_confidence_response(self, structured_results: CollectedResults,
                                       synthesis_result: SynthesisResult,
                                       language: str,
                                       start_time: datetime) -> FinalResponse:
        """
        Handle a response with confidence below the minimum threshold
        
        Args:
            structured_results: The collected results
            synthesis_result: The synthesis result with low confidence
            language: Language for generating questions
            start_time: Processing start time
            
        Returns:
            FinalResponse with clarification questions or low-confidence warning
        """
        # Create uncertainty assessment from low confidence
        from myriad.core.uncertainty.uncertainty_signals import UncertaintyAssessment, UncertaintyType, UncertaintyLevel
        
        uncertainty_assessment = UncertaintyAssessment(
            agent_id="OutputProcessor",
            primary_uncertainty_type=UncertaintyType.LOW_CONFIDENCE,
            uncertainty_level=UncertaintyLevel.HIGH,
            uncertainty_score=1.0 - synthesis_result.confidence_score,
            affected_concepts=['response'],
            description=f"Synthesized response has low confidence ({synthesis_result.confidence_score:.2f})",
            suggested_actions=["Request clarification", "Gather more information"],
            context={'synthesis_warnings': synthesis_result.warnings}
        )
        
        query_metadata = structured_results.query_metadata or {}
        original_query = query_metadata.get('original_query', '')
        
        # Initiate dialogue for clarification
        dialogue_session = self.socratic_dialogue_manager.initiate_dialogue(
            original_query=original_query,
            uncertainty_assessment=uncertainty_assessment,
            language=language
        )
        
        # Format clarification questions
        clarification_questions = self._format_clarification_questions(
            dialogue_session.questions_asked,
            language
        )
        
        # Create message explaining low confidence and asking for clarification
        clarification_message = self._generate_low_confidence_message(
            synthesis_result,
            clarification_questions,
            language
        )
        
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return FinalResponse(
            response_id=f"resp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}",
            query_id=structured_results.query_id,
            final_content=clarification_message,
            confidence_score=synthesis_result.confidence_score,
            response_metadata={
                'processor_info': {
                    'processor_name': 'Enhanced_Output_Processor',
                    'processor_version': '1.0.0',
                    'processing_timestamp': datetime.now().isoformat()
                },
                'low_confidence_reason': 'Insufficient information or conflicting sources',
                'synthesis_warnings': synthesis_result.warnings
            },
            processing_time_ms=processing_time,
            status="needs_clarification",
            requires_clarification=True,
            clarification_questions=clarification_questions,
            dialogue_session_id=dialogue_session.session_id,
            language=language,
            uncertainty_info={'type': 'low_confidence', 'score': synthesis_result.confidence_score}
        )
    
    def _extract_uncertainty_assessment(self, uncertainty_info: Dict[str, Any]) -> Optional[UncertaintyAssessment]:
        """Extract UncertaintyAssessment from uncertainty info dictionary"""
        if not uncertainty_info:
            return None
        
        from myriad.core.uncertainty.uncertainty_signals import UncertaintyAssessment, UncertaintyType, UncertaintyLevel
        
        # Try to reconstruct UncertaintyAssessment
        try:
            uncertainty_type = UncertaintyType(uncertainty_info.get('primary_uncertainty_type', 'knowledge_gap'))
            uncertainty_level = UncertaintyLevel(uncertainty_info.get('uncertainty_level', 'medium'))
            
            return UncertaintyAssessment(
                agent_id=uncertainty_info.get('agent_id', 'InputProcessor'),
                primary_uncertainty_type=uncertainty_type,
                uncertainty_level=uncertainty_level,
                uncertainty_score=uncertainty_info.get('uncertainty_score', 0.5),
                affected_concepts=uncertainty_info.get('affected_concepts', []),
                description=uncertainty_info.get('description', 'Uncertainty detected'),
                suggested_actions=uncertainty_info.get('suggested_actions', []),
                context=uncertainty_info.get('context', {})
            )
        except:
            return None
    
    def _format_clarification_questions(self, questions: List[SocraticQuestion],
                                       language: str) -> List[Dict[str, Any]]:
        """
        Format Socratic questions for presentation to the user
        
        Args:
            questions: List of SocraticQuestion objects
            language: Language for the questions
            
        Returns:
            List of formatted question dictionaries
        """
        formatted_questions = []
        
        for i, question in enumerate(questions, 1):
            formatted_q = {
                'question_id': question.question_id,
                'question_number': i,
                'question_type': question.question_type.value,
                'question_text': question.question_text,
                'priority': question.priority,
                'expected_response_type': question.expected_response_type
            }
            
            # Add options if this is a multiple choice question
            if question.options:
                formatted_q['options'] = question.options
                formatted_q['response_format'] = 'multiple_choice'
            else:
                formatted_q['response_format'] = 'free_text'
            
            formatted_questions.append(formatted_q)
        
        return formatted_questions
    
    def _generate_clarification_message(self, uncertainty_assessment: Optional[UncertaintyAssessment],
                                       questions: List[Dict[str, Any]],
                                       language: str) -> str:
        """
        Generate a human-friendly message explaining the need for clarification
        
        Args:
            uncertainty_assessment: The uncertainty assessment
            questions: Formatted clarification questions
            language: Language for the message
            
        Returns:
            Clarification message string
        """
        # Language-specific templates
        templates = {
            'en': {
                'intro': "I need some clarification to provide an accurate answer.",
                'reason_knowledge_gap': "I don't have enough information about some aspects of your query.",
                'reason_conflicting': "I found conflicting information and need your guidance.",
                'reason_ambiguous': "Your query has multiple possible interpretations.",
                'questions_intro': "Please help me understand by answering these questions:",
                'question_format': "{num}. {text}"
            },
            'es': {
                'intro': "Necesito alguna aclaración para proporcionar una respuesta precisa.",
                'reason_knowledge_gap': "No tengo suficiente información sobre algunos aspectos de tu consulta.",
                'reason_conflicting': "Encontré información contradictoria y necesito tu orientación.",
                'reason_ambiguous': "Tu consulta tiene múltiples interpretaciones posibles.",
                'questions_intro': "Por favor, ayúdame a entender respondiendo estas preguntas:",
                'question_format': "{num}. {text}"
            },
            'fr': {
                'intro': "J'ai besoin de clarification pour fournir une réponse précise.",
                'reason_knowledge_gap': "Je n'ai pas assez d'informations sur certains aspects de votre question.",
                'reason_conflicting': "J'ai trouvé des informations contradictoires et j'ai besoin de votre aide.",
                'reason_ambiguous': "Votre question a plusieurs interprétations possibles.",
                'questions_intro': "Veuillez m'aider à comprendre en répondant à ces questions:",
                'question_format': "{num}. {text}"
            },
            'de': {
                'intro': "Ich brauche eine Klärung, um eine genaue Antwort zu geben.",
                'reason_knowledge_gap': "Ich habe nicht genügend Informationen über einige Aspekte Ihrer Anfrage.",
                'reason_conflicting': "Ich habe widersprüchliche Informationen gefunden und brauche Ihre Anleitung.",
                'reason_ambiguous': "Ihre Anfrage hat mehrere mögliche Interpretationen.",
                'questions_intro': "Bitte helfen Sie mir zu verstehen, indem Sie diese Fragen beantworten:",
                'question_format': "{num}. {text}"
            },
            'zh': {
                'intro': "我需要一些澄清来提供准确的答案。",
                'reason_knowledge_gap': "我没有足够的信息了解您查询的某些方面。",
                'reason_conflicting': "我发现了矛盾的信息，需要您的指导。",
                'reason_ambiguous': "您的查询有多种可能的解释。",
                'questions_intro': "请通过回答这些问题帮助我理解：",
                'question_format': "{num}. {text}"
            }
        }
        
        template = templates.get(language, templates['en'])
        
        # Build message
        message_parts = [template['intro'], ""]
        
        # Add reason if uncertainty assessment is available
        if uncertainty_assessment:
            uncertainty_type = uncertainty_assessment.primary_uncertainty_type.value
            if 'knowledge_gap' in uncertainty_type:
                message_parts.append(template['reason_knowledge_gap'])
            elif 'conflicting' in uncertainty_type:
                message_parts.append(template['reason_conflicting'])
            elif 'ambiguous' in uncertainty_type:
                message_parts.append(template['reason_ambiguous'])
            message_parts.append("")
        
        # Add questions
        message_parts.append(template['questions_intro'])
        message_parts.append("")
        
        for question in questions:
            q_text = template['question_format'].format(
                num=question['question_number'],
                text=question['question_text']
            )
            message_parts.append(q_text)
            
            # Add options if multiple choice
            if question.get('options'):
                for i, option in enumerate(question['options'], 1):
                    message_parts.append(f"   {chr(96+i)}) {option}")
            message_parts.append("")
        
        return '\n'.join(message_parts)
    
    def _generate_low_confidence_message(self, synthesis_result: SynthesisResult,
                                        questions: List[Dict[str, Any]],
                                        language: str) -> str:
        """
        Generate a message for low confidence responses
        
        Args:
            synthesis_result: The synthesis result with low confidence
            questions: Clarification questions
            language: Language for the message
            
        Returns:
            Low confidence message string
        """
        templates = {
            'en': {
                'intro': "I have limited confidence in my answer due to insufficient or conflicting information.",
                'confidence': "Confidence level: {confidence:.0%}",
                'clarification': "To provide a better answer, I need some clarification:"
            },
            'es': {
                'intro': "Tengo confianza limitada en mi respuesta debido a información insuficiente o contradictoria.",
                'confidence': "Nivel de confianza: {confidence:.0%}",
                'clarification': "Para proporcionar una mejor respuesta, necesito alguna aclaración:"
            },
            'fr': {
                'intro': "J'ai une confiance limitée dans ma réponse en raison d'informations insuffisantes ou contradictoires.",
                'confidence': "Niveau de confiance: {confidence:.0%}",
                'clarification': "Pour fournir une meilleure réponse, j'ai besoin de clarification:"
            },
            'de': {
                'intro': "Ich habe begrenztesVertrauen in meine Antwort aufgrund unzureichender oder widersprüchlicher Informationen.",
                'confidence': "Vertrauensniveau: {confidence:.0%}",
                'clarification': "Um eine bessere Antwort zu geben, brauche ich eine Klärung:"
            },
            'zh': {
                'intro': "由于信息不足或矛盾，我对答案的信心有限。",
                'confidence': "信心水平：{confidence:.0%}",
                'clarification': "为了提供更好的答案，我需要一些澄清："
            }
        }
        
        template = templates.get(language, templates['en'])
        
        message_parts = [
            template['intro'],
            template['confidence'].format(confidence=synthesis_result.confidence_score),
            "",
            template['clarification'],
            ""
        ]
        
        # Add questions using the same format as clarification message
        return message_parts[0] + '\n' + self._generate_clarification_message(None, questions, language)
    
    def process_clarification_response(self, dialogue_session_id: str,
                                      user_responses: Dict[str, str],
                                      language: str = 'en') -> Dict[str, Any]:
        """
        Process user responses to clarification questions
        
        Args:
            dialogue_session_id: The dialogue session ID
            user_responses: Dictionary mapping question_id to user response
            language: Language of the responses
            
        Returns:
            Dictionary with processed responses and next steps
        """
        # Submit responses to dialogue manager
        processed = self.socratic_dialogue_manager.submit_responses(
            dialogue_session_id,
            user_responses
        )
        
        # Check if dialogue is resolved
        if processed['resolved']:
            return {
                'status': 'resolved',
                'resolution': processed['resolution'],
                'next_action': 'reprocess_query',
                'updated_query_context': processed.get('updated_context', {})
            }
        else:
            # More questions needed
            return {
                'status': 'needs_more_clarification',
                'additional_questions': processed.get('additional_questions', []),
                'next_action': 'ask_more_questions'
            }
