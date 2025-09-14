"""
Enhanced Input Processor - The "Sensory Cortex"
Implements Task 3.1.4: Enhanced Task List Generation

This is the main Input Processor that integrates all components to generate
enhanced "Processor-to-Orchestrator (Task List)" messages per PROTOCOLS.md
"""

import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict

from .parser import AdvancedParser, QueryMetadata, ParsedQuery
from .intent_recognizer import IntentRecognizer, IntentResult
from .ambiguity_resolver import AmbiguityResolver, AmbiguityDetection, DisambiguationResult

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

@dataclass
class EnhancedTaskList:
    """Enhanced Task List message per PROTOCOLS.md"""
    protocol_version: str
    query_metadata: Dict[str, Any]
    parsed_query: Dict[str, Any]
    task_list: List[Dict[str, Any]]
    ambiguity_info: Optional[Dict[str, Any]] = None
    processing_metadata: Optional[Dict[str, Any]] = None

class EnhancedInputProcessor:
    """
    Enhanced Input Processor implementing the complete "Sensory Cortex" functionality
    
    This processor:
    1. Parses complex queries into structured components
    2. Recognizes user intent with confidence scoring
    3. Resolves ambiguities or flags them for clarification
    4. Generates prioritized task lists with dependencies
    5. Produces protocol-compliant messages for the Orchestrator
    """
    
    def __init__(self):
        """Initialize the Enhanced Input Processor with all components"""
        self.parser = AdvancedParser()
        self.intent_recognizer = IntentRecognizer()
        self.ambiguity_resolver = AmbiguityResolver()
        
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
    
    def process_query(self, raw_query: str, user_context: Optional[Dict] = None) -> EnhancedTaskList:
        """
        Process a raw query into an enhanced task list
        
        Args:
            raw_query: The raw user query string
            user_context: Optional user context (session, preferences, history)
            
        Returns:
            EnhancedTaskList ready for the Orchestrator
        """
        # Step 1: Parse the query
        query_metadata, parsed_query = self.parser.parse_query(raw_query, user_context)
        
        # Step 2: Recognize intent
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
        
        # Step 4: Generate task list
        task_list = self._generate_task_list(
            parsed_query, intent_result, ambiguity_detection, disambiguation_result
        )
        
        # Step 5: Create enhanced task list message
        enhanced_task_list = EnhancedTaskList(
            protocol_version="1.0",
            query_metadata=asdict(query_metadata),
            parsed_query=asdict(parsed_query),
            task_list=[asdict(task) for task in task_list],
            ambiguity_info=self._create_ambiguity_info(ambiguity_detection, disambiguation_result),
            processing_metadata=self._create_processing_metadata(intent_result)
        )
        
        return enhanced_task_list
    
    def _generate_task_list(self, parsed_query: ParsedQuery, intent_result: IntentResult,
                          ambiguity_detection: AmbiguityDetection, 
                          disambiguation_result: Optional[DisambiguationResult]) -> List[TaskItem]:
        """Generate prioritized task list with dependencies"""
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
                estimated_time_ms=self._estimate_task_time(intent_result.primary_intent, concept)
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
                    estimated_time_ms=self._estimate_task_time('explain_impact', 'relationship')
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
                estimated_time_ms=2000
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
    
    def _create_processing_metadata(self, intent_result: IntentResult) -> Dict[str, Any]:
        """Create processing metadata for debugging and optimization"""
        return {
            'processing_timestamp': datetime.now().isoformat(),
            'processor_version': '1.0.0',
            'intent_analysis': {
                'primary_intent': intent_result.primary_intent,
                'confidence': intent_result.confidence,
                'alternatives': intent_result.alternative_intents,
                'context_factors': intent_result.context_factors
            },
            'performance_metrics': {
                'processing_time_ms': 50,  # Would be measured in real implementation
                'complexity_handled': True,
                'ambiguity_detected': intent_result.is_ambiguous
            }
        }
    
    def to_orchestrator_protocol(self, enhanced_task_list: EnhancedTaskList) -> Dict[str, Any]:
        """
        Convert enhanced task list to the standard Orchestrator protocol format
        
        This maintains backward compatibility with the existing Orchestrator
        while providing enhanced information.
        """
        # Convert to the basic protocol format expected by current Orchestrator
        basic_task_list = {
            "query_id": enhanced_task_list.query_metadata['query_id'],
            "tasks": []
        }
        
        for task_dict in enhanced_task_list.task_list:
            # Convert enhanced task to basic task format
            basic_task = {
                "task_id": task_dict['task_id'],
                "intent": task_dict['intent'],
                "concept": task_dict['concept'],
                "args": {
                    "context": task_dict['context'],
                    "priority": task_dict['priority'],
                    "confidence": task_dict['confidence']
                }
            }
            basic_task_list["tasks"].append(basic_task)
        
        return basic_task_list
