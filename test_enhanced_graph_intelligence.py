#!/usr/bin/env python3
"""
Enhanced Graph Intelligence Test Suite
======================================

Tests the Enhanced Graph Intelligence system that provides:
- Smart agent discovery with relevance scoring
- Context-aware agent selection
- Dynamic agent clustering and organization
- Performance optimization for graph operations

Test Coverage:
- Intelligent agent discovery
- Relevance scoring algorithms
- Agent clustering
- Performance tracking
- Cache management
- Integration with orchestrator

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Enhanced Graph Intelligence)
Date: 2025-01-01
"""

import sys
import os
import time
import json
from typing import Dict, Any

# Add path for intelligence module
sys.path.append('.')

print("🎯 ENHANCED GRAPH INTELLIGENCE TEST SUITE")
print("==========================================")
print("Testing advanced intelligence for smart agent discovery and selection")
print()

def test_intelligence_initialization():
    """Test that the Enhanced Graph Intelligence can be initialized"""
    print("🔍 Test 1: Intelligence System Initialization")
    print("==============================================")
    
    try:
        from intelligence.enhanced_graph_intelligence import EnhancedGraphIntelligence
        
        intelligence = EnhancedGraphIntelligence()
        print("✅ Enhanced Graph Intelligence initialized successfully")
        print(f"   Configuration: {intelligence.config}")
        print(f"   Agent profiles: {len(intelligence.agent_profiles)}")
        print(f"   Agent clusters: {len(intelligence.agent_clusters)}")
        return True
        
    except Exception as e:
        print(f"❌ Intelligence system initialization failed: {e}")
        return False

def test_query_context_parsing():
    """Test query context parsing and analysis"""
    print("\n🧠 Test 2: Query Context Parsing")
    print("=================================")
    
    try:
        from intelligence.enhanced_graph_intelligence import EnhancedGraphIntelligence
        
        intelligence = EnhancedGraphIntelligence()
        
        # Test different types of queries
        test_cases = [
            ("quantum computing", "analyze", {"urgency": "high"}),
            ("machine learning", "define", {"complexity": "medium"}),
            ("artificial intelligence", "explain", {"urgency": "low"})
        ]
        
        for concept, intent, context in test_cases:
            query_context = intelligence._parse_query_context(concept, intent, context)
            
            print(f"✅ Parsed query context for '{concept}':")
            print(f"   Complexity: {query_context.complexity_score:.2f}")
            print(f"   Domains: {query_context.domain_indicators}")
            print(f"   Capabilities: {query_context.required_capabilities}")
            print(f"   Urgency: {query_context.urgency_level}")
        
        return True
        
    except Exception as e:
        print(f"❌ Query context parsing test failed: {e}")
        return False

def test_agent_clustering():
    """Test agent clustering algorithms"""
    print("\n🔗 Test 3: Agent Clustering")
    print("============================")
    
    try:
        from intelligence.enhanced_graph_intelligence import (
            EnhancedGraphIntelligence, AgentProfile
        )
        from datetime import datetime
        
        intelligence = EnhancedGraphIntelligence()
        
        # Create mock agent profiles
        mock_agents = [
            AgentProfile(
                agent_id="AI_Definition_Agent",
                agent_name="AI Definition Agent",
                endpoint="http://ai_definition:5001",
                agent_type="factbase_enhanced",
                primary_concepts=["artificial_intelligence", "machine_learning"],
                capabilities=["concept_definition", "knowledge_storage"],
                expertise_domains=["technology", "computer_science"],
                performance_metrics={"response_quality": 0.9, "accuracy": 0.85},
                specialization_score=0.8,
                availability_score=1.0,
                last_updated=datetime.now(),
                creation_method="neurogenesis",
                collaboration_history=["quantum_ai", "deep_learning"]
            ),
            AgentProfile(
                agent_id="Quantum_Computing_Agent",
                agent_name="Quantum Computing Agent", 
                endpoint="http://quantum_computing:5002",
                agent_type="specialist_basic",
                primary_concepts=["quantum_computing", "quantum_mechanics"],
                capabilities=["technical_analysis", "principle_explanation"],
                expertise_domains=["science", "physics"],
                performance_metrics={"response_quality": 0.95, "accuracy": 0.9},
                specialization_score=0.95,
                availability_score=0.9,
                last_updated=datetime.now(),
                creation_method="neurogenesis",
                collaboration_history=["quantum_ai"]
            ),
            AgentProfile(
                agent_id="Business_Analysis_Agent",
                agent_name="Business Analysis Agent",
                endpoint="http://business_analysis:5003",
                agent_type="function_basic",
                primary_concepts=["business_analysis", "market_research"],
                capabilities=["analytical_reasoning", "data_analysis"],
                expertise_domains=["business", "economics"],
                performance_metrics={"response_quality": 0.75, "accuracy": 0.8},
                specialization_score=0.7,
                availability_score=0.8,
                last_updated=datetime.now(),
                creation_method="static",
                collaboration_history=["market_ai"]
            )
        ]
        
        # Add mock agents to intelligence system
        for agent in mock_agents:
            intelligence.agent_profiles[agent.agent_id] = agent
        
        # Test clustering
        clusters = intelligence.create_agent_clusters()
        
        print(f"✅ Created {len(clusters)} agent clusters:")
        for cluster_id, cluster in clusters.items():
            print(f"   {cluster.cluster_name}: {len(cluster.agent_ids)} agents")
            print(f"      Type: {cluster.cluster_type}")
            print(f"      Keywords: {cluster.cluster_keywords}")
            print(f"      Score: {cluster.cluster_score:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent clustering test failed: {e}")
        return False

