#!/usr/bin/env python3
"""
Agent Template System for Dynamic Neurogenesis
Defines templates for creating specialized agents dynamically.

This supports Phase 2 of biomimetic neurogenesis where we create 
template-based agents for new concepts discovered during expansion.
"""

import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class AgentType(Enum):
    FACTBASE = "FactBase"
    FUNCTION_EXECUTOR = "FunctionExecutor"
    ANALYZER = "Analyzer"
    SPECIALIST = "Specialist"

class SpecializationLevel(Enum):
    BASIC = "basic"          # Simple knowledge storage and retrieval
    ENHANCED = "enhanced"    # Includes basic reasoning and relationships
    ADVANCED = "advanced"    # Full autonomous learning and adaptation

@dataclass
class AgentTemplate:
    """Template for creating specialized agents"""
    template_id: str
    name_pattern: str          # e.g., "{concept}_Definition_AI"
    agent_type: AgentType
    specialization_level: SpecializationLevel
    primary_capabilities: List[str]
    knowledge_domains: List[str]
    collaboration_types: List[str]
    flask_routes: List[str]
    dependencies: List[str]
    port_range: tuple          # (start_port, end_port)
    docker_base_image: str
    startup_script: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        result['agent_type'] = self.agent_type.value
        result['specialization_level'] = self.specialization_level.value
        return result

