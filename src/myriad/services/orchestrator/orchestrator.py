import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import time
import os
import sys
import urllib.parse
from typing import Optional, Dict, Any, List

# The Orchestrator now communicates with the GraphDB Manager, not the old registry.
from myriad.core.lifecycle.dynamic_lifecycle_manager import get_lifecycle_manager
from myriad.core.learning.autonomous_learning_engine import get_learning_engine
from myriad.core.intelligence.enhanced_graph_intelligence import get_enhanced_intelligence
from myriad.core.optimization.performance_engine import get_performance_engine

GRAPHDB_MANAGER_URL = "http://graphdb_manager_ai:5008"

# Persistent HTTP session with retries/backoff (env-tunable)
SESSION_RETRIES = int(os.environ.get("HTTP_RETRIES", "3"))
SESSION_BACKOFF = float(os.environ.get("HTTP_BACKOFF", "0.3"))
SESSION_POOL_MAX = int(os.environ.get("HTTP_POOL_MAX", "20"))

_http_session = requests.Session()
_adapter = HTTPAdapter(
    pool_connections=SESSION_POOL_MAX,
    pool_maxsize=SESSION_POOL_MAX,
    max_retries=Retry(
        total=SESSION_RETRIES,
        connect=SESSION_RETRIES,
        read=SESSION_RETRIES,
        backoff_factor=SESSION_BACKOFF,
        status_forcelist=[502, 503, 504],
        allowed_methods=["GET", "POST"]
    ),
)
_http_session.mount("http://", _adapter)
_http_session.mount("https://", _adapter)

# Agent endpoints for concept research
LIGHTBULB_DEFINITION_AI_URL = "http://lightbulb_definition_ai:5001"
LIGHTBULB_FUNCTION_AI_URL = "http://lightbulb_function_ai:5002"

# Dynamic agent creation (Phase 2 Neurogenesis)
ENABLE_DYNAMIC_AGENTS = os.environ.get("ENABLE_DYNAMIC_AGENTS", "true").lower() == "true"

# Autonomous learning (Phase 3 Neurogenesis)
ENABLE_AUTONOMOUS_LEARNING = os.environ.get("ENABLE_AUTONOMOUS_LEARNING", "true").lower() == "true"

# Import lifecycle manager for dynamic agent creation
try:
    lifecycle_manager = get_lifecycle_manager()
    LIFECYCLE_MANAGER_AVAILABLE = True
    print("🧬 Dynamic Lifecycle Manager loaded successfully")
except ImportError as e:
    lifecycle_manager = None
    LIFECYCLE_MANAGER_AVAILABLE = False
    print(f"⚠️  Dynamic Lifecycle Manager not available: {e}")

# Import autonomous learning engine for Phase 3 neurogenesis
try:
    learning_engine = get_learning_engine()
    LEARNING_ENGINE_AVAILABLE = True
    print("🧠 Autonomous Learning Engine loaded successfully")
except ImportError as e:
    learning_engine = None
    LEARNING_ENGINE_AVAILABLE = False
    print(f"⚠️  Autonomous Learning Engine not available: {e}")

# Import enhanced graph intelligence for smart agent selection
try:
    enhanced_intelligence = get_enhanced_intelligence()
    ENHANCED_INTELLIGENCE_AVAILABLE = True
    print("🎯 Enhanced Graph Intelligence loaded successfully")
except ImportError as e:
    enhanced_intelligence = None
    ENHANCED_INTELLIGENCE_AVAILABLE = False
    print(f"⚠️  Enhanced Graph Intelligence not available: {e}")

# Import performance optimization engine for maximum performance
try:
    performance_engine = get_performance_engine()
    PERFORMANCE_OPTIMIZATION_AVAILABLE = True
    print("🚀 Performance Optimization Engine loaded successfully")
except ImportError as e:
    performance_engine = None
    PERFORMANCE_OPTIMIZATION_AVAILABLE = False
    print(f"⚠️  Performance Optimization Engine not available: {e}")