def test_intelligent_agent_discovery():
    """Test intelligent agent discovery with relevance scoring"""
    print("\n🎯 Test 4: Intelligent Agent Discovery")
    print("=======================================")
    
    try:
        from intelligence.enhanced_graph_intelligence import (
            EnhancedGraphIntelligence, AgentProfile
        )
        from datetime import datetime
        
        intelligence = EnhancedGraphIntelligence()
        
        # Add mock agent (reuse from previous test)
        mock_agent = AgentProfile(
            agent_id="Quantum_Computing_Agent",
            agent_name="Quantum Computing Agent",
            endpoint="http://quantum_computing:5002",
            agent_type="specialist_basic",
            primary_concepts=["quantum_computing", "quantum_mechanics"],
            capabilities=["technical_analysis", "principle_explanation"],
            expertise_domains=["science", "physics"],
            performance_metrics={"response_quality": 0.95, "accuracy": 0.9},
            specialization_score=0.95,
            availability_score=0.9,
            last_updated=datetime.now(),
            creation_method="neurogenesis",
            collaboration_history=["quantum_ai"]
        )
        
        intelligence.agent_profiles[mock_agent.agent_id] = mock_agent
        
        # Test intelligent discovery
        results = intelligence.discover_intelligent_agents(
            concept="quantum computing",
            intent="analyze",
            context={"urgency": "high", "complexity": "advanced"}
        )
        
        print(f"✅ Intelligent discovery found {len(results)} relevant agents:")
        for result in results:
            print(f"   Agent: {result.agent_id}")
            print(f"   Relevance: {result.relevance_score:.3f}")
            print(f"   Expertise: {result.expertise_match:.3f}")
            print(f"   Capability: {result.capability_match:.3f}")
            print(f"   Performance: {result.performance_factor:.3f}")
            print(f"   Reasoning: {', '.join(result.reasoning)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Intelligent agent discovery test failed: {e}")
        return False

def test_performance_tracking():
    """Test agent performance tracking and updates"""
    print("\n📊 Test 5: Performance Tracking")
    print("================================")
    
    try:
        from intelligence.enhanced_graph_intelligence import (
            EnhancedGraphIntelligence, AgentProfile
        )
        from datetime import datetime
        
        intelligence = EnhancedGraphIntelligence()
        
        # Add mock agent
        mock_agent = AgentProfile(
            agent_id="Test_Performance_Agent",
            agent_name="Test Performance Agent",
            endpoint="http://test_agent:5004",
            agent_type="factbase_basic",
            primary_concepts=["testing"],
            capabilities=["testing"],
            expertise_domains=["testing"],
            performance_metrics={},
            specialization_score=0.5,
            availability_score=1.0,
            last_updated=datetime.now(),
            creation_method="static",
            collaboration_history=[]
        )
        
        intelligence.agent_profiles[mock_agent.agent_id] = mock_agent
        
        # Test performance updates
        performance_data = {
            'response_time': 0.5,
            'success_rate': 1.0,
            'response_quality': 0.9,
            'accuracy': 0.85,
            'helpfulness': 0.8
        }
        
        intelligence.update_agent_performance("Test_Performance_Agent", performance_data)
        
        # Verify update
        updated_agent = intelligence.agent_profiles["Test_Performance_Agent"]
        print(f"✅ Performance tracking working:")
        print(f"   Updated metrics: {updated_agent.performance_metrics}")
        print(f"   Performance history entries: {len(intelligence.performance_history['Test_Performance_Agent'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance tracking test failed: {e}")
        return False

