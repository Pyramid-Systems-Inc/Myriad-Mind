"""
Enhanced Graph Intelligence System
==================================

Advanced intelligence layer for the Myriad Cognitive Architecture that provides:
- Smart agent discovery with relevance scoring
- Context-aware agent selection
- Dynamic agent clustering and organization  
- Intelligent query routing
- Performance optimization for graph operations

This system transforms basic graph queries into intelligent agent selection
that considers expertise, context, performance, and domain specialization.

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Enhanced Graph Intelligence)
Date: 2025-01-01
"""

import json
import time
import requests
import logging
import threading
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from pathlib import Path
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentProfile:
    """Comprehensive profile of an agent's capabilities and performance"""
    agent_id: str
    agent_name: str
    endpoint: str
    agent_type: str
    primary_concepts: List[str]
    capabilities: List[str]
    expertise_domains: List[str]
    performance_metrics: Dict[str, float]
    specialization_score: float
    availability_score: float
    last_updated: datetime
    creation_method: str  # 'static', 'neurogenesis'
    collaboration_history: List[str]

@dataclass
class QueryContext:
    """Context information for intelligent query processing"""
    concept: str
    intent: str
    complexity_score: float
    domain_indicators: List[str]
    required_capabilities: List[str]
    urgency_level: str  # 'low', 'medium', 'high'
    user_preferences: Dict[str, Any]

@dataclass
class AgentRelevanceScore:
    """Relevance score for an agent relative to a specific query"""
    agent_id: str
    relevance_score: float
    expertise_match: float
    capability_match: float
    domain_overlap: float
    performance_factor: float
    availability_factor: float
    confidence_level: float
    reasoning: List[str]
    hebbian_weight: float = 0.5

@dataclass
class AgentCluster:
    """Cluster of related agents organized by domain or expertise"""
    cluster_id: str
    cluster_name: str
    cluster_type: str  # 'domain', 'capability', 'performance'
    agent_ids: List[str]
    cluster_keywords: List[str]
    cluster_score: float
    last_updated: datetime

