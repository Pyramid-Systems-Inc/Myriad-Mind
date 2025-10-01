"""
Socratic Questioning System for Myriad Cognitive Architecture
============================================================

This module provides the Socratic questioning system that generates clarifying
questions when uncertainty is detected, enabling more human-like dialogue
for resolving ambiguity and knowledge gaps.

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Socratic Questioning)
Date: 2025-01-01
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import time

from ..uncertainty.uncertainty_signals import UncertaintyAssessment, UncertaintyType, UncertaintyLevel

class QuestionType(Enum):
    """Types of Socratic questions"""
    CLARIFICATION = "clarification"  # Request for clarification
    ELABORATION = "elaboration"      # Request for more detail
    JUSTIFICATION = "justification"  # Request for reasoning
    ALTERNATIVE = "alternative"      # Request for alternatives
    EXAMPLE = "example"              # Request for examples
    IMPLICATION = "implication"      # Request for implications
    PERSPECTIVE = "perspective"      # Request for different perspectives

class DialogueState(Enum):
    """States in the Socratic dialogue"""
    INITIATING = "initiating"        # Starting the dialogue
    QUESTIONING = "questioning"      # Asking questions
    PROCESSING = "processing"        # Processing user responses
    RESOLVING = "resolving"          # Resolving the uncertainty
    COMPLETED = "completed"          # Dialogue completed

@dataclass
class SocraticQuestion:
    """A single Socratic question"""
    question_id: str
    question_type: QuestionType
    question_text: str
    context: Dict[str, Any]
    expected_response_type: str
    priority: int  # 1-5, where 1 is highest
    options: Optional[List[str]] = None  # For multiple choice questions

@dataclass
class DialogueSession:
    """A Socratic dialogue session"""
    session_id: str
    original_query: str
    uncertainty_assessment: UncertaintyAssessment
    current_state: DialogueState
    questions_asked: List[SocraticQuestion]
    responses_received: List[Dict[str, Any]]
    resolution: Optional[Dict[str, Any]]
    metadata: Dict[str, Any]
    created_at: float
    updated_at: float

class SocraticQuestionGenerator:
    """
    Generates Socratic questions to resolve uncertainty and ambiguity
    
    This generator creates targeted questions based on:
    - Type of uncertainty detected
    - Specific concepts or relationships affected
    - Context of the original query
    - Previous questions and responses in the dialogue
    """
    
    def __init__(self):
        """Initialize the Socratic question generator"""
        
        # Question templates for different uncertainty types
        self.question_templates = {
            UncertaintyType.KNOWLEDGE_GAP: {
                QuestionType.CLARIFICATION: [
                    "I don't have enough information about {concept}. Can you provide more details?",
                    "My knowledge about {concept} is limited. What specific aspect would you like me to focus on?",
                    "I need more context about {concept}. Can you elaborate on what you're looking for?"
                ],
                QuestionType.EXAMPLE: [
                    "To better understand {concept}, could you provide an example?",
                    "An example would help me grasp {concept} better. Can you share one?",
                    "I'm not familiar with {concept} in this context. Could you give me an example?"
                ]
            },
            UncertaintyType.CONFLICTING_INFO: {
                QuestionType.CLARIFICATION: [
                    "I found conflicting information about {concept}. Which source should I prioritize?",
                    "There seems to be disagreement about {concept}. Can you help me resolve this?",
                    "I'm getting conflicting answers about {concept}. What's your perspective on this?"
                ],
                QuestionType.JUSTIFICATION: [
                    "Why do you think {perspective} is more accurate than {alternative}?",
                    "What evidence supports {perspective} over {alternative}?",
                    "Can you help me understand why {perspective} is preferred in this case?"
                ]
            },
            UncertaintyType.AMBIGUOUS_CONCEPT: {
                QuestionType.CLARIFICATION: [
                    "When you mention '{concept}', do you mean:",
                    "I'm not sure which '{concept}' you're referring to. Do you mean:",
                    "The term '{concept}' can mean different things. Are you referring to:"
                ],
                QuestionType.ALTERNATIVE: [
                    "Are you interested in {option1} or {option2}?",
                    "Should I focus on {option1} or {option2} in my response?",
                    "Which aspect of '{concept}' is most relevant: {option1} or {option2}?"
                ]
            },
            UncertaintyType.INSUFFICIENT_CONTEXT: {
                QuestionType.CLARIFICATION: [
                    "I need more context to properly answer about {concept}. Can you provide background information?",
                    "To give you the best answer about {concept}, could you share more context?",
                    "The context for {concept} isn't clear. What situation are you referring to?"
                ],
                QuestionType.PERSPECTIVE: [
                    "From what perspective are you asking about {concept}?",
                    "What's your point of view or interest in {concept}?",
                    "Are you looking at {concept} from a specific angle or perspective?"
                ]
            },
            UncertaintyType.LOW_CONFIDENCE: {
                QuestionType.JUSTIFICATION: [
                    "I'm not entirely confident about my understanding of {concept}. Can you confirm if this is correct?",
                    "Before I proceed with {concept}, could you verify if my understanding is accurate?",
                    "I want to make sure I'm on the right track with {concept}. Can you provide guidance?"
                ]
            }
        }
        
        # Follow-up question templates
        self.follow_up_templates = {
            QuestionType.ELABORATION: [
                "Could you tell me more about {topic}?",
                "What additional details can you share about {topic}?",
                "I'd like to understand {topic} better. Can you elaborate?"
            ],
            QuestionType.IMPLICATION: [
                "What are the implications of {topic} in this context?",
                "How does {topic} affect the situation you're describing?",
                "What consequences does {topic} have for your question?"
            ],
            QuestionType.PERSPECTIVE: [
                "How do you see {topic} from your perspective?",
                "What's your take on {topic}?",
                "From your point of view, what's most important about {topic}?"
            ]
        }
    
    def generate_questions(self, uncertainty_assessment: UncertaintyAssessment, 
                          original_query: str, context: Dict[str, Any] = None) -> List[SocraticQuestion]:
        """
        Generate Socratic questions based on uncertainty assessment
        
        Args:
            uncertainty_assessment: The uncertainty assessment from the agent
            original_query: The original user query
            context: Additional context for question generation
            
        Returns:
            List of Socratic questions ordered by priority
        """
        questions = []
        question_id_counter = 1
        
        # Generate questions for each uncertainty signal
        for signal in uncertainty_assessment.uncertainty_signals:
            signal_questions = self._generate_questions_for_signal(
                signal, original_query, context, question_id_counter
            )
            questions.extend(signal_questions)
            question_id_counter += len(signal_questions)
        
        # Sort questions by priority and relevance
        questions = self._prioritize_questions(questions, uncertainty_assessment)
        
        return questions[:5]  # Limit to top 5 questions
    
    def _generate_questions_for_signal(self, signal, original_query: str, 
                                     context: Dict[str, Any], start_id: int) -> List[SocraticQuestion]:
        """Generate questions for a specific uncertainty signal"""
        questions = []
        
        # Get templates for this uncertainty type
        templates = self.question_templates.get(signal.uncertainty_type, {})
        
        # Generate questions for each question type
        for question_type, template_list in templates.items():
            if not template_list:
                continue
            
            # Select the most appropriate template
            template = self._select_template(template_list, signal, context)
            
            # Format the template with context
            question_text = self._format_template(template, signal, original_query, context)
            
            # Determine expected response type
            expected_response = self._determine_expected_response(question_type, signal)
            
            # Create the question
            question = SocraticQuestion(
                question_id=f"q_{start_id}",
                question_type=question_type,
                question_text=question_text,
                context={
                    'uncertainty_type': signal.uncertainty_type.value,
                    'affected_elements': signal.affected_elements,
                    'original_query': original_query
                },
                expected_response_type=expected_response,
                priority=self._calculate_question_priority(question_type, signal),
                options=self._generate_question_options(signal, question_type)
            )
            
            questions.append(question)
            start_id += 1
        
        return questions
    
    def _select_template(self, templates: List[str], signal, context: Dict[str, Any]) -> str:
        """Select the most appropriate template from a list"""
        if not templates:
            return "I need more information to help you better."
        
        # Simple selection - could be enhanced with more sophisticated logic
        # For now, just return the first template
        return templates[0]
    
    def _format_template(self, template: str, signal, original_query: str, 
                        context: Dict[str, Any]) -> str:
        """Format a template with context-specific information"""
        # Replace placeholders with actual values
        formatted = template
        
        # Replace concept placeholders
        if signal.affected_elements:
            concept = signal.affected_elements[0]  # Use first affected element
            formatted = formatted.replace("{concept}", concept)
        
        # Replace perspective/alternative placeholders
        if signal.uncertainty_type == UncertaintyType.CONFLICTING_INFO:
            # This would need more sophisticated logic to extract perspectives
            formatted = formatted.replace("{perspective}", "the first perspective")
            formatted = formatted.replace("{alternative}", "the alternative perspective")
        elif signal.uncertainty_type == UncertaintyType.AMBIGUOUS_CONCEPT:
            # This would need to extract the specific meanings
            formatted = formatted.replace("{option1}", "the first meaning")
            formatted = formatted.replace("{option2}", "the second meaning")
        
        return formatted
    
    def _determine_expected_response(self, question_type: QuestionType, 
                                   signal) -> str:
        """Determine the expected type of response for a question"""
        response_types = {
            QuestionType.CLARIFICATION: "text",
            QuestionType.ELABORATION: "text",
            QuestionType.JUSTIFICATION: "text",
            QuestionType.ALTERNATIVE: "choice",
            QuestionType.EXAMPLE: "example",
            QuestionType.IMPLICATION: "text",
            QuestionType.PERSPECTIVE: "text"
        }
        
        return response_types.get(question_type, "text")
    
    def _calculate_question_priority(self, question_type: QuestionType, 
                                   signal) -> int:
        """Calculate priority for a question (1-5, where 1 is highest)"""
        # Base priorities by question type
        base_priorities = {
            QuestionType.CLARIFICATION: 1,      # Highest priority
            QuestionType.ALTERNATIVE: 2,       # High priority
            QuestionType.JUSTIFICATION: 3,     # Medium-high priority
            QuestionType.EXAMPLE: 4,           # Medium priority
            QuestionType.ELABORATION: 4,       # Medium priority
            QuestionType.IMPLICATION: 5,       # Lower priority
            QuestionType.PERSPECTIVE: 5        # Lower priority
        }
        
        base_priority = base_priorities.get(question_type, 3)
        
        # Adjust based on uncertainty level
        if signal.level == UncertaintyLevel.VERY_HIGH:
            return min(base_priority, 1)  # Highest priority for very high uncertainty
        elif signal.level == UncertaintyLevel.HIGH:
            return min(base_priority, 2)  # High priority for high uncertainty
        elif signal.level == UncertaintyLevel.MEDIUM:
            return base_priority  # Keep base priority for medium uncertainty
        else:
            return max(base_priority, 4)  # Lower priority for low uncertainty
    
    def _generate_question_options(self, signal, question_type: QuestionType) -> Optional[List[str]]:
        """Generate options for multiple-choice questions"""
        if question_type == QuestionType.ALTERNATIVE and signal.uncertainty_type == UncertaintyType.AMBIGUOUS_CONCEPT:
            # Generate options based on ambiguous concept meanings
            if signal.affected_elements:
                concept = signal.affected_elements[0].lower()
                if concept == "drive":
                    return ["Computer storage", "Vehicle operation", "Motivation/drive"]
                elif concept == "bank":
                    return ["Financial institution", "River bank"]
                elif concept == "light":
                    return ["Illumination", "Weight", "Color shade"]
                elif concept == "factory":
                    return ["Manufacturing facility", "Design pattern"]
        
        return None
    
    def _prioritize_questions(self, questions: List[SocraticQuestion], 
                            uncertainty_assessment: UncertaintyAssessment) -> List[SocraticQuestion]:
        """Prioritize questions based on uncertainty assessment and question type"""
        # Sort by priority (lower number = higher priority)
        questions.sort(key=lambda q: q.priority)
        
        # Further prioritize based on uncertainty level
        if uncertainty_assessment.overall_uncertainty in [UncertaintyLevel.VERY_HIGH, UncertaintyLevel.HIGH]:
            # For high uncertainty, prioritize clarification questions
            clarification_questions = [q for q in questions if q.question_type == QuestionType.CLARIFICATION]
            other_questions = [q for q in questions if q.question_type != QuestionType.CLARIFICATION]
            return clarification_questions + other_questions
        
        return questions


class SocraticDialogueManager:
    """
    Manages Socratic dialogue sessions for resolving uncertainty
    
    This manager:
    - Initiates dialogue sessions when uncertainty is detected
    - Tracks questions asked and responses received
    - Determines when uncertainty is resolved
    - Maintains dialogue state and context
    """
    
    def __init__(self):
        """Initialize the Socratic dialogue manager"""
        self.question_generator = SocraticQuestionGenerator()
        self.active_sessions: Dict[str, DialogueSession] = {}
    
    def initiate_dialogue(self, original_query: str, uncertainty_assessment: UncertaintyAssessment,
                         context: Dict[str, Any] = None) -> DialogueSession:
        """
        Initiate a Socratic dialogue session
        
        Args:
            original_query: The original user query
            uncertainty_assessment: The uncertainty assessment from the agent
            context: Additional context for the dialogue
            
        Returns:
            DialogueSession with initial questions
        """
        # Generate session ID
        session_id = f"dialogue_{int(time.time())}_{hash(original_query) % 10000}"
        
        # Create dialogue session
        session = DialogueSession(
            session_id=session_id,
            original_query=original_query,
            uncertainty_assessment=uncertainty_assessment,
            current_state=DialogueState.INITIATING,
            questions_asked=[],
            responses_received=[],
            resolution=None,
            metadata=context or {},
            created_at=time.time(),
            updated_at=time.time()
        )
        
        # Generate initial questions
        questions = self.question_generator.generate_questions(
            uncertainty_assessment, original_query, context
        )
        
        # Add questions to session
        session.questions_asked = questions
        session.current_state = DialogueState.QUESTIONING
        
        # Store session
        self.active_sessions[session_id] = session
        
        return session
    
    def process_response(self, session_id: str, user_response: str) -> DialogueSession:
        """
        Process a user response in a dialogue session
        
        Args:
            session_id: ID of the dialogue session
            user_response: The user's response to the last question
            
        Returns:
            Updated DialogueSession
        """
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Record the response
        response_data = {
            'timestamp': time.time(),
            'response': user_response,
            'question_id': session.questions_asked[-1].question_id if session.questions_asked else None
        }
        session.responses_received.append(response_data)
        session.updated_at = time.time()
        
        # Update dialogue state
        session.current_state = DialogueState.PROCESSING
        
        # Determine if uncertainty is resolved
        if self._is_uncertainty_resolved(session):
            session.current_state = DialogueState.RESOLVING
            session.resolution = self._create_resolution(session)
            session.current_state = DialogueState.COMPLETED
        else:
            # Generate follow-up questions if needed
            follow_up_questions = self._generate_follow_up_questions(session)
            if follow_up_questions:
                session.questions_asked.extend(follow_up_questions)
                session.current_state = DialogueState.QUESTIONING
            else:
                # No more questions, mark as completed
                session.current_state = DialogueState.COMPLETED
        
        return session
    
    def _is_uncertainty_resolved(self, session: DialogueSession) -> bool:
        """Determine if the uncertainty has been resolved based on responses"""
        # Simple heuristic: if we have at least one response, consider it resolved
        # In a more sophisticated implementation, this would analyze the response content
        return len(session.responses_received) > 0
    
    def _create_resolution(self, session: DialogueSession) -> Dict[str, Any]:
        """Create a resolution based on the dialogue"""
        return {
            'status': 'resolved',
            'resolution_type': 'user_clarification',
            'clarifications_provided': [r['response'] for r in session.responses_received],
            'timestamp': time.time()
        }
    
    def _generate_follow_up_questions(self, session: DialogueSession) -> List[SocraticQuestion]:
        """Generate follow-up questions if needed"""
        # For now, don't generate follow-up questions
        # In a more sophisticated implementation, this would analyze the response
        # and determine if additional clarification is needed
        return []
    
    def get_session(self, session_id: str) -> Optional[DialogueSession]:
        """Get a dialogue session by ID"""
        return self.active_sessions.get(session_id)
    
    def close_session(self, session_id: str) -> Optional[DialogueSession]:
        """Close a dialogue session and return the final state"""
        session = self.active_sessions.get(session_id)
        if session:
            session.current_state = DialogueState.COMPLETED
            del self.active_sessions[session_id]
        return session


# Global instances
socratic_question_generator = SocraticQuestionGenerator()
socratic_dialogue_manager = SocraticDialogueManager()


def get_socratic_question_generator() -> SocraticQuestionGenerator:
    """Get the global Socratic question generator instance"""
    return socratic_question_generator


def get_socratic_dialogue_manager() -> SocraticDialogueManager:
    """Get the global Socratic dialogue manager instance"""
    return socratic_dialogue_manager