# Communication Protocols - Level 2: Neurogenesis & Network

📚 **Part 2 of 4** | [← Level 1: Foundation](protocols-level-1-foundation.md) | [Level 3: Advanced →](protocols-level-3-advanced.md) | [Migration Guide](protocols-migration.md) | [Index](../INDEX.md)

**Version**: 5.1  
**Date**: 2025-01-01  
**Status**: ✅ Implemented & Operational

**Related Documents:**
- Architecture: [`architecture-level-2-components.md`](../architecture/architecture-level-2-components.md)
- Roadmap: [`roadmap-level-2-phases.md`](../roadmap/roadmap-level-2-phases.md)
- Implementation: [`sprint-1-2-foundation.md`](../implementation/sprint-1-2-foundation.md)

---

## Overview

This document defines the neurogenesis and network protocols for the Myriad Cognitive Architecture - the **world's first implementation of true biomimetic neurogenesis protocols** enabling dynamic creation of specialized agents for unknown concepts.

**What's in Level 2:**
- Phase 2 Neurogenesis: Biomimetic Agent Creation Protocols
- Phase 2: Network Protocols (Agent-to-Agent Communication)
- Phase 3: Evolution Protocols (Graph Intelligence & Hebbian Learning)

**Prerequisites:** [Level 1: Foundation](protocols-level-1-foundation.md)  
**Next Level:** [Level 3: Advanced Features](protocols-level-3-advanced.md)

---

## Table of Contents