async def optimized_graph_query(operation: str, endpoint: str, payload: Dict[str, Any], 
                               cache_key: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Execute optimized graph database query with performance optimizations"""
    
    if PERFORMANCE_OPTIMIZATION_AVAILABLE and cache_key:
        try:
            # Use optimized query with caching and performance tracking
            result = await performance_engine.optimized_query(
                operation=operation,
                query=f"HTTP_REQUEST:{endpoint}",  # Virtual query for tracking
                parameters=payload,
                cache_key_data=cache_key,
                use_cache=True
            )
            
            # The performance engine expects Neo4j queries, but we need HTTP requests
            # So we'll use it for caching and monitoring, but still make HTTP calls
            if result.get('cached'):
                return result['data']
                
        except Exception as e:
            print(f"⚠️ Performance optimization error, falling back to direct query: {e}")
    
    # Fallback to direct HTTP request
    try:
        response = _http_session.post(f"{GRAPHDB_MANAGER_URL}{endpoint}", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Cache the result if performance optimization is available
            if PERFORMANCE_OPTIMIZATION_AVAILABLE and cache_key:
                try:
                    await performance_engine.cache.set(
                        "graph_query", 
                        cache_key, 
                        data
                    )
                except:
                    pass  # Cache error doesn't affect functionality
            
            return data
        return None
    except requests.exceptions.RequestException as e:
        print(f"Graph query error for {operation}: {e}")
        return None

def check_concept_exists(concept: str) -> bool:
    """Check if a concept node already exists in the graph (optimized)"""
    
    cache_key = {
        "operation": "concept_exists",
        "concept": concept.lower(),
        "query_type": "existence_check"
    }
    
    async def _check_concept():
        result = await optimized_graph_query(
            operation="check_concept_exists",
            endpoint="/find_connected_nodes",
            payload={
                "start_node_label": "Concept",
                "start_node_properties": {"name": concept.lower()},
                "relationship_type": "HANDLES_CONCEPT",
                "relationship_direction": "in",
                "target_node_label": "Agent"
            },
            cache_key=cache_key
        )
        
        if result:
            return len(result.get("nodes", [])) > 0
        return False
    
    # For now, we'll use synchronous version with future async optimization
    try:
        payload = {
            "start_node_label": "Concept",
            "start_node_properties": {"name": concept.lower()},
            "relationship_type": "HANDLES_CONCEPT",
            "relationship_direction": "in",
            "target_node_label": "Agent"
        }
        
        start_time = time.time()
        response = _http_session.post(f"{GRAPHDB_MANAGER_URL}/find_connected_nodes", json=payload, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            exists = len(data.get("nodes", [])) > 0
            
            # Track performance if available
            if PERFORMANCE_OPTIMIZATION_AVAILABLE:
                try:
                    performance_engine.monitor.record_metric(
                        operation="check_concept_exists",
                        response_time=time.time() - start_time,
                        cache_hit=False,
                        query_complexity=1,
                        compression_ratio=1.0,
                        error_count=0
                    )
                except:
                    pass
            
            return exists
        return False
    except requests.exceptions.RequestException as e:
        # Track error if performance engine available
        if PERFORMANCE_OPTIMIZATION_AVAILABLE:
            try:
                performance_engine.monitor.record_metric(
                    operation="check_concept_exists",
                    response_time=time.time() - start_time if 'start_time' in locals() else 0.0,
                    cache_hit=False,
                    query_complexity=1,
                    compression_ratio=1.0,
                    error_count=1
                )
            except:
                pass
                
        print(f"Error checking concept existence for '{concept}': {e}")
        return False

def research_unknown_concept(concept: str, intent: str) -> Dict[str, Any]:
    """Research an unknown concept using existing agents"""
    print(f"🧠 NEUROGENESIS: Researching unknown concept '{concept}' for intent '{intent}'")
    
    research_data = {
        "concept": concept,
        "intent": intent,
        "research_timestamp": time.time(),
        "research_sources": [],
        "knowledge_gathered": {},
        "related_concepts": [],
        "confidence_score": 0.0
    }
    
    # Use existing agents to research the concept through collaboration
    research_agents = [
        {"name": "Lightbulb_Definition_AI", "url": LIGHTBULB_DEFINITION_AI_URL, "expertise": "technical_definitions"},
        {"name": "Lightbulb_Function_AI", "url": LIGHTBULB_FUNCTION_AI_URL, "expertise": "functional_analysis"}
    ]
    
    for agent in research_agents:
        print(f"  📚 Requesting research assistance from {agent['name']}...")
        research_result = request_concept_research(agent, concept, intent)
        if research_result:
            research_data["knowledge_gathered"][agent['expertise']] = research_result
            research_data["research_sources"].append(agent["name"])
    
    # Synthesize research results
    synthesized_knowledge = synthesize_research_results(research_data)
    research_data.update(synthesized_knowledge)
    
    return research_data

def request_concept_research(agent: Dict[str, str], concept: str, intent: str) -> Optional[Dict[str, Any]]:
    """Request an agent to research an unknown concept"""
    collaboration_request = {
        "source_agent": {"name": "Orchestrator_Neurogenesis", "type": "ConceptResearcher"},
        "collaboration_type": "knowledge_request",
        "target_concept": concept,
        "specific_request": {
            "knowledge_type": "concept_research",
            "research_depth": "comprehensive",
            "focus_areas": [intent, "definition", "relationships", "applications"]
        },
        "context": {
            "neurogenesis_trigger": True,
            "unknown_concept": concept,
            "original_intent": intent,
            "research_purpose": "concept_expansion"
        }
    }
    
    try:
        response = _http_session.post(f"{agent['url']}/collaborate", json=collaboration_request, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                return result.get("data")
            elif result.get("status") == "no_expertise":
                print(f"    ℹ️  {agent['name']} has no expertise in '{concept}'")
                return None
        else:
            print(f"    ⚠️  Research request failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"    ❌ Research request error: {e}")
    
    return None

def synthesize_research_results(research_data: Dict[str, Any]) -> Dict[str, Any]:
    """Synthesize research results into a coherent concept understanding"""
    knowledge = research_data.get("knowledge_gathered", {})
    concept = research_data.get("concept", "unknown")
    
    synthesized = {
        "primary_definition": "",
        "key_attributes": [],
        "related_concepts": [],
        "applications": [],
        "confidence_score": 0.0
    }
    
    # Extract and combine knowledge from different sources
    definitions = []
    attributes = []
    applications = []
    confidence_scores = []
    
    for expertise, data in knowledge.items():
        if isinstance(data, dict):
            # Extract primary knowledge
            if "primary_knowledge" in data:
                definitions.append(data["primary_knowledge"])
            
            # Extract confidence scores
            if "confidence" in data:
                confidence_scores.append(data["confidence"])
            
            # Extract additional context if available
            if "additional_context" in data:
                context = data["additional_context"]
                if isinstance(context, dict):
                    for key, value in context.items():
                        if "application" in key.lower() or "impact" in key.lower():
                            applications.append(str(value))
    
    # Synthesize primary definition
    if definitions:
        synthesized["primary_definition"] = f"Based on research: {' | '.join(definitions[:2])}"
    else:
        synthesized["primary_definition"] = f"Unknown concept '{concept}' requires further research"
    
    # Calculate confidence
    if confidence_scores:
        synthesized["confidence_score"] = sum(confidence_scores) / len(confidence_scores)
    else:
        synthesized["confidence_score"] = 0.1  # Low confidence for unknown concepts
    
    # Extract related concepts and applications
    synthesized["applications"] = applications[:3]  # Top 3 applications
    synthesized["related_concepts"] = [concept.lower()]  # At minimum, relate to itself
    
    return synthesized

def create_concept_node(concept: str, research_data: Dict[str, Any]) -> bool:
    """Create a rich concept node in the graph with researched data"""
    print(f"🔬 Creating rich concept node for '{concept}'...")
    
    node_properties = {
        "name": concept.lower(),
        "display_name": concept,
        "type": "researched_concept",
        "creation_method": "neurogenesis_research",
        "creation_timestamp": research_data.get("research_timestamp", time.time()),
        "primary_definition": research_data.get("primary_definition", ""),
        "confidence_score": research_data.get("confidence_score", 0.0),
        "research_sources": json.dumps(research_data.get("research_sources", [])),
        "key_attributes": json.dumps(research_data.get("key_attributes", [])),
        "related_concepts": json.dumps(research_data.get("related_concepts", [])),
        "applications": json.dumps(research_data.get("applications", [])),
        "original_intent": research_data.get("intent", ""),
        "research_status": "active"
    }
    
    try:
        # Create the concept node
        create_payload = {
            "label": "Concept",
            "properties": node_properties
        }
        
        response = _http_session.post(f"{GRAPHDB_MANAGER_URL}/create_node", json=create_payload, timeout=10)
        
        if response.status_code == 201:
            result = response.json()
            node_id = result.get("node_id")
            print(f"  ✅ Created concept node '{concept}' (ID: {node_id})")
            return True
        else:
            print(f"  ❌ Failed to create concept node: {response.status_code}")
            print(f"     Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error creating concept node: {e}")
        return False

def create_dynamic_agent(concept: str, intent: str, research_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create a dynamic agent for a concept (Phase 2 Neurogenesis)"""
    
    if not LIFECYCLE_MANAGER_AVAILABLE or not ENABLE_DYNAMIC_AGENTS:
        print(f"  ⚠️  Dynamic agent creation disabled or unavailable")
        return None
    
    print(f"🧬 PHASE 2 NEUROGENESIS: Creating dynamic agent for '{concept}'")
    
    try:
        # Create the dynamic agent, defaulting to the "General" region
        agent = lifecycle_manager.create_agent(concept, intent, research_data, region="General")
        
        if agent:
            print(f"  ✅ Dynamic agent created: {agent.agent_name}")
            print(f"     Agent ID: {agent.agent_id}")
            print(f"     Endpoint: {agent.endpoint}")
            print(f"     Capabilities: {', '.join(agent.capabilities)}")
            
            # Register the agent in the graph database
            agent_registration_success = register_dynamic_agent_in_graph(agent, concept)
            
            # Start autonomous learning (Phase 3 Neurogenesis)
            learning_session_id = None
            if LEARNING_ENGINE_AVAILABLE and ENABLE_AUTONOMOUS_LEARNING:
                learning_session_id = start_autonomous_learning(agent, concept, intent)
            
            return {
                "agent_id": agent.agent_id,
                "agent_name": agent.agent_name,
                "endpoint": agent.endpoint,
                "status": agent.status.value,
                "capabilities": agent.capabilities,
                "graph_registered": agent_registration_success,
                "learning_session": learning_session_id
            }
        else:
            print(f"  ❌ Failed to create dynamic agent for '{concept}'")
            return None
            
    except Exception as e:
        print(f"  ❌ Dynamic agent creation error: {e}")
        return None

def start_autonomous_learning(agent, concept: str, intent: str) -> Optional[str]:
    """Start autonomous learning for a newly created agent (Phase 3 Neurogenesis)"""
    
    print(f"🧠 PHASE 3 NEUROGENESIS: Starting autonomous learning for '{agent.agent_name}'")
    
    try:
        # Define learning objectives based on intent and agent type
        learning_objectives = generate_learning_objectives(concept, intent, agent.capabilities)
        
        # Start autonomous learning session
        session_id = learning_engine.initiate_autonomous_learning(
            agent_name=agent.agent_name,
            concept=concept,
            learning_objectives=learning_objectives
        )
        
        print(f"  ✅ Autonomous learning started: Session {session_id}")
        print(f"     Learning objectives: {', '.join(learning_objectives)}")
        
        return session_id
        
    except Exception as e:
        print(f"  ❌ Autonomous learning startup error: {e}")
        return None

def generate_learning_objectives(concept: str, intent: str, capabilities: List[str]) -> List[str]:
    """Generate learning objectives for an agent based on its concept and capabilities"""
    
    objectives = []
    
    # Base objectives for all agents
    objectives.extend([
        "understand_core_definition",
        "identify_key_principles",
        "map_relationships"
    ])
    
    # Intent-specific objectives
    if intent in ["define", "explain"]:
        objectives.extend([
            "develop_explanation_skills",
            "build_knowledge_depth"
        ])
    elif intent in ["analyze", "evaluate"]:
        objectives.extend([
            "develop_analytical_reasoning",
            "understand_applications"
        ])
    elif intent in ["compare", "relate"]:
        objectives.extend([
            "identify_comparisons",
            "understand_relationships"
        ])
    
    # Capability-specific objectives
    if "advanced_reasoning" in capabilities:
        objectives.append("develop_complex_reasoning")
    
    if "expert_consultation" in capabilities:
        objectives.append("achieve_expert_level_knowledge")
    
    if "use_case_analysis" in capabilities:
        objectives.append("master_practical_applications")
    
    # Remove duplicates and limit to reasonable number
    objectives = list(set(objectives))[:6]  # Limit to 6 objectives
    
    return objectives

def _update_agent_performance_metrics(agent_url: str, concept: str, intent: str, 
                                     start_time: float, result: dict, success: bool):
    """Update agent performance metrics in Enhanced Graph Intelligence"""
    
    if not ENHANCED_INTELLIGENCE_AVAILABLE:
        return
    
    try:
        # Calculate performance metrics
        response_time = time.time() - start_time
        
        # Extract agent ID from URL
        agent_id = _extract_agent_id_from_url(agent_url)
        if not agent_id:
            return
        
        # Calculate performance scores
        performance_data = {
            'response_time': response_time,
            'success_rate': 1.0 if success else 0.0,
            'last_request_time': time.time()
        }
        
        # Add quality scores based on result
        if success and result:
            status = result.get('status', 'unknown')
            
            if status == 'success':
                performance_data['response_quality'] = 0.9
                performance_data['accuracy'] = 0.85
                performance_data['helpfulness'] = 0.8
            elif status == 'partial':
                performance_data['response_quality'] = 0.6
                performance_data['accuracy'] = 0.7
                performance_data['helpfulness'] = 0.6
            else:
                performance_data['response_quality'] = 0.3
                performance_data['accuracy'] = 0.4
                performance_data['helpfulness'] = 0.3
        else:
            # Failed request
            performance_data['response_quality'] = 0.1
            performance_data['accuracy'] = 0.1
            performance_data['helpfulness'] = 0.1
        
        # Update Enhanced Graph Intelligence
        enhanced_intelligence.update_agent_performance(agent_id, performance_data)
        
        print(f"📊 Updated performance metrics for {agent_id}: {performance_data.get('response_quality', 0):.2f} quality")
        
        # Hebbian learning: strengthen/decay relationship weights based on outcome
        try:
            payload = {
                "agent_id": agent_id,
                "concept": concept.lower(),
                "success": bool(success)
            }
            _http_session.post(f"{GRAPHDB_MANAGER_URL}/hebbian/strengthen", json=payload, timeout=5)
        except Exception as he:
            print(f"⚠️  Hebbian update failed: {he}")

    except Exception as e:
        print(f"⚠️  Could not update performance metrics: {e}")

def _extract_agent_id_from_url(agent_url: str) -> Optional[str]:
    """Extract agent ID from agent URL"""
    
    # Common patterns for agent URLs
    # http://lightbulb_definition_ai:5001 -> Lightbulb_Definition_AI
    # http://localhost:5001 -> None (can't determine)
    
    if not agent_url:
        return None
    
    try:
        # Extract hostname from URL
        parsed = urllib.parse.urlparse(agent_url)
        hostname = parsed.hostname
        
        if hostname and '_' in hostname:
            # Convert hostname to agent ID format
            # lightbulb_definition_ai -> Lightbulb_Definition_AI
            parts = hostname.split('_')
            agent_id = '_'.join(part.capitalize() for part in parts)
            return agent_id
        
        return None
        
    except Exception:
        return None

def register_dynamic_agent_in_graph(agent, concept: str) -> bool:
    """Register a dynamically created agent in the graph database"""
    
    print(f"  📊 Registering dynamic agent in graph database...")
    
    try:
        # Create agent node
        agent_payload = {
            "label": "Agent",
            "properties": {
                "name": agent.agent_name,
                "type": agent.template_id,
                "endpoint": agent.endpoint,
                "port": agent.port,
                "agent_id": agent.agent_id,
                "creation_method": "dynamic_neurogenesis",
                "creation_timestamp": agent.created_at,
                "status": agent.status.value,
                "capabilities": json.dumps(agent.capabilities),
                "concept_specialization": concept.lower()
            }
        }
        
        agent_response = _http_session.post(f"{GRAPHDB_MANAGER_URL}/create_node", 
                                     json=agent_payload, timeout=10)
        
        if agent_response.status_code == 201:
            agent_node_id = agent_response.json().get("node_id")
            print(f"    ✅ Agent node created (ID: {agent_node_id})")
            
            # Create HANDLES_CONCEPT relationship
            concept_rel_payload = {
                "start_node_id": agent_node_id,
                "end_node_label": "Concept",
                "end_node_properties": {"name": concept.lower()},
                "relationship_type": "HANDLES_CONCEPT",
                "relationship_properties": {
                    "specialization_level": "dynamic",
                    "creation_timestamp": time.time(),
                    "confidence": 0.8  # Dynamic agents start with good confidence
                }
            }
            
            concept_rel_response = _http_session.post(f"{GRAPHDB_MANAGER_URL}/create_relationship",
                                       json=concept_rel_payload, timeout=10)

            # Create BELONGS_TO relationship
            region_rel_payload = {
                "start_node_id": agent_node_id,
                "end_node_label": "Region",
                "end_node_properties": {"name": "General"}, # Default to General for now
                "relationship_type": "BELONGS_TO"
            }

            region_rel_response = _http_session.post(f"{GRAPHDB_MANAGER_URL}/create_relationship",
                                      json=region_rel_payload, timeout=10)
            
            if concept_rel_response.status_code == 201 and region_rel_response.status_code == 201:
                print(f"    ✅ Agent-Concept and Agent-Region relationships created")
                return True
            else:
                print(f"    ⚠️  Failed to create agent relationships.")
                print(f"       HANDLES_CONCEPT -> Status: {concept_rel_response.status_code}")
                print(f"       BELONGS_TO -> Status: {region_rel_response.status_code}")
                return False
        else:
            print(f"    ❌ Failed to create agent node: {agent_response.status_code}")
            return False
            
    except Exception as e:
        print(f"    ❌ Graph registration error: {e}")
        return False

def expand_concept(concept: str, intent: str) -> Dict[str, Any]:
    """Complete concept expansion process: research + graph node creation + optional agent creation"""
    print(f"🚀 CONCEPT EXPANSION: Starting expansion for '{concept}'")
    
    # Step 1: Research the concept
    research_data = research_unknown_concept(concept, intent)
    
    # Step 2: Create rich graph node
    node_success = create_concept_node(concept, research_data)
    
    # Step 3: Determine if we should create a dynamic agent
    should_create_agent = False
    confidence = research_data.get("confidence_score", 0.0)
    research_sources = research_data.get("research_sources", [])
    
    # Create dynamic agent if:
    # - Research confidence is reasonable (>0.3)
    # - We have research sources
    # - Dynamic agents are enabled
    if confidence > 0.3 and research_sources and ENABLE_DYNAMIC_AGENTS:
        should_create_agent = True
        print(f"  🧬 Confidence {confidence:.2f} > 0.3 and sources available - triggering dynamic agent creation")
    
    agent_data = None
    if should_create_agent:
        agent_data = create_dynamic_agent(concept, intent, research_data)
    
    # Step 4: Return expansion result
    expansion_result = {
        "concept": concept,
        "expansion_successful": node_success,
        "research_data": research_data,
        "expansion_method": "neurogenesis_phase2" if agent_data else "neurogenesis_phase1",
        "dynamic_agent": agent_data,
        "can_retry": True
    }
    
    if agent_data:
        print(f"  🎉 FULL NEUROGENESIS: Concept '{concept}' now has dedicated agent!")
        expansion_result["message"] = f"Successfully created specialized agent '{agent_data['agent_name']}' for '{concept}'. The agent is ready to handle future queries about this concept."
        expansion_result["agent_endpoint"] = agent_data["endpoint"]
    elif node_success:
        print(f"  🎉 Concept expansion completed successfully for '{concept}'!")
        expansion_result["message"] = f"Successfully expanded knowledge about '{concept}' through agent research and graph node creation."
    else:
        print(f"  ⚠️  Concept expansion partially completed for '{concept}' (research done, node creation failed)")
        expansion_result["message"] = f"Researched '{concept}' but failed to create graph node. Research data available."
    
    return expansion_result

def discover_agent_via_graph(concept: str, intent: str) -> Optional[str]:
    """Discovers an agent using Enhanced Graph Intelligence for optimal selection."""
    
    if ENHANCED_INTELLIGENCE_AVAILABLE:
        # Use Enhanced Graph Intelligence for smart agent selection
        try:
            print(f"🎯 Using Enhanced Graph Intelligence for '{concept}' with intent '{intent}'")
            
            # Get intelligent agent recommendations
            agent_scores = enhanced_intelligence.discover_intelligent_agents(
                concept=concept,
                intent=intent,
                context={"query_source": "orchestrator"}
            )
            
            if agent_scores:
                # Select the highest scoring agent
                best_agent = agent_scores[0]
                
                print(f"  🧠 Selected agent: {best_agent.agent_id}")
                print(f"     Relevance score: {best_agent.relevance_score:.3f}")
                print(f"     Reasoning: {', '.join(best_agent.reasoning[:2])}")  # Show top 2 reasons
                
                # Get endpoint from agent profile
                agent_profile = enhanced_intelligence.agent_profiles.get(best_agent.agent_id)
                if agent_profile and agent_profile.endpoint:
                    return agent_profile.endpoint
                else:
                    # Fallback to basic discovery for endpoint
                    return _discover_agent_endpoint_fallback(best_agent.agent_id)
            else:
                print(f"  ⚠️  Enhanced Intelligence found no suitable agents for '{concept}'")
                return None
                
        except Exception as e:
            print(f"  ⚠️  Enhanced Intelligence error: {e}")
            print(f"  🔄 Falling back to basic graph discovery")
            return _discover_agent_basic_fallback(concept, intent)
    else:
        # Fallback to basic graph discovery
        return _discover_agent_basic_fallback(concept, intent)

def _discover_agent_endpoint_fallback(agent_id: str) -> Optional[str]:
    """Fallback method to discover agent endpoint from graph"""
    try:
        payload = {
            "start_node_label": "Agent",
            "start_node_properties": {"name": agent_id},
            "relationship_type": "*",
            "relationship_direction": "both",
            "target_node_label": "*"
        }
        response = _http_session.post(f"{GRAPHDB_MANAGER_URL}/find_connected_nodes", json=payload, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            agent_data = data.get("source_node", {})
            return agent_data.get("endpoint")
        return None
    except requests.exceptions.RequestException as e:
        print(f"    ⚠️  Endpoint fallback error: {e}")
        return None

def _discover_agent_basic_fallback(concept: str, intent: str) -> Optional[str]:
    """Basic fallback agent discovery method"""
    try:
        payload = {
            "start_node_label": "Concept",
            "start_node_properties": {"name": concept.lower()},
            "relationship_type": "HANDLES_CONCEPT",
            "relationship_direction": "in",
            "target_node_label": "Agent"
        }
        response = requests.post(f"{GRAPHDB_MANAGER_URL}/find_connected_nodes", json=payload, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("nodes"):
                agent_node = data["nodes"][0]
                return agent_node.get("endpoint")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error in basic agent discovery for '{concept}': {e}")
        return None

def send_task_to_agent(task: dict) -> Optional[dict]:
    """Sends a single task to the appropriate agent discovered via the graph."""
    concept, intent = task['concept'], task['intent']
    start_time = time.time()
    
    # Use Enhanced Graph Intelligence for agent discovery
    agent_url = discover_agent_via_graph(concept, intent)
    
    if agent_url:
        # Agent found - normal processing
        payload = {"task_id": task["task_id"], "intent": intent, "concept": concept, "args": task.get("args", {})}
        print(f"Dispatching Agent Job to {agent_url} (discovered via graph): {payload}")
        try:
            response = _http_session.post(agent_url, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            # Track performance for Enhanced Graph Intelligence
            _update_agent_performance_metrics(agent_url, concept, intent, start_time, result, success=True)
            
            return result
        except requests.exceptions.RequestException as e:
            error_result = {"task_id": task["task_id"], "status": "error", "error_message": str(e)}
            
            # Track failure for Enhanced Graph Intelligence
            _update_agent_performance_metrics(agent_url, concept, intent, start_time, error_result, success=False)
            
            return error_result
    else:
        # 🧠 NEUROGENESIS TRIGGER: No agent found for concept
        print(f"🧠 NEUROGENESIS TRIGGERED: No agent found for concept '{concept}' with intent '{intent}'")
        
        # Check if this is a completely unknown concept
        concept_exists = check_concept_exists(concept)
        
        if not concept_exists:
            print(f"  🔍 Concept '{concept}' is completely unknown - triggering concept expansion!")
            
            # Trigger concept expansion (Phase 1: Concept Expansion)
            expansion_result = expand_concept(concept, intent)
            
            if expansion_result.get("expansion_successful") or expansion_result.get("dynamic_agent"):
                # Concept expansion successful - return the researched knowledge
                response = {
                    "task_id": task["task_id"],
                    "status": "neurogenesis_success",
                    "data": expansion_result["message"],
                    "neurogenesis_data": {
                        "concept": concept,
                        "expansion_method": expansion_result.get("expansion_method", "concept_research"),
                        "research_summary": expansion_result["research_data"].get("primary_definition", ""),
                        "confidence": expansion_result["research_data"].get("confidence_score", 0.0),
                        "sources": expansion_result["research_data"].get("research_sources", [])
                    },
                    "agent_name": "Orchestrator_Neurogenesis"
                }
                
                # Add dynamic agent information if created
                if expansion_result.get("dynamic_agent"):
                    agent_info = expansion_result["dynamic_agent"]
                    response["neurogenesis_data"]["dynamic_agent_created"] = True
                    response["neurogenesis_data"]["new_agent_name"] = agent_info["agent_name"]
                    response["neurogenesis_data"]["new_agent_endpoint"] = agent_info["endpoint"]
                    response["neurogenesis_data"]["new_agent_capabilities"] = agent_info["capabilities"]
                    response["status"] = "neurogenesis_with_agent_creation"
                
                return response
            else:
                # Concept expansion failed but we have research data
                research_data = expansion_result.get("research_data", {})
                if research_data.get("primary_definition"):
                    return {
                        "task_id": task["task_id"],
                        "status": "neurogenesis_partial",
                        "data": f"Researched '{concept}': {research_data.get('primary_definition', 'No definition found')}",
                        "neurogenesis_data": {
                            "concept": concept,
                            "expansion_method": "research_only",
                            "research_summary": research_data.get("primary_definition", ""),
                            "confidence": research_data.get("confidence_score", 0.0),
                            "sources": research_data.get("research_sources", [])
                        },
                        "agent_name": "Orchestrator_Neurogenesis"
                    }
                else:
                    return {
                        "task_id": task["task_id"],
                        "status": "neurogenesis_failed",
                        "data": f"Unable to research or expand knowledge about '{concept}'. This concept may require specialized agents or external knowledge sources.",
                        "error_message": f"Concept expansion failed for '{concept}'"
                    }
        else:
            # Concept exists but no agent handles it
            return {
                "task_id": task["task_id"],
                "status": "no_agent_available",
                "data": f"Concept '{concept}' exists in the knowledge graph but no agent is currently available to handle intent '{intent}'. This may require agent creation in future phases.",
                "error_message": f"No agent available for known concept '{concept}' with intent '{intent}'"
            }

def process_tasks(tasks: list) -> dict:
    """Processes a list of tasks by sending them to agents and collecting results."""
    all_results = {}
    for task in tasks:
        result = send_task_to_agent(task)
        all_results[str(task["task_id"])] = result or {"task_id": task["task_id"], "status": "error", "error_message": "Failed to process task."}
    return all_results