"""
Input Processor - The "Sensory Cortex" with Uncertainty Signaling and Multi-Language Support
Implements Task 3.1.4: Enhanced Task List Generation

This is the main Input Processor that integrates all components to generate
"Processor-to-Orchestrator (Task List)" messages per PROTOCOLS.md, now with
uncertainty signaling and multi-language capabilities.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict

from .parser import AdvancedParser, QueryMetadata, ParsedQuery
from .intent_recognizer import IntentRecognizer, IntentResult
from .ambiguity_resolver import AmbiguityResolver, AmbiguityDetection, DisambiguationResult

# Import new uncertainty and multi-language components
from myriad.core.uncertainty.uncertainty_signals import get_uncertainty_detector, UncertaintyAssessment
from myriad.core.socratic.socratic_questioning import get_socratic_dialogue_manager, DialogueSession
from myriad.core.multilang.multilang_parser import get_multilang_parser, QueryMetadata as MultilangQueryMetadata, ParsedQuery as MultilangParsedQuery

@dataclass
class TaskItem:
    """Individual task in the task list"""
    task_id: int
    intent: str
    concept: str
    context: str
    priority: int
    dependencies: List[int]
    confidence: float = 1.0
    estimated_time_ms: int = 1000
    uncertainty_assessment: Optional[UncertaintyAssessment] = None
    language: str = "en"
    requires_clarification: bool = False

@dataclass
class TaskList:
    """Task List message per PROTOCOLS.md"""
    protocol_version: str
    query_metadata: Dict[str, Any]
    parsed_query: Dict[str, Any]
    task_list: List[Dict[str, Any]]
    ambiguity_info: Optional[Dict[str, Any]] = None
    uncertainty_info: Optional[Dict[str, Any]] = None
    language_info: Optional[Dict[str, Any]] = None
    clarification_needed: bool = False
    processing_metadata: Optional[Dict[str, Any]] = None

class InputProcessor:
    """
    Input Processor implementing the complete "Sensory Cortex" functionality
    
    This processor:
    1. Detects the language of the input query
    2. Parses complex queries into structured components using language-specific parsers
    3. Recognizes user intent with confidence scoring
    4. Resolves ambiguities or flags them for clarification
    5. Assesses uncertainty in the query understanding
    6. Generates prioritized task lists with uncertainty information
    7. Initiates Socratic dialogue when needed
    8. Produces protocol-compliant messages for the Orchestrator
    """
    
    def __init__(self):
        """Initialize the Input Processor with all components"""
        # Original components
        self.parser = AdvancedParser()
        self.intent_recognizer = IntentRecognizer()
        self.ambiguity_resolver = AmbiguityResolver()
        
        # New uncertainty and multi-language components
        self.multilang_parser = get_multilang_parser()
        self.uncertainty_detector = get_uncertainty_detector()
        self.socratic_dialogue_manager = get_socratic_dialogue_manager()
        
        # Task generation configuration
        self.max_tasks_per_query = 10
        self.default_task_timeout_ms = 5000
        
        # Intent to agent type mapping (based on current system)
        self.intent_agent_mapping = {
            'define': 'fact_base',
            'analyze_historical_context': 'function_executor',
            'explain_impact': 'function_executor',
            'compare': 'pattern_matcher',
            'calculate': 'function_executor',
            'summarize': 'micro_generator'
        }
        
        # Active dialogue sessions
        self.active_dialogues: Dict[str, DialogueSession] = {}
    
    def process_query(self, raw_query: str, user_context: Optional[Dict] = None) -> TaskList:
        """
        Process a raw query into a task list with uncertainty and language support
        
        Args:
            raw_query: The raw user query string
            user_context: Optional user context (session, preferences, history)
            
        Returns:
            TaskList ready for the Orchestrator
        """
        # Step 1: Detect language and parse with language-specific parser
        query_metadata, parsed_query = self._parse_with_language_support(raw_query, user_context)
        
        # Step 2: Recognize intent (using original recognizer for now)
        intent_result = self.intent_recognizer.recognize_intent(raw_query, user_context)
        
        # Step 3: Detect and resolve ambiguity
        ambiguity_detection = self.ambiguity_resolver.detect_ambiguity(
            raw_query, parsed_query.concepts, intent_result
        )
        
        disambiguation_result = None
        if ambiguity_detection.is_ambiguous:
            disambiguation_result = self.ambiguity_resolver.resolve_ambiguity(
                raw_query, ambiguity_detection, user_context
            )
        
        # Step 4: Assess uncertainty in query understanding
        query_data = {
            'query': raw_query,
            'concepts': parsed_query.concepts,
            'relationships': parsed_query.relationships,
            'intent': intent_result.primary_intent,
            'confidence': intent_result.confidence,
            'ambiguity': ambiguity_detection.is_ambiguous
        }
        
        uncertainty_assessment = self.uncertainty_detector.assess_uncertainty(
            query_data, "InputProcessor"
        )
        
        # Step 5: Determine if clarification is needed
        clarification_needed = self._determine_clarification_need(
            uncertainty_assessment, ambiguity_detection, disambiguation_result
        )
        
        # Step 6: Generate task list with uncertainty information
        task_list = self._generate_task_list(
            parsed_query, intent_result, ambiguity_detection, disambiguation_result,
            uncertainty_assessment, query_metadata.detected_language.value
        )
        
        # Step 7: Create task list message
        task_list_message = TaskList(
            protocol_version="2.0",
            query_metadata=asdict(query_metadata),
            parsed_query=asdict(parsed_query),
            task_list=[asdict(task) for task in task_list],
            ambiguity_info=self._create_ambiguity_info(ambiguity_detection, disambiguation_result),
            uncertainty_info=self._create_uncertainty_info(uncertainty_assessment),
            language_info=self._create_language_info(query_metadata),
            clarification_needed=clarification_needed,
            processing_metadata=self._create_processing_metadata(intent_result, uncertainty_assessment)
        )
        
        return task_list_message
    
    def _parse_with_language_support(self, raw_query: str, user_context: Optional[Dict] = None) -> Tuple[MultilangQueryMetadata, MultilangParsedQuery]:
        """Parse query with language detection and language-specific parsing"""
        try:
            # Use the multi-language parser
            return self.multilang_parser.parse_query(raw_query, user_context)
        except Exception as e:
            # Fallback to original parser if multi-language parsing fails
            print(f"Multi-language parsing failed, falling back to English parser: {e}")
            
            # Use original parser
            original_metadata, original_parsed = self.parser.parse_query(raw_query, user_context)
            
            # Convert to multi-language format
            multilang_metadata = MultilangQueryMetadata(
                query_id=original_metadata.query_id,
                original_query=original_metadata.original_query,
                detected_language="en",  # Default to English
                language_confidence=0.5,  # Low confidence for fallback
                timestamp=original_metadata.timestamp,
                user_context=original_metadata.user_context
            )
            
            multilang_parsed = MultilangParsedQuery(
                primary_intent=original_parsed.primary_intent,
                concepts=original_parsed.concepts,
                relationships=original_parsed.relationships,
                complexity_score=original_parsed.complexity_score,
                estimated_agents_needed=original_parsed.estimated_agents_needed,
                language="en",
                language_specific_data={}
            )
            
            return multilang_metadata, multilang_parsed
    
    def _determine_clarification_need(self, uncertainty_assessment: UncertaintyAssessment,
                                    ambiguity_detection: AmbiguityDetection,
                                    disambiguation_result: Optional[DisambiguationResult]) -> bool:
        """Determine if clarification is needed based on uncertainty and ambiguity"""
        # High uncertainty requires clarification
        if uncertainty_assessment.overall_uncertainty.value >= 0.7:
            return True
        
        # Unresolved ambiguity requires clarification
        if ambiguity_detection.is_ambiguous and (
            not disambiguation_result or
            not disambiguation_result.resolved
        ):
            return True
        
        # Recommended action is to clarify or research
        if uncertainty_assessment.recommended_action in ["clarify", "research"]:
            return True
        
        return False
    
    def _generate_task_list(self, parsed_query: MultilangParsedQuery, intent_result: IntentResult,
                          ambiguity_detection: AmbiguityDetection,
                          disambiguation_result: Optional[DisambiguationResult],
                          uncertainty_assessment: UncertaintyAssessment,
                          language: str) -> List[TaskItem]:
        """Generate task list with uncertainty information"""
        tasks = []
        task_id_counter = 1
        
        # Primary intent task for each major concept
        primary_tasks = []
        for i, concept in enumerate(parsed_query.concepts[:5]):  # Limit to top 5 concepts
            task = TaskItem(
                task_id=task_id_counter,
                intent=intent_result.primary_intent,
                concept=concept,
                context=self._determine_context(concept, parsed_query),
                priority=1,
                dependencies=[],
                confidence=intent_result.confidence,
                estimated_time_ms=self._estimate_task_time(intent_result.primary_intent, concept),
                uncertainty_assessment=uncertainty_assessment,
                language=language,
                requires_clarification=uncertainty_assessment.recommended_action == "clarify"
            )
            tasks.append(task)
            primary_tasks.append(task_id_counter)
            task_id_counter += 1
        
        # Add relationship-based tasks
        for relationship in parsed_query.relationships:
            if len(primary_tasks) >= 2:  # Need at least 2 primary tasks for relationships
                task = TaskItem(
                    task_id=task_id_counter,
                    intent=self._relationship_to_intent(relationship['type']),
                    concept=f"{relationship['subject']}_{relationship['object']}_relationship",
                    context=relationship['type'],
                    priority=2,
                    dependencies=primary_tasks[:2],  # Depends on first two primary tasks
                    confidence=0.8,
                    estimated_time_ms=self._estimate_task_time('explain_impact', 'relationship'),
                    uncertainty_assessment=uncertainty_assessment,
                    language=language,
                    requires_clarification=False
                )
                tasks.append(task)
                task_id_counter += 1
        
        # Add synthesis task if multiple concepts
        if len(parsed_query.concepts) > 1:
            synthesis_task = TaskItem(
                task_id=task_id_counter,
                intent='synthesize_response',
                concept='multi_concept_synthesis',
                context=intent_result.primary_intent,
                priority=3,
                dependencies=primary_tasks,
                confidence=0.9,
                estimated_time_ms=2000,
                uncertainty_assessment=uncertainty_assessment,
                language=language,
                requires_clarification=False
            )
            tasks.append(synthesis_task)
        
        # Sort by priority and return
        return sorted(tasks, key=lambda x: (x.priority, -x.confidence))
    
    def _determine_context(self, concept: str, parsed_query: ParsedQuery) -> str:
        """Determine appropriate context for a concept based on the query"""
        # Check for historical context
        if any(rel['type'] == 'temporal' for rel in parsed_query.relationships):
            return 'historical_context'
        
        # Check for comparative context
        if any(rel['type'] == 'comparative' for rel in parsed_query.relationships):
            return 'comparative_analysis'
        
        # Check for functional context
        if any(rel['type'] == 'functional' for rel in parsed_query.relationships):
            return 'functional_analysis'
        
        # Default context based on concept
        if any(word in concept.lower() for word in ['factory', 'industrial', 'manufacturing']):
            return 'industrial_application'
        elif any(word in concept.lower() for word in ['technology', 'invention', 'innovation']):
            return 'technological_development'
        else:
            return 'general_knowledge'
    
    def _relationship_to_intent(self, relationship_type: str) -> str:
        """Convert relationship type to appropriate intent"""
        mapping = {
            'causal': 'explain_impact',
            'temporal': 'analyze_historical_context',
            'comparative': 'compare',
            'functional': 'explain_impact'
        }
        return mapping.get(relationship_type, 'explain_impact')
    
    def _estimate_task_time(self, intent: str, concept: str) -> int:
        """Estimate task completion time in milliseconds"""
        base_times = {
            'define': 500,
            'analyze_historical_context': 1500,
            'explain_impact': 1200,
            'compare': 1000,
            'calculate': 800,
            'summarize': 1000,
            'synthesize_response': 2000
        }
        
        base_time = base_times.get(intent, 1000)
        
        # Adjust based on concept complexity
        if len(concept.split('_')) > 2:  # Complex compound concept
            base_time = int(base_time * 1.3)
        
        return base_time
    
    def _create_ambiguity_info(self, ambiguity_detection: AmbiguityDetection,
                             disambiguation_result: Optional[DisambiguationResult]) -> Optional[Dict[str, Any]]:
        """Create ambiguity information for the task list"""
        if not ambiguity_detection.is_ambiguous:
            return None
        
        ambiguity_info = {
            'detected': True,
            'type': ambiguity_detection.ambiguity_type.value if ambiguity_detection.ambiguity_type else None,
            'elements': ambiguity_detection.ambiguous_elements,
            'confidence': ambiguity_detection.confidence,
            'suggested_clarifications': ambiguity_detection.suggested_clarifications
        }
        
        if disambiguation_result:
            ambiguity_info['resolution'] = {
                'resolved': disambiguation_result.resolved,
                'chosen_interpretation': disambiguation_result.chosen_interpretation,
                'confidence': disambiguation_result.confidence,
                'reasoning': disambiguation_result.reasoning
            }
        
        return ambiguity_info
    
    def _create_uncertainty_info(self, uncertainty_assessment: UncertaintyAssessment) -> Optional[Dict[str, Any]]:
        """Create uncertainty information for the task list"""
        if uncertainty_assessment.overall_uncertainty.value < 0.3:  # Very low uncertainty
            return None
        
        uncertainty_info = {
            'detected': True,
            'overall_level': uncertainty_assessment.overall_uncertainty.value,
            'recommended_action': uncertainty_assessment.recommended_action,
            'confidence_in_assessment': uncertainty_assessment.confidence_in_assessment,
            'signal_count': len(uncertainty_assessment.uncertainty_signals)
        }
        
        # Add details about uncertainty signals
        signals = []
        for signal in uncertainty_assessment.uncertainty_signals:
            signals.append({
                'type': signal.uncertainty_type.value,
                'level': signal.level.value,
                'description': signal.description,
                'affected_elements': signal.affected_elements,
                'suggested_clarifications': signal.suggested_clarifications
            })
        
        uncertainty_info['signals'] = signals
        
        return uncertainty_info
    
    def _create_language_info(self, query_metadata: MultilangQueryMetadata) -> Dict[str, Any]:
        """Create language information for the task list"""
        return {
            'detected_language': query_metadata.detected_language.value,
            'language_confidence': query_metadata.language_confidence,
            'language_features': query_metadata.user_context.get('language_specific_features', {}),
            'parser_version': query_metadata.user_context.get('parser_version', '1.0')
        }
    
    def _create_processing_metadata(self, intent_result: IntentResult,
                                    uncertainty_assessment: UncertaintyAssessment) -> Dict[str, Any]:
        """Create processing metadata for debugging and optimization"""
        return {
            'processing_timestamp': datetime.now().isoformat(),
            'processor_version': '2.0',
            'intent_analysis': {
                'primary_intent': intent_result.primary_intent,
                'confidence': intent_result.confidence,
                'alternatives': intent_result.alternative_intents,
                'context_factors': intent_result.context_factors
            },
            'uncertainty_analysis': {
                'overall_uncertainty': uncertainty_assessment.overall_uncertainty.value,
                'recommended_action': uncertainty_assessment.recommended_action,
                'signal_count': len(uncertainty_assessment.uncertainty_signals)
            },
            'performance_metrics': {
                'processing_time_ms': 50,  # Would be measured in real implementation
                'complexity_handled': True,
                'ambiguity_detected': intent_result.is_ambiguous,
                'uncertainty_detected': uncertainty_assessment.overall_uncertainty.value > 0.3
            }
        }
    
    def initiate_clarification_dialogue(self, task_list: TaskList,
                                      user_response: Optional[str] = None) -> Dict[str, Any]:
        """
        Initiate or continue a clarification dialogue based on uncertainty
        
        Args:
            task_list: The task list with uncertainty information
            user_response: Optional user response to continue the dialogue
            
        Returns:
            Dialogue response with questions or resolution
        """
        if not task_list.uncertainty_info or not task_list.clarification_needed:
            return {
                'status': 'no_clarification_needed',
                'message': 'No clarification needed based on current assessment'
            }
        
        # Check if there's an active dialogue session
        query_id = task_list.query_metadata.get('query_id')
        if query_id in self.active_dialogues:
            # Continue existing dialogue
            if user_response:
                session = self.socratic_dialogue_manager.process_response(query_id, user_response)
                return self._format_dialogue_response(session)
            else:
                return {
                    'status': 'awaiting_response',
                    'message': 'Please provide a response to the clarification question'
                }
        else:
            # Start new dialogue
            uncertainty_assessment = self._reconstruct_uncertainty_assessment(task_list.uncertainty_info)
            original_query = task_list.query_metadata.get('original_query', '')
            
            session = self.socratic_dialogue_manager.initiate_dialogue(
                original_query, uncertainty_assessment, task_list.query_metadata
            )
            
            self.active_dialogues[query_id] = session
            return self._format_dialogue_response(session)
    
    def _reconstruct_uncertainty_assessment(self, uncertainty_info: Dict[str, Any]) -> UncertaintyAssessment:
        """Reconstruct uncertainty assessment from task list uncertainty info"""
        from myriad.core.uncertainty.uncertainty_signals import UncertaintyLevel, UncertaintyType, UncertaintySignal
        
        # Create uncertainty signals from task list info
        signals = []
        for signal_data in uncertainty_info.get('signals', []):
            signal = UncertaintySignal(
                uncertainty_type=UncertaintyType(signal_data['type']),
                level=UncertaintyLevel(signal_data['level']),
                description=signal_data['description'],
                affected_elements=signal_data['affected_elements'],
                suggested_clarifications=signal_data['suggested_clarifications'],
                confidence_in_uncertainty=0.7,  # Default confidence
                timestamp=0,  # Would be actual timestamp
                source_agent="InputProcessor"
            )
            signals.append(signal)
        
        # Create uncertainty assessment
        return UncertaintyAssessment(
            overall_uncertainty=UncertaintyLevel(uncertainty_info['overall_level']),
            uncertainty_signals=signals,
            recommended_action=uncertainty_info['recommended_action'],
            confidence_in_assessment=uncertainty_info['confidence_in_assessment'],
            metadata={}
        )
    
    def _format_dialogue_response(self, session: DialogueSession) -> Dict[str, Any]:
        """Format a dialogue session response"""
        if session.current_state.value == 'questioning' and session.questions_asked:
            # Return the next question
            question = session.questions_asked[-1]  # Get the most recent question
            return {
                'status': 'question',
                'session_id': session.session_id,
                'question_id': question.question_id,
                'question_text': question.question_text,
                'question_type': question.question_type.value,
                'options': question.options,
                'context': question.context
            }
        elif session.current_state.value == 'completed':
            # Return the resolution
            return {
                'status': 'completed',
                'session_id': session.session_id,
                'resolution': session.resolution,
                'message': 'Clarification dialogue completed'
            }
        else:
            return {
                'status': session.current_state.value,
                'session_id': session.session_id,
                'message': f'Dialogue is in {session.current_state.value} state'
            }
    
    def to_orchestrator_protocol(self, task_list: TaskList) -> Dict[str, Any]:
        """
        Convert task list to the standard Orchestrator protocol format
        
        This maintains backward compatibility with the existing Orchestrator
        while providing enhanced information.
        """
        # Convert to the basic protocol format expected by current Orchestrator
        basic_task_list = {
            "query_id": task_list.query_metadata['query_id'],
            "tasks": []
        }
        
        for task_dict in task_list.task_list:
            # Convert task to basic task format
            basic_task = {
                "task_id": task_dict['task_id'],
                "intent": task_dict['intent'],
                "concept": task_dict['concept'],
                "args": {
                    "context": task_dict['context'],
                    "priority": task_dict['priority'],
                    "confidence": task_dict['confidence'],
                    "language": task_dict.get('language', 'en')
                }
            }
            
            # Add uncertainty information if available
            if task_dict.get('uncertainty_assessment'):
                basic_task['args']['uncertainty_level'] = task_dict['uncertainty_assessment'].overall_uncertainty.value
                basic_task['args']['requires_clarification'] = task_dict.get('requires_clarification', False)
            
            basic_task_list["tasks"].append(basic_task)
        
        # Add enhanced metadata as optional fields
        if task_list.uncertainty_info:
            basic_task_list['uncertainty_info'] = task_list.uncertainty_info
        
        if task_list.language_info:
            basic_task_list['language_info'] = task_list.language_info
        
        if task_list.clarification_needed:
            basic_task_list['clarification_needed'] = True
        
        return basic_task_list