1. [Phase 2 Neurogenesis: Biomimetic Agent Creation](#phase-2-neurogenesis-biomimetic-agent-creation-protocols)
2. [Phase 2: Network Protocols](#phase-2-network-protocols)
3. [Phase 3: Evolution Protocols](#phase-3-evolution-protocols)

---

## Phase 2 Neurogenesis: Biomimetic Agent Creation Protocols

*The world's first implementation of true biomimetic neurogenesis protocols - enabling dynamic creation of specialized agents for unknown concepts*

### 2.1 Neurogenesis Pipeline Overview

The neurogenesis system implements a complete biomimetic pipeline that mirrors biological neural development:

1. **Unknown Concept Detection**: Orchestrator identifies concepts without existing agents
2. **Multi-Agent Research**: Existing agents collaborate to research unknown concepts  
3. **Template Selection**: AI-driven selection of appropriate agent templates
4. **Code Generation**: Dynamic creation of Flask application and Dockerfile
5. **Deployment**: Docker container instantiation and service startup
6. **Graph Registration**: Automatic registration and relationship creation

### 2.2 Unknown Concept Detection Protocol

**Purpose**: Triggered when no agent is found for a concept during graph traversal  
**Endpoint**: `POST /orchestrate` (internal to orchestrator)

**Detection Logic**:

```json
{
  "neurogenesis_trigger": {
    "concept": "quantum_computer",
    "intent": "define",
    "confidence_threshold": 0.7,
    "existing_agents_found": 0,
    "trigger_reason": "no_agent_found"
  }
}
```

### 2.3 Multi-Agent Research Protocol

**Purpose**: Orchestrated research of unknown concepts using existing agents  
**Endpoint**: `POST /collaborate`

**Research Request**:

```json
{
  "collaboration_type": "concept_research",
  "research_request": {
    "concept": "quantum_computer", 
    "intent": "define",
    "requester": "Orchestrator_Neurogenesis",
    "research_aspects": [
      "basic_definition",
      "technical_principles", 
      "applications",
      "industry_relevance"
    ]
  }
}
```

**Research Response**:

```json
{
  "research_result": {
    "agent_id": "Lightbulb_Definition_AI",
    "expertise_level": "limited",
    "research_data": {
      "definition": "A quantum computer leverages quantum mechanics...",
      "related_concepts": ["quantum_mechanics", "superposition", "computing"],
      "confidence": 0.6,
      "sources": ["quantum_physics_principles"]
    },
    "recommendations": {
      "suggested_template": "specialist_basic",
      "domain_focus": "quantum_computing"
    }
  }
}
```

### 2.4 Template Selection Protocol

**Purpose**: AI-driven selection of optimal agent template for new concept  
**Component**: Template Manager (`templates/agent_templates.py`)

**Template Selection Logic**:

```json
{
  "template_selection": {
    "concept": "quantum_computer",
    "research_analysis": {
      "complexity_score": 0.9,
      "domain_specialization": "high",
      "knowledge_type": "technical_factual"
    },
    "recommended_template": {
      "template_id": "specialist_basic",
      "confidence": 0.85,
      "customizations": {
        "knowledge_domains": ["quantum_computing", "computer_science"],
        "capabilities": ["technical_definition", "principle_explanation"]
      }
    }
  }
}
```

### 2.5 Agent Code Generation Protocol

**Purpose**: Dynamic generation of Flask application and Dockerfile for new agent  
**Component**: Dynamic Lifecycle Manager (`lifecycle/dynamic_lifecycle_manager.py`)

**Generated Agent Structure**:

```json
{
  "agent_creation": {
    "agent_name": "Quantum_Computer_Knowledge_AI",
    "container_name": "quantum_computer_specialist",
    "port": 7001,
    "capabilities": [
      "concept_definition",
      "technical_analysis", 
      "principle_explanation"
    ],
    "generated_files": {
      "flask_app": "app.py",
      "dockerfile": "Dockerfile",
      "requirements": "requirements.txt"
    }
  }
}
```

### 2.6 Dynamic Agent Deployment Protocol

**Purpose**: Docker container creation and service startup  
**Endpoint**: Internal Docker commands via subprocess

**Deployment Commands**:

```bash
# Build agent image
docker build -t quantum_computer_specialist /path/to/agent/

# Start agent container  
docker run -d --name quantum_computer_specialist \
  --network myriad-mind_default \
  -p 7001:5000 \
  quantum_computer_specialist

# Health check
curl http://quantum_computer_specialist:5000/health
```

### 2.7 Graph Registration Protocol

**Purpose**: Register new agent and create concept relationships in Neo4j  
**Endpoint**: `POST /create_node`, `POST /create_relationship`

**Agent Registration**:

```json
{
  "create_agent_node": {
    "name": "Quantum_Computer_Knowledge_AI",
    "type": "Agent", 
    "properties": {
      "endpoint": "http://quantum_computer_specialist:5000",
      "agent_type": "specialist_basic",
      "capabilities": ["concept_definition", "technical_analysis"],
      "creation_method": "neurogenesis",
      "created_at": "2025-01-01T12:00:00Z"
    }
  }
}
```

**Concept Relationship**:

```json
{
  "create_relationship": {
    "source_node": "quantum_computer",
    "target_node": "Quantum_Computer_Knowledge_AI", 
    "relationship_type": "HANDLES_CONCEPT",
    "properties": {
      "confidence": 0.8,
      "creation_method": "neurogenesis",
      "weight": 1.0
    }
  }
}
```

### 2.8 Neurogenesis Success Response

**Purpose**: Final response indicating successful neurogenesis completion  
**Format**: Standard orchestrator response with neurogenesis metadata

```json
{
  "task_id": 1,
  "agent": "Orchestrator_Neurogenesis", 
  "status": "neurogenesis_with_agent_creation",
  "result": {
    "concept_researched": "quantum_computer",
    "agent_created": "Quantum_Computer_Knowledge_AI",
    "endpoint": "http://quantum_computer_specialist:5000",
    "confidence": 0.85,
    "capabilities": ["concept_definition", "technical_analysis"]
  },
  "neurogenesis_metadata": {
    "research_sources": ["Lightbulb_Definition_AI", "Lightbulb_Function_AI"],
    "template_used": "specialist_basic", 
    "deployment_time": "3.2s",
    "graph_registered": true
  }
}
```

---

## Phase 2: Network Protocols

*Enables direct agent-to-agent communication and cluster coordination*

### 2.1 Agent-to-Agent Direct Communication

**Purpose**: Enable agents to communicate directly without orchestrator mediation

**Direct Query Protocol**: `Agent A → Agent B`

```json
{
  "direct_communication": {
    "protocol_version": "2.0",
    "communication_type": "peer_query",
    "source_agent": {
      "agent_id": "lightbulb_fact_001",
      "cluster_id": "industrial_technology"
    },
    "target_agent": {
      "agent_id": "factory_history_001",
      "cluster_id": "historical_analysis"
    },
    "query_context": {
      "original_user_query": "Why was the lightbulb important for factories?",
      "current_task": "building_historical_context",
      "collaboration_reason": "need_pre_electric_factory_conditions"
    },
    "specific_request": {
      "intent": "provide_context",
      "concept": "factory_working_conditions_1870s",
      "required_aspects": ["lighting_conditions", "working_hours", "productivity_limitations"],
      "response_format": "structured_facts"
    }
  }
}
```

**Direct Response Protocol**: `Agent B → Agent A`

```json
{
  "direct_response": {
    "protocol_version": "2.0", 
    "response_to": "lightbulb_fact_001",
    "collaboration_success": true,
    "contextual_data": {
      "factory_conditions_1870s": {
        "lighting": "primarily_daylight_candles_gas",
        "avg_working_hours": 9.5,
        "seasonal_variation": "30_percent_reduction_winter",
        "safety_incidents": "high_due_to_open_flames"
      },
      "productivity_impact": {
        "daylight_efficiency": 1.0,
        "artificial_light_efficiency": 0.45,
        "night_work_feasibility": "very_limited"
      }
    },
    "collaboration_metadata": {
      "response_confidence": 0.89,
      "data_freshness": "historical_archives_2023",
      "suggests_further_collaboration": [
        {
          "agent_id": "industrial_revolution_timeline_001",
          "reason": "can_provide_adoption_timeline"
        }
      ]
    }
  }
}
```

### 2.2 Cluster Coordination Protocol

**Purpose**: Manage agent clusters and optimize intra-cluster communication

**Cluster Formation**: `Registry → Cluster Manager`

```json
{
  "cluster_management": {
    "action": "form_cluster",
    "cluster_definition": {
      "cluster_id": "industrial_technology_v2",
      "concept_domain": "industrial_technology",
      "specialization_level": "detailed",
      "member_agents": [
        {
          "agent_id": "lightbulb_fact_001",
          "role": "primary_fact_provider",
          "specialization": "electric_lighting"
        },
        {
          "agent_id": "electricity_history_001", 
          "role": "contextual_support",
          "specialization": "electrical_development"
        },
        {
          "agent_id": "industrial_innovation_001",
          "role": "impact_analyzer", 
          "specialization": "technology_adoption"
        }
      ]
    },
    "coordination_rules": {
      "load_balancing": "round_robin_with_specialization_preference",
      "fallback_strategy": "cross_cluster_escalation",
      "performance_optimization": "cache_frequent_collaborations"
    }
  }
}
```

### 2.3 Event-Driven Messaging Protocol

**Purpose**: Asynchronous communication via message broker

**Event Publication**: `Agent → Event Broker`

```json
{
  "event_publication": {
    "event_type": "knowledge_update",
    "source_agent": "lightbulb_fact_001",
    "event_data": {
      "concept": "lightbulb",
      "update_type": "new_historical_context",
      "updated_knowledge": {
        "discovery": "Early factory adoption faster in textile industry",
        "evidence_quality": "high",
        "impact_on_queries": ["factory_productivity", "industrial_adoption_patterns"]
      }
    },
    "publication_metadata": {
      "timestamp": "2024-01-01T15:30:00Z",
      "relevance_topics": ["industrial_history", "technology_adoption"],
      "suggested_subscribers": ["factory_*", "industrial_*", "productivity_*"]
    }
  }
}
```

---

## Phase 3: Evolution Protocols

*Supports dynamic growth, learning, and graph-based intelligence*

### 3.1 Graph Database Schema

**Purpose**: Rich knowledge representation and traversal-based agent discovery

**Node Schema**: `Agent Nodes`

```json
{
  "node_type": "agent_node",
  "properties": {
    "agent_id": "lightbulb_fact_001",
    "agent_type": "fact_base",
    "concept_domain": "electrical_technology",
    "specialization_level": 0.85,
    "capabilities": ["define", "explain_properties", "historical_context"],
    "knowledge_depth": {
      "primary_concepts": ["lightbulb", "incandescent_lighting"],
      "secondary_concepts": ["electricity", "industrial_applications"],
      "tertiary_concepts": ["manufacturing", "innovation_adoption"]
    },
    "performance_metrics": {
      "avg_confidence": 0.94,
      "response_time_p95": 60,
      "collaboration_success_rate": 0.91,
      "query_satisfaction_score": 4.7
    },
    "learning_metadata": {
      "creation_date": "2024-01-01T00:00:00Z",
      "last_knowledge_update": "2024-01-01T12:00:00Z",
      "adaptation_count": 23,
      "neurogenesis_generation": 1
    }
  }
}
```

**Relationship Schema**: `Agent Collaboration Edges`

```json
{
  "relationship_type": "COLLABORATES_WITH",
  "source_node": "lightbulb_fact_001",
  "target_node": "factory_history_001", 
  "properties": {
    "collaboration_weight": 0.78,
    "activation_frequency": 47,
    "success_rate": 0.89,
    "hebbian_strength": 0.82,
    "collaboration_contexts": [
      "industrial_history_queries",
      "technology_impact_analysis",
      "productivity_studies"
    ],
    "performance_metrics": {
      "avg_combined_confidence": 0.91,
      "response_time_improvement": 0.23,
      "user_satisfaction_boost": 0.15
    },
    "learning_evolution": {
      "initial_weight": 0.1,
      "growth_rate": 0.68,
      "last_strengthening": "2024-01-01T14:45:00Z",
      "strengthening_trigger": "successful_collaboration"
    }
  }
}
```

**Graph Traversal Query Protocol**: `Orchestrator → Graph Database`

```json
{
  "graph_query": {
    "query_type": "find_optimal_agent_path",
    "start_concepts": ["lightbulb", "factories"],
    "target_intent": "explain_importance",
    "traversal_parameters": {
      "max_path_length": 4,
      "min_confidence_threshold": 0.7,
      "collaboration_weight_preference": 0.8,
      "avoid_overloaded_agents": true
    },
    "optimization_criteria": [
      "minimize_total_response_time",
      "maximize_combined_confidence",
      "prefer_proven_collaborations"
    ]
  }
}
```

### 3.2 Neurogenesis Protocol

**Purpose**: Dynamic agent creation when encountering unknown concepts

**Agent Creation Request**: `Lifecycle Manager → Agent Factory`

```json
{
  "neurogenesis_request": {
    "trigger_context": {
      "unknown_concept": "LED_lighting",
      "query_context": "Modern factory lighting comparison",
      "knowledge_gap": "no_agent_handles_LED_technology",
      "urgency_level": "medium"
    },
    "agent_specification": {
      "proposed_agent_type": "fact_base",
      "concept_specialization": "LED_lighting", 
      "knowledge_scope": {
        "primary_focus": "LED_technology_facts",
        "secondary_focus": ["energy_efficiency", "industrial_applications"],
        "knowledge_sources": ["LED_technical_specifications", "industrial_lighting_standards"]
      },
      "integration_cluster": "lighting_technology"
    },
    "scaffolding_requirements": {
      "initial_knowledge_base": "LED_basics_curated_dataset",
      "collaboration_bootstrapping": [
        {
          "mentor_agent": "lightbulb_fact_001",
          "knowledge_transfer": "lighting_fundamentals"
        },
        {
          "collaboration_partner": "energy_efficiency_001",
          "synergy_area": "power_consumption_analysis"
        }
      ]
    }
  }
}
```

**Agent Integration Protocol**: `New Agent → Network Integration`

```json
{
  "integration_protocol": {
    "new_agent_metadata": {
      "agent_id": "LED_lighting_fact_001",
      "generation": 2,
      "parent_agents": ["lightbulb_fact_001"],
      "knowledge_inheritance": ["lighting_principles", "industrial_applications"]
    },
    "network_integration": {
      "cluster_assignment": "lighting_technology_expanded",
      "initial_relationships": [
        {
          "target_agent": "lightbulb_fact_001",
          "relationship_type": "SPECIALIZATION_OF",
          "initial_weight": 0.6
        },
        {
          "target_agent": "energy_efficiency_001", 
          "relationship_type": "COLLABORATES_WITH",
          "initial_weight": 0.3
        }
      ]
    },
    "learning_initialization": {
      "bootstrap_training": "LED_knowledge_base_v1.0",
      "initial_confidence_baseline": 0.75,
      "learning_rate": 0.05,
      "collaboration_learning_enabled": true
    }
  }
}
```

### 3.3 Hebbian Learning Protocol (✅ IMPLEMENTED)

**Purpose**: Strengthen agent-to-concept connectivity based on successful activations; decay unused connections.

**Learning Event**: `Collaboration Monitor → Learning Engine`

```json
{
  "hebbian_learning_event": {
    "agent_id": "Lightbulb_Definition_AI",
    "concept": "lightbulb",
    "success": true,
    "edge": "HANDLES_CONCEPT"
  }
}
```

#### 3.3.1 Endpoints

- `POST /hebbian/strengthen`
  - Request:

  ```json
  {"agent_id":"Lightbulb_Definition_AI","concept":"lightbulb","success":true}
  ```

  - Response: `{"status":"success","relationship": {"weight":0.62,...}}`

- `POST /hebbian/decay`
  - Request:

  ```json
  {"concept":"lightbulb","decay_rate":0.05}
  ```

  - Response: `{"status":"success","decayed":N}`

- `POST /get_agents_for_concept`
  - Request: `{"concept":"lightbulb"}`
  - Response: agents with relationship properties including `weight`.

#### 3.3.2 Orchestrator Hook

Upon each agent outcome, the orchestrator invokes `/hebbian/strengthen` with `success` reflecting the outcome.

#### 3.3.3 Routing Integration

Enhanced Graph Intelligence incorporates `weight` into relevance scoring (10% contribution by default).

---

## Continue Reading

- **Previous:** [Level 1: Foundation Protocols](protocols-level-1-foundation.md) - Basic communication and graph database
- **Next:** [Level 3: Advanced Protocols](protocols-level-3-advanced.md) - Multi-modal learning and autonomous cognition
- **Implementation:** [Sprint 1-2: Foundation](../implementation/sprint-1-2-foundation.md) - Neurogenesis implementation guide
- **Architecture:** [Components Deep-Dive](../architecture/architecture-level-2-components.md)
- **Index:** [Documentation Home](../INDEX.md)

---

**Neurogenesis & network protocols complete** | Next: Advanced features and autonomous cognition →