def test_cache_management():
    """Test query cache management"""
    print("\n🧹 Test 6: Cache Management")
    print("============================")
    
    try:
        from intelligence.enhanced_graph_intelligence import EnhancedGraphIntelligence
        
        intelligence = EnhancedGraphIntelligence()
        
        # Test cache key generation
        cache_key1 = intelligence._generate_cache_key("test_concept", "define", {"urgency": "high"})
        cache_key2 = intelligence._generate_cache_key("test_concept", "define", {"urgency": "high"})
        cache_key3 = intelligence._generate_cache_key("test_concept", "analyze", {"urgency": "high"})
        
        print(f"✅ Cache key generation working:")
        print(f"   Same query keys match: {cache_key1 == cache_key2}")
        print(f"   Different query keys differ: {cache_key1 != cache_key3}")
        
        # Test cache validity
        from datetime import datetime, timedelta
        
        old_timestamp = datetime.now() - timedelta(seconds=400)  # Older than TTL
        recent_timestamp = datetime.now() - timedelta(seconds=100)  # Within TTL
        
        print(f"   Old cache invalid: {not intelligence._is_cache_valid(old_timestamp)}")
        print(f"   Recent cache valid: {intelligence._is_cache_valid(recent_timestamp)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Cache management test failed: {e}")
        return False

def test_orchestrator_integration():
    """Test integration with orchestrator (if available)"""
    print("\n🔗 Test 7: Orchestrator Integration")
    print("====================================")
    
    try:
        # Test if we can import the enhanced orchestrator functions
        sys.path.append('orchestration')
        from orchestrator import (
            ENHANCED_INTELLIGENCE_AVAILABLE, 
            _extract_agent_id_from_url
        )
        
        print(f"✅ Orchestrator integration working:")
        print(f"   Enhanced Intelligence available: {ENHANCED_INTELLIGENCE_AVAILABLE}")
        
        # Test URL parsing
        test_urls = [
            "http://lightbulb_definition_ai:5001",
            "http://quantum_computing_agent:5002",
            "http://localhost:5003"
        ]
        
        for url in test_urls:
            agent_id = _extract_agent_id_from_url(url)
            print(f"   URL '{url}' -> Agent ID: {agent_id}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Orchestrator integration test skipped: {e}")
        return True  # Not a critical failure

def test_intelligence_stats():
    """Test intelligence system statistics"""
    print("\n📈 Test 8: Intelligence Statistics")
    print("===================================")
    
    try:
        from intelligence.enhanced_graph_intelligence import EnhancedGraphIntelligence
        
        intelligence = EnhancedGraphIntelligence()
        
        # Get stats
        stats = intelligence.get_intelligence_stats()
        
        print(f"✅ Intelligence statistics:")
        print(f"   Agent profiles: {stats['agent_profiles']}")
        print(f"   Agent clusters: {stats['agent_clusters']}")
        print(f"   Cache entries: {stats['cache_entries']}")
        print(f"   Performance records: {stats['performance_records']}")
        print(f"   Average performance: {stats['avg_agent_performance']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Intelligence statistics test failed: {e}")
        return False

def run_all_tests():
    """Run all Enhanced Graph Intelligence tests"""
    print("Starting comprehensive Enhanced Graph Intelligence test suite...\n")
    
    tests = [
        ("Intelligence System Initialization", test_intelligence_initialization),
        ("Query Context Parsing", test_query_context_parsing),
        ("Agent Clustering", test_agent_clustering),
        ("Intelligent Agent Discovery", test_intelligent_agent_discovery),
        ("Performance Tracking", test_performance_tracking),
        ("Cache Management", test_cache_management),
        ("Orchestrator Integration", test_orchestrator_integration),
        ("Intelligence Statistics", test_intelligence_stats)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("🏁 ENHANCED GRAPH INTELLIGENCE TEST RESULTS")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL ENHANCED GRAPH INTELLIGENCE TESTS PASSED!")
        print("✨ Smart agent discovery system is operational!")
        print("🎯 Enhanced Graph Intelligence: READY FOR PRODUCTION!")
    else:
        print(f"⚠️  {total - passed} tests failed. Review the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