class AgentTemplateManager:
    """Manages agent templates and instantiation"""
    
    def __init__(self):
        self.templates = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default agent templates"""
        
        # Basic FactBase Template
        factbase_template = AgentTemplate(
            template_id="factbase_basic",
            name_pattern="{concept}_Definition_AI",
            agent_type=AgentType.FACTBASE,
            specialization_level=SpecializationLevel.BASIC,
            primary_capabilities=[
                "concept_definition",
                "knowledge_storage",
                "fact_retrieval",
                "basic_relationships"
            ],
            knowledge_domains=["{concept}"],
            collaboration_types=[
                "knowledge_request",
                "context_sharing",
                "concept_research"
            ],
            flask_routes=[
                "/health", 
                "/collaborate",
                "/query",
                "/update_knowledge"
            ],
            dependencies=[
                "flask",
                "requests", 
                "json"
            ],
            port_range=(6000, 6999),
            docker_base_image="python:3.11-slim",
            startup_script="app.py"
        )
        
        # Enhanced FactBase Template
        factbase_enhanced = AgentTemplate(
            template_id="factbase_enhanced",
            name_pattern="{concept}_Knowledge_AI",
            agent_type=AgentType.FACTBASE,
            specialization_level=SpecializationLevel.ENHANCED,
            primary_capabilities=[
                "concept_definition",
                "knowledge_storage", 
                "fact_retrieval",
                "relationship_analysis",
                "context_inference",
                "knowledge_synthesis"
            ],
            knowledge_domains=["{concept}"],
            collaboration_types=[
                "knowledge_request",
                "context_sharing", 
                "concept_research",
                "knowledge_synthesis",
                "relationship_mapping"
            ],
            flask_routes=[
                "/health",
                "/collaborate", 
                "/query",
                "/update_knowledge",
                "/analyze_relationships",
                "/synthesize"
            ],
            dependencies=[
                "flask",
                "requests",
                "json",
                "networkx"
            ],
            port_range=(7000, 7999),
            docker_base_image="python:3.11-slim",
            startup_script="app.py"
        )
        
        # Function Executor Template
        function_template = AgentTemplate(
            template_id="function_basic",
            name_pattern="{concept}_Function_AI",
            agent_type=AgentType.FUNCTION_EXECUTOR,
            specialization_level=SpecializationLevel.BASIC,
            primary_capabilities=[
                "function_execution",
                "impact_analysis",
                "application_assessment",
                "performance_evaluation"
            ],
            knowledge_domains=["{concept}"],
            collaboration_types=[
                "function_execution",
                "knowledge_request",
                "context_sharing",
                "impact_analysis"
            ],
            flask_routes=[
                "/health",
                "/collaborate",
                "/execute",
                "/analyze_impact",
                "/evaluate"
            ],
            dependencies=[
                "flask",
                "requests",
                "json",
                "numpy"
            ],
            port_range=(8000, 8999),
            docker_base_image="python:3.11-slim",
            startup_script="app.py"
        )
        
        # Specialist Template (for domain-specific expertise)
        specialist_template = AgentTemplate(
            template_id="specialist_basic",
            name_pattern="{concept}_Specialist_AI",
            agent_type=AgentType.SPECIALIST,
            specialization_level=SpecializationLevel.ENHANCED,
            primary_capabilities=[
                "domain_expertise",
                "specialized_analysis",
                "expert_recommendations",
                "domain_relationships",
                "trend_analysis"
            ],
            knowledge_domains=["{concept}"],
            collaboration_types=[
                "expert_consultation",
                "knowledge_request",
                "context_sharing",
                "specialized_analysis",
                "recommendation_generation"
            ],
            flask_routes=[
                "/health",
                "/collaborate",
                "/consult",
                "/analyze", 
                "/recommend",
                "/explain"
            ],
            dependencies=[
                "flask",
                "requests",
                "json",
                "sklearn",
                "pandas"
            ],
            port_range=(9000, 9999),
            docker_base_image="python:3.11-slim",
            startup_script="app.py"
        )
        
        # Register templates
        self.templates = {
            "factbase_basic": factbase_template,
            "factbase_enhanced": factbase_enhanced,
            "function_basic": function_template,
            "specialist_basic": specialist_template
        }
    
    def get_template(self, template_id: str) -> Optional[AgentTemplate]:
        """Get a specific template"""
        return self.templates.get(template_id)
    
    def list_templates(self) -> List[str]:
        """List available template IDs"""
        return list(self.templates.keys())
    
    def get_templates_by_type(self, agent_type: AgentType) -> List[AgentTemplate]:
        """Get all templates of a specific type"""
        return [t for t in self.templates.values() if t.agent_type == agent_type]
    
    def suggest_template(self, concept: str, intent: str, research_data: Dict[str, Any]) -> str:
        """Suggest the best template for a concept based on research data"""
        
        # Analyze the research data to determine the best template
        confidence = research_data.get("confidence_score", 0.0)
        applications = research_data.get("applications", [])
        knowledge_complexity = len(research_data.get("related_concepts", []))
        
        # Simple heuristics for template selection
        if intent in ["define", "explain", "describe"]:
            # Definitional queries suggest FactBase agents
            if confidence > 0.7 or knowledge_complexity > 3:
                return "factbase_enhanced"
            else:
                return "factbase_basic"
                
        elif intent in ["analyze", "impact", "evaluate"]:
            # Analytical queries suggest Function agents
            return "function_basic"
            
        elif intent in ["recommend", "optimize", "improve"]:
            # Advisory queries suggest Specialist agents
            return "specialist_basic"
            
        else:
            # Default to basic FactBase for unknown intents
            return "factbase_basic"
    
    def customize_template(self, template_id: str, concept: str, 
                          research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Customize a template for a specific concept"""
        
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Create customized agent specification
        customized = template.to_dict()
        
        # Customize for the specific concept
        customized["agent_name"] = template.name_pattern.format(concept=concept.title().replace(" ", "_"))
        customized["concept"] = concept
        customized["knowledge_domains"] = [concept.lower()]
        
        # Add research data
        customized["initial_knowledge"] = research_data
        customized["research_sources"] = research_data.get("research_sources", [])
        customized["confidence_level"] = research_data.get("confidence_score", 0.0)
        
        # Generate unique identifiers
        customized["container_name"] = concept.lower().replace(" ", "_") + "_" + template.agent_type.value.lower()
        customized["service_name"] = customized["container_name"] 
        
        return customized

# Global template manager instance
template_manager = AgentTemplateManager()

def get_template_manager() -> AgentTemplateManager:
    """Get the global template manager instance"""
    return template_manager

if __name__ == "__main__":
    # Demo the template system
    manager = get_template_manager()
    
    print("🧬 Agent Template System Demo")
    print("=" * 40)
    
    print(f"Available templates: {manager.list_templates()}")
    
    # Example: Create an agent for "LED" concept
    concept = "LED"
    intent = "define"
    research_data = {
        "concept": concept,
        "confidence_score": 0.8,
        "applications": ["lighting", "displays", "indicators"],
        "related_concepts": ["light", "semiconductor", "electricity"],
        "research_sources": ["Lightbulb_Definition_AI"]
    }
    
    suggested_template = manager.suggest_template(concept, intent, research_data)
    print(f"\nSuggested template for '{concept}': {suggested_template}")
    
    customized_agent = manager.customize_template(suggested_template, concept, research_data)
    print(f"\nCustomized agent spec:")
    print(json.dumps(customized_agent, indent=2))