class EnhancedGraphIntelligence:
    """
    Advanced intelligence system for smart agent discovery and selection.
    
    Key Features:
    - Multi-criteria relevance scoring
    - Dynamic agent clustering
    - Context-aware selection
    - Performance optimization
    - Intelligent routing
    """
    
    def __init__(self):
        self.agent_profiles: Dict[str, AgentProfile] = {}
        self.agent_clusters: Dict[str, AgentCluster] = {}
        self.query_cache: Dict[str, Any] = {}
        self.performance_history: Dict[str, List[Dict]] = defaultdict(list)
        
        # Configuration
        self.config = {
            'cache_ttl': 300,  # 5 minutes
            'min_relevance_threshold': 0.3,
            'cluster_update_interval': 3600,  # 1 hour
            'performance_history_limit': 100,
            'max_agents_per_query': 5,
            'clustering_similarity_threshold': 0.7
        }
        
        # GraphDB connection
        self.graphdb_url = "http://graphdb_manager_ai:5008"
        
        # Background tasks
        self._start_background_tasks()
        
        logger.info("🧠 Enhanced Graph Intelligence System initialized")
    
    def _start_background_tasks(self):
        """Start background tasks for maintenance and optimization"""
        
        # Agent profile update task
        profile_thread = threading.Thread(target=self._profile_update_loop, daemon=True)
        profile_thread.start()
        
        # Clustering update task  
        clustering_thread = threading.Thread(target=self._clustering_update_loop, daemon=True)
        clustering_thread.start()
        
        # Cache cleanup task
        cache_thread = threading.Thread(target=self._cache_cleanup_loop, daemon=True)
        cache_thread.start()
        
        logger.info("🔄 Background intelligence tasks started")

    def _fetch_hebbian_weight(self, agent_name: str, concept: str) -> float:
        """Fetch Hebbian weight for (Agent)-[HANDLES_CONCEPT]->(Concept). Defaults to 0.5."""
        try:
            response = requests.post(
                f"{self.graphdb_url}/get_agents_for_concept",
                json={"concept": concept, "relationship_type": "HANDLES_CONCEPT"},
                timeout=8
            )
            if response.status_code == 200:
                agents = response.json().get("agents", [])
                for item in agents:
                    agent = item.get("agent", {})
                    rel = item.get("relationship", {})
                    if agent.get("name") == agent_name:
                        return float(rel.get("weight", 0.5))
        except requests.RequestException:
            pass
        return 0.5
    
    def discover_intelligent_agents(self, concept: str, intent: str, 
                                  context: Optional[Dict[str, Any]] = None) -> List[AgentRelevanceScore]:
        """
        Intelligent agent discovery with multi-criteria relevance scoring.
        
        Args:
            concept: The concept to find agents for
            intent: The intended action (define, analyze, etc.)
            context: Additional context for intelligent selection
            
        Returns:
            List of agents with relevance scores, sorted by relevance
        """
        logger.info(f"🎯 Intelligent agent discovery for '{concept}' with intent '{intent}'")
        
        # Parse query context
        query_context = self._parse_query_context(concept, intent, context or {})
        
        # Check cache first
        cache_key = self._generate_cache_key(concept, intent, context)
        if cache_key in self.query_cache:
            cached_result = self.query_cache[cache_key]
            if self._is_cache_valid(cached_result['timestamp']):
                logger.info("📋 Returning cached intelligent agent selection")
                return cached_result['agents']
        
        # Discover candidate agents
        candidate_agents = self._discover_candidate_agents(concept, query_context)
        
        # Score agents for relevance
        scored_agents = []
        for agent_profile in candidate_agents:
            relevance_score = self._calculate_agent_relevance(agent_profile, query_context)
            if relevance_score.relevance_score >= self.config['min_relevance_threshold']:
                scored_agents.append(relevance_score)
        
        # Sort by relevance score
        scored_agents.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Limit results
        max_agents = self.config['max_agents_per_query']
        final_agents = scored_agents[:max_agents]
        
        # Cache the result
        self.query_cache[cache_key] = {
            'agents': final_agents,
            'timestamp': datetime.now(),
            'query_context': query_context
        }
        
        logger.info(f"✅ Found {len(final_agents)} relevant agents with intelligence scoring")
        
        return final_agents
    
    def _parse_query_context(self, concept: str, intent: str, context: Dict[str, Any]) -> QueryContext:
        """Parse and analyze query context for intelligent processing"""
        
        # Analyze concept complexity
        complexity_score = self._calculate_concept_complexity(concept)
        
        # Extract domain indicators
        domain_indicators = self._extract_domain_indicators(concept, intent)
        
        # Determine required capabilities
        required_capabilities = self._map_intent_to_capabilities(intent)
        
        # Assess urgency
        urgency_level = context.get('urgency', 'medium')
        
        return QueryContext(
            concept=concept,
            intent=intent,
            complexity_score=complexity_score,
            domain_indicators=domain_indicators,
            required_capabilities=required_capabilities,
            urgency_level=urgency_level,
            user_preferences=context.get('preferences', {})
        )
    
    def _calculate_concept_complexity(self, concept: str) -> float:
        """Calculate the complexity score of a concept"""
        
        # Simple heuristics for concept complexity
        complexity_factors = []
        
        # Length factor
        word_count = len(concept.split())
        complexity_factors.append(min(word_count / 5.0, 1.0))
        
        # Technical terms detection
        technical_indicators = [
            'quantum', 'neural', 'biomimetic', 'algorithm', 'artificial',
            'machine', 'deep', 'learning', 'intelligence', 'cognitive',
            'advanced', 'complex', 'sophisticated', 'revolutionary'
        ]
        
        tech_score = sum(1 for term in technical_indicators if term.lower() in concept.lower())
        complexity_factors.append(min(tech_score / 3.0, 1.0))
        
        # Average the factors
        return sum(complexity_factors) / len(complexity_factors)
    
    def _extract_domain_indicators(self, concept: str, intent: str) -> List[str]:
        """Extract domain indicators from concept and intent"""
        
        domain_keywords = {
            'technology': ['computer', 'software', 'digital', 'tech', 'system', 'algorithm'],
            'science': ['quantum', 'physics', 'chemistry', 'biology', 'research', 'scientific'],
            'engineering': ['engineering', 'design', 'build', 'construct', 'develop', 'create'],
            'business': ['business', 'market', 'commercial', 'industry', 'enterprise', 'economic'],
            'healthcare': ['medical', 'health', 'clinical', 'patient', 'diagnosis', 'treatment'],
            'education': ['learning', 'education', 'teaching', 'knowledge', 'training', 'academic']
        }
        
        text = f"{concept} {intent}".lower()
        detected_domains = []
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in text for keyword in keywords):
                detected_domains.append(domain)
        
        return detected_domains
    
    def _map_intent_to_capabilities(self, intent: str) -> List[str]:
        """Map query intent to required agent capabilities"""
        
        intent_capability_map = {
            'define': ['concept_definition', 'knowledge_storage'],
            'explain': ['explanation_skills', 'knowledge_synthesis'],
            'analyze': ['analytical_reasoning', 'data_analysis'],
            'compare': ['comparison_analysis', 'relationship_mapping'],
            'evaluate': ['evaluation_skills', 'critical_thinking'],
            'create': ['creative_generation', 'synthesis'],
            'solve': ['problem_solving', 'logical_reasoning'],
            'predict': ['predictive_analysis', 'forecasting'],
            'optimize': ['optimization', 'performance_analysis']
        }
        
        return intent_capability_map.get(intent.lower(), ['general_knowledge'])
    
    def _discover_candidate_agents(self, concept: str, context: QueryContext) -> List[AgentProfile]:
        """Discover candidate agents using multiple strategies"""
        
        candidates = []
        
        # Strategy 1: Direct concept match
        direct_matches = self._find_direct_concept_agents(concept)
        candidates.extend(direct_matches)
        
        # Strategy 2: Domain-based discovery
        domain_agents = self._find_domain_agents(context.domain_indicators)
        candidates.extend(domain_agents)
        
        # Strategy 3: Capability-based discovery
        capability_agents = self._find_capability_agents(context.required_capabilities)
        candidates.extend(capability_agents)
        
        # Strategy 4: Cluster-based discovery
        cluster_agents = self._find_cluster_agents(concept, context)
        candidates.extend(cluster_agents)
        
        # Remove duplicates
        unique_candidates = {agent.agent_id: agent for agent in candidates}
        
        return list(unique_candidates.values())
    
    def _find_direct_concept_agents(self, concept: str) -> List[AgentProfile]:
        """Find agents that directly handle the concept"""
        
        try:
            response = requests.post(
                f"{self.graphdb_url}/find_connected_nodes",
                json={
                    "node_name": concept,
                    "relationship_types": ["HANDLES_CONCEPT"],
                    "direction": "incoming"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                agents = result.get('connected_agents', [])
                
                profiles = []
                for agent_data in agents:
                    profile = self._create_agent_profile_from_graph_data(agent_data)
                    if profile:
                        profiles.append(profile)
                
                return profiles
            
        except requests.RequestException as e:
            logger.warning(f"Could not find direct concept agents: {e}")
        
        return []
    
    def _find_domain_agents(self, domains: List[str]) -> List[AgentProfile]:
        """Find agents based on domain expertise"""
        
        domain_agents = []
        
        for domain in domains:
            # Look for agents with domain expertise
            for agent_id, profile in self.agent_profiles.items():
                if any(domain.lower() in expertise.lower() for expertise in profile.expertise_domains):
                    domain_agents.append(profile)
        
        return domain_agents
    
    def _find_capability_agents(self, capabilities: List[str]) -> List[AgentProfile]:
        """Find agents based on required capabilities"""
        
        capability_agents = []
        
        for capability in capabilities:
            for agent_id, profile in self.agent_profiles.items():
                if any(capability.lower() in cap.lower() for cap in profile.capabilities):
                    capability_agents.append(profile)
        
        return capability_agents
    
    def _find_cluster_agents(self, concept: str, context: QueryContext) -> List[AgentProfile]:
        """Find agents using cluster-based discovery"""
        
        cluster_agents = []
        
        # Find relevant clusters
        relevant_clusters = self._find_relevant_clusters(concept, context)
        
        for cluster in relevant_clusters:
            for agent_id in cluster.agent_ids:
                if agent_id in self.agent_profiles:
                    cluster_agents.append(self.agent_profiles[agent_id])
        
        return cluster_agents
    
    def _find_relevant_clusters(self, concept: str, context: QueryContext) -> List[AgentCluster]:
        """Find clusters relevant to the concept and context"""
        
        relevant_clusters = []
        concept_lower = concept.lower()
        
        for cluster in self.agent_clusters.values():
            # Check if concept matches cluster keywords
            keyword_match = any(keyword.lower() in concept_lower for keyword in cluster.cluster_keywords)
            
            # Check domain overlap
            domain_match = any(domain in cluster.cluster_keywords for domain in context.domain_indicators)
            
            if keyword_match or domain_match:
                relevant_clusters.append(cluster)
        
        # Sort by cluster score
        relevant_clusters.sort(key=lambda x: x.cluster_score, reverse=True)
        
        return relevant_clusters[:3]  # Top 3 relevant clusters
    
    def _calculate_agent_relevance(self, agent: AgentProfile, context: QueryContext) -> AgentRelevanceScore:
        """Calculate comprehensive relevance score for an agent"""
        
        # Expertise match score
        expertise_match = self._calculate_expertise_match(agent, context)
        
        # Capability match score  
        capability_match = self._calculate_capability_match(agent, context)
        
        # Domain overlap score
        domain_overlap = self._calculate_domain_overlap(agent, context)
        
        # Performance factor
        performance_factor = self._calculate_performance_factor(agent)
        
        # Availability factor
        availability_factor = self._calculate_availability_factor(agent)
        
        # Hebbian weight factor (relationship strength)
        hebbian_weight = self._fetch_hebbian_weight(agent.agent_name, context.concept)

        # Weighted relevance score (include hebbian factor)
        weights = {
            'expertise': 0.28,
            'capability': 0.22,
            'domain': 0.18,
            'performance': 0.14,
            'availability': 0.08,
            'hebbian': 0.10
        }
        
        relevance_score = (
            expertise_match * weights['expertise'] +
            capability_match * weights['capability'] +
            domain_overlap * weights['domain'] +
            performance_factor * weights['performance'] +
            availability_factor * weights['availability'] +
            hebbian_weight * weights['hebbian']
        )
        
        # Calculate confidence level
        confidence_level = self._calculate_confidence_level(agent, context, relevance_score)
        
        # Generate reasoning
        reasoning = self._generate_relevance_reasoning(
            agent, context, expertise_match, capability_match, 
            domain_overlap, performance_factor, availability_factor
        )
        
        score = AgentRelevanceScore(
            agent_id=agent.agent_id,
            relevance_score=relevance_score,
            expertise_match=expertise_match,
            capability_match=capability_match,
            domain_overlap=domain_overlap,
            performance_factor=performance_factor,
            availability_factor=availability_factor,
            confidence_level=confidence_level,
            reasoning=reasoning,
            hebbian_weight=hebbian_weight
        )
        # Add reasoning for hebbian factor
        if hebbian_weight >= 0.7:
            score.reasoning.append(f"Strong learned association (weight {hebbian_weight:.2f})")
        elif hebbian_weight >= 0.5:
            score.reasoning.append(f"Moderate learned association (weight {hebbian_weight:.2f})")
        else:
            score.reasoning.append(f"Weak learned association (weight {hebbian_weight:.2f})")
        return score
    
    def _calculate_expertise_match(self, agent: AgentProfile, context: QueryContext) -> float:
        """Calculate how well agent expertise matches the query"""
        
        concept_lower = context.concept.lower()
        matches = 0
        total = len(agent.primary_concepts) + len(agent.expertise_domains)
        
        if total == 0:
            return 0.0
        
        # Check primary concepts
        for concept in agent.primary_concepts:
            if concept.lower() in concept_lower or concept_lower in concept.lower():
                matches += 1
        
        # Check expertise domains
        for domain in agent.expertise_domains:
            if domain.lower() in concept_lower or any(indicator in domain.lower() for indicator in context.domain_indicators):
                matches += 1
        
        # Apply specialization bonus
        base_score = matches / total
        specialization_bonus = agent.specialization_score * 0.2
        
        return min(base_score + specialization_bonus, 1.0)
    
    def _calculate_capability_match(self, agent: AgentProfile, context: QueryContext) -> float:
        """Calculate how well agent capabilities match required capabilities"""
        
        if not context.required_capabilities:
            return 0.5  # Neutral score if no specific capabilities required
        
        matches = 0
        for required_cap in context.required_capabilities:
            if any(required_cap.lower() in cap.lower() for cap in agent.capabilities):
                matches += 1
        
        return matches / len(context.required_capabilities)
    
    def _calculate_domain_overlap(self, agent: AgentProfile, context: QueryContext) -> float:
        """Calculate domain overlap between agent and query"""
        
        if not context.domain_indicators:
            return 0.5  # Neutral score if no domain indicators
        
        overlaps = 0
        for domain in context.domain_indicators:
            if any(domain.lower() in expertise.lower() for expertise in agent.expertise_domains):
                overlaps += 1
        
        return overlaps / len(context.domain_indicators)
    
    def _calculate_performance_factor(self, agent: AgentProfile) -> float:
        """Calculate performance factor based on historical metrics"""
        
        if not agent.performance_metrics:
            return 0.5  # Default score for new agents
        
        # Average key performance metrics
        key_metrics = ['response_quality', 'accuracy', 'helpfulness']
        scores = []
        
        for metric in key_metrics:
            if metric in agent.performance_metrics:
                scores.append(agent.performance_metrics[metric])
        
        if scores:
            return sum(scores) / len(scores)
        
        return 0.5
    
    def _calculate_availability_factor(self, agent: AgentProfile) -> float:
        """Calculate availability factor based on current load and status"""
        
        # Use availability score from profile
        return agent.availability_score
    
    def _calculate_confidence_level(self, agent: AgentProfile, context: QueryContext, relevance_score: float) -> float:
        """Calculate confidence level in the agent selection"""
        
        factors = [
            relevance_score,
            len(agent.collaboration_history) / 10.0,  # Experience factor
            agent.specialization_score,
            1.0 if agent.creation_method == 'neurogenesis' else 0.8  # Neurogenesis bonus
        ]
        
        return min(sum(factors) / len(factors), 1.0)
    
    def _generate_relevance_reasoning(self, agent: AgentProfile, context: QueryContext,
                                    expertise_match: float, capability_match: float,
                                    domain_overlap: float, performance_factor: float,
                                    availability_factor: float) -> List[str]:
        """Generate human-readable reasoning for the relevance score"""
        
        reasoning = []
        
        if expertise_match > 0.7:
            reasoning.append(f"Strong expertise match: {expertise_match:.2f}")
        elif expertise_match > 0.4:
            reasoning.append(f"Moderate expertise match: {expertise_match:.2f}")
        else:
            reasoning.append(f"Limited expertise match: {expertise_match:.2f}")
        
        if capability_match > 0.7:
            reasoning.append(f"Excellent capability alignment: {capability_match:.2f}")
        elif capability_match > 0.4:
            reasoning.append(f"Good capability alignment: {capability_match:.2f}")
        
        if domain_overlap > 0.5:
            reasoning.append(f"Good domain overlap: {domain_overlap:.2f}")
        
        if performance_factor > 0.7:
            reasoning.append(f"High performance history: {performance_factor:.2f}")
        
        if availability_factor > 0.8:
            reasoning.append(f"High availability: {availability_factor:.2f}")
        
        if agent.creation_method == 'neurogenesis':
            reasoning.append("Created via neurogenesis for specialized knowledge")
        
        return reasoning
    
    def _create_agent_profile_from_graph_data(self, agent_data: Dict[str, Any]) -> Optional[AgentProfile]:
        """Create agent profile from graph database data"""
        
        try:
            agent_id = agent_data.get('name', '')
            if not agent_id:
                return None
            
            # Extract or set default values
            return AgentProfile(
                agent_id=agent_id,
                agent_name=agent_data.get('name', agent_id),
                endpoint=agent_data.get('endpoint', ''),
                agent_type=agent_data.get('type', 'unknown'),
                primary_concepts=agent_data.get('primary_concepts', []),
                capabilities=agent_data.get('capabilities', []),
                expertise_domains=agent_data.get('expertise_domains', []),
                performance_metrics=agent_data.get('performance_metrics', {}),
                specialization_score=agent_data.get('specialization_score', 0.5),
                availability_score=agent_data.get('availability_score', 1.0),
                last_updated=datetime.now(),
                creation_method=agent_data.get('creation_method', 'static'),
                collaboration_history=agent_data.get('collaboration_history', [])
            )
            
        except Exception as e:
            logger.warning(f"Could not create agent profile from data: {e}")
            return None
    
    def update_agent_performance(self, agent_id: str, performance_data: Dict[str, Any]):
        """Update agent performance metrics for intelligent selection"""
        
        if agent_id in self.agent_profiles:
            profile = self.agent_profiles[agent_id]
            
            # Update performance metrics
            for metric, value in performance_data.items():
                profile.performance_metrics[metric] = value
            
            # Record performance history
            self.performance_history[agent_id].append({
                'timestamp': datetime.now(),
                'metrics': performance_data.copy()
            })
            
            # Limit history size
            if len(self.performance_history[agent_id]) > self.config['performance_history_limit']:
                self.performance_history[agent_id] = self.performance_history[agent_id][-self.config['performance_history_limit']:]
            
            # Update last_updated
            profile.last_updated = datetime.now()
            
            logger.info(f"📊 Updated performance metrics for agent {agent_id}")
    
    def create_agent_clusters(self) -> Dict[str, AgentCluster]:
        """Create intelligent clusters of related agents"""
        
        logger.info("🔗 Creating intelligent agent clusters...")
        
        clusters = {}
        
        # Domain-based clustering
        domain_clusters = self._create_domain_clusters()
        clusters.update(domain_clusters)
        
        # Capability-based clustering
        capability_clusters = self._create_capability_clusters()
        clusters.update(capability_clusters)
        
        # Performance-based clustering
        performance_clusters = self._create_performance_clusters()
        clusters.update(performance_clusters)
        
        self.agent_clusters = clusters
        
        logger.info(f"✅ Created {len(clusters)} intelligent agent clusters")
        
        return clusters
    
    def _create_domain_clusters(self) -> Dict[str, AgentCluster]:
        """Create clusters based on domain expertise"""
        
        domain_groups = defaultdict(list)
        
        # Group agents by domain
        for agent_id, profile in self.agent_profiles.items():
            for domain in profile.expertise_domains:
                domain_groups[domain].append(agent_id)
        
        clusters = {}
        for domain, agent_ids in domain_groups.items():
            if len(agent_ids) >= 2:  # Only cluster if multiple agents
                cluster_id = f"domain_{domain.lower().replace(' ', '_')}"
                clusters[cluster_id] = AgentCluster(
                    cluster_id=cluster_id,
                    cluster_name=f"Domain: {domain}",
                    cluster_type="domain",
                    agent_ids=agent_ids,
                    cluster_keywords=[domain],
                    cluster_score=len(agent_ids) / len(self.agent_profiles),
                    last_updated=datetime.now()
                )
        
        return clusters
    
    def _create_capability_clusters(self) -> Dict[str, AgentCluster]:
        """Create clusters based on capabilities"""
        
        capability_groups = defaultdict(list)
        
        # Group agents by capabilities
        for agent_id, profile in self.agent_profiles.items():
            for capability in profile.capabilities:
                capability_groups[capability].append(agent_id)
        
        clusters = {}
        for capability, agent_ids in capability_groups.items():
            if len(agent_ids) >= 2:  # Only cluster if multiple agents
                cluster_id = f"capability_{capability.lower().replace(' ', '_')}"
                clusters[cluster_id] = AgentCluster(
                    cluster_id=cluster_id,
                    cluster_name=f"Capability: {capability}",
                    cluster_type="capability",
                    agent_ids=agent_ids,
                    cluster_keywords=[capability],
                    cluster_score=len(agent_ids) / len(self.agent_profiles),
                    last_updated=datetime.now()
                )
        
        return clusters
    
    def _create_performance_clusters(self) -> Dict[str, AgentCluster]:
        """Create clusters based on performance levels"""
        
        if not self.agent_profiles:
            return {}
        
        # Group agents by performance tier
        high_performers = []
        medium_performers = []
        emerging_performers = []
        
        for agent_id, profile in self.agent_profiles.items():
            avg_performance = self._calculate_performance_factor(profile)
            
            if avg_performance >= 0.8:
                high_performers.append(agent_id)
            elif avg_performance >= 0.6:
                medium_performers.append(agent_id)
            else:
                emerging_performers.append(agent_id)
        
        clusters = {}
        
        if high_performers:
            clusters["performance_high"] = AgentCluster(
                cluster_id="performance_high",
                cluster_name="High Performance Agents",
                cluster_type="performance",
                agent_ids=high_performers,
                cluster_keywords=["high_performance", "excellent", "expert"],
                cluster_score=0.9,
                last_updated=datetime.now()
            )
        
        if medium_performers:
            clusters["performance_medium"] = AgentCluster(
                cluster_id="performance_medium",
                cluster_name="Medium Performance Agents",
                cluster_type="performance", 
                agent_ids=medium_performers,
                cluster_keywords=["medium_performance", "competent", "reliable"],
                cluster_score=0.7,
                last_updated=datetime.now()
            )
        
        if emerging_performers:
            clusters["performance_emerging"] = AgentCluster(
                cluster_id="performance_emerging",
                cluster_name="Emerging Performance Agents",
                cluster_type="performance",
                agent_ids=emerging_performers,
                cluster_keywords=["emerging", "developing", "new"],
                cluster_score=0.5,
                last_updated=datetime.now()
            )
        
        return clusters
    
    def _profile_update_loop(self):
        """Background loop to update agent profiles"""
        
        while True:
            try:
                self._refresh_agent_profiles()
                time.sleep(600)  # Update every 10 minutes
            except Exception as e:
                logger.error(f"Agent profile update error: {e}")
                time.sleep(60)  # Retry after 1 minute on error
    
    def _clustering_update_loop(self):
        """Background loop to update clusters"""
        
        while True:
            try:
                if self.agent_profiles:  # Only update if we have profiles
                    self.create_agent_clusters()
                time.sleep(self.config['cluster_update_interval'])
            except Exception as e:
                logger.error(f"Clustering update error: {e}")
                time.sleep(300)  # Retry after 5 minutes on error
    
    def _cache_cleanup_loop(self):
        """Background loop to clean up expired cache entries"""
        
        while True:
            try:
                self._cleanup_expired_cache()
                time.sleep(300)  # Cleanup every 5 minutes
            except Exception as e:
                logger.error(f"Cache cleanup error: {e}")
                time.sleep(60)  # Retry after 1 minute on error
    
    def _refresh_agent_profiles(self):
        """Refresh agent profiles from graph database"""
        
        try:
            # Query all agents from graph database
            response = requests.post(
                f"{self.graphdb_url}/query_nodes",
                json={"node_type": "Agent"},
                timeout=15
            )
            
            if response.status_code == 200:
                agents_data = response.json().get('nodes', [])
                
                for agent_data in agents_data:
                    profile = self._create_agent_profile_from_graph_data(agent_data)
                    if profile:
                        self.agent_profiles[profile.agent_id] = profile
                
                logger.info(f"🔄 Refreshed {len(agents_data)} agent profiles")
            
        except requests.RequestException as e:
            logger.warning(f"Could not refresh agent profiles: {e}")
    
    def _cleanup_expired_cache(self):
        """Remove expired entries from query cache"""
        
        current_time = datetime.now()
        expired_keys = []
        
        for key, cache_entry in self.query_cache.items():
            if current_time - cache_entry['timestamp'] > timedelta(seconds=self.config['cache_ttl']):
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.query_cache[key]
        
        if expired_keys:
            logger.info(f"🧹 Cleaned up {len(expired_keys)} expired cache entries")
    
    def _generate_cache_key(self, concept: str, intent: str, context: Optional[Dict[str, Any]]) -> str:
        """Generate cache key for query"""
        
        key_data = f"{concept}|{intent}|{json.dumps(context or {}, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_cache_valid(self, timestamp: datetime) -> bool:
        """Check if cache entry is still valid"""
        
        return datetime.now() - timestamp < timedelta(seconds=self.config['cache_ttl'])
    
    def get_intelligence_stats(self) -> Dict[str, Any]:
        """Get statistics about the intelligence system"""
        
        return {
            'agent_profiles': len(self.agent_profiles),
            'agent_clusters': len(self.agent_clusters),
            'cache_entries': len(self.query_cache),
            'performance_records': sum(len(history) for history in self.performance_history.values()),
            'cluster_types': Counter(cluster.cluster_type for cluster in self.agent_clusters.values()),
            'avg_agent_performance': sum([
                self._calculate_performance_factor(profile) 
                for profile in self.agent_profiles.values()
            ]) / len(self.agent_profiles) if self.agent_profiles else 0.0,
            'last_cluster_update': max(
                (cluster.last_updated for cluster in self.agent_clusters.values()),
                default=datetime.min
            ).isoformat() if self.agent_clusters else None
        }


# Global enhanced graph intelligence instance
enhanced_intelligence = EnhancedGraphIntelligence()


def get_enhanced_intelligence() -> EnhancedGraphIntelligence:
    """Get the global enhanced intelligence instance"""
    return enhanced_intelligence


if __name__ == "__main__":
    # Test the enhanced intelligence system
    intelligence = EnhancedGraphIntelligence()
    
    # Test intelligent agent discovery
    agents = intelligence.discover_intelligent_agents(
        concept="quantum computing",
        intent="analyze",
        context={"urgency": "high", "complexity": "advanced"}
    )
    
    print(f"🧠 Found {len(agents)} intelligent agent matches:")
    for agent in agents:
        print(f"   {agent.agent_id}: {agent.relevance_score:.2f} relevance")
        print(f"      Reasoning: {', '.join(agent.reasoning)}")
    
    # Get intelligence stats
    stats = intelligence.get_intelligence_stats()
    print(f"\n📊 Intelligence System Stats:")
    print(json.dumps(stats, indent=2, default=str))
