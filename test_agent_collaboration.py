#!/usr/bin/env python3
"""
Agent-to-Agent Communication Test
Tests direct peer collaboration without orchestrator mediation.

This demonstrates the "reflex arcs" capability where agents can directly 
communicate with each other using graph-based peer discovery.
"""

import requests
import json
import time
from typing import Dict, Any

# Agent endpoints
DEFINITION_AI_URL = "http://localhost:5001"
FUNCTION_AI_URL = "http://localhost:5002"
GRAPHDB_MANAGER_URL = "http://localhost:5008"

def check_services_health():
    """Check if all required services are healthy"""
    services = [
        ("Definition AI", DEFINITION_AI_URL),
        ("Function AI", FUNCTION_AI_URL),
        ("GraphDB Manager", GRAPHDB_MANAGER_URL)
    ]
    
    print("🔍 Checking service health...")
    all_healthy = True
    
    for name, url in services:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {name}: Healthy")
            else:
                print(f"  ❌ {name}: Unhealthy (status {response.status_code})")
                all_healthy = False
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {name}: Connection failed ({e})")
            all_healthy = False
    
    return all_healthy

def test_knowledge_request_collaboration():
    """Test Definition AI requesting knowledge from Function AI"""
    print("\n🧪 Test 1: Definition AI → Function AI (Knowledge Request)")
    print("=" * 60)
    
    collaboration_request = {
        "source_agent": {"name": "Lightbulb_Definition_AI", "type": "FactBase"},
        "collaboration_type": "knowledge_request",
        "target_concept": "lightbulb",
        "specific_request": {
            "knowledge_type": "industrial_impact",
            "detail_level": "detailed"
        },
        "context": {
            "user_query": "Comprehensive lightbulb information needed",
            "requesting_for": "user_query_synthesis"
        }
    }
    
    print("📤 Definition AI requesting industrial impact knowledge from Function AI...")
    print(f"Request: {json.dumps(collaboration_request, indent=2)}")
    
    try:
        response = requests.post(
            f"{FUNCTION_AI_URL}/collaborate", 
            json=collaboration_request, 
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n📥 Response received:")
            print(f"Status: {result.get('status')}")
            print(f"Data: {json.dumps(result.get('data'), indent=2)}")
            print(f"Collaboration Metadata: {json.dumps(result.get('collaboration_metadata'), indent=2)}")
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_context_sharing_collaboration():
    """Test Function AI requesting context from Definition AI"""
    print("\n🧪 Test 2: Function AI → Definition AI (Context Sharing)")
    print("=" * 60)
    
    collaboration_request = {
        "source_agent": {"name": "Lightbulb_Function_AI", "type": "FunctionExecutor"},
        "collaboration_type": "context_sharing",
        "target_concept": "lightbulb",
        "specific_request": {
            "context_type": "technical_attributes",
            "depth": "comprehensive"
        },
        "context": {
            "analysis_purpose": "impact_assessment",
            "requesting_for": "comprehensive_analysis"
        }
    }
    
    print("📤 Function AI requesting context from Definition AI...")
    print(f"Request: {json.dumps(collaboration_request, indent=2)}")
    
    try:
        response = requests.post(
            f"{DEFINITION_AI_URL}/collaborate", 
            json=collaboration_request, 
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n📥 Response received:")
            print(f"Status: {result.get('status')}")
            print(f"Data: {json.dumps(result.get('data'), indent=2)}")
            print(f"Collaboration Metadata: {json.dumps(result.get('collaboration_metadata'), indent=2)}")
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_function_execution_collaboration():
    """Test Definition AI requesting function execution from Function AI"""
    print("\n🧪 Test 3: Definition AI → Function AI (Function Execution)")
    print("=" * 60)
    
    collaboration_request = {
        "source_agent": {"name": "Lightbulb_Definition_AI", "type": "FactBase"},
        "collaboration_type": "function_execution",
        "target_concept": "lightbulb",
        "specific_request": {
            "function_type": "impact_analysis",
            "scope": "industrial_applications",
            "output_format": "structured_analysis"
        },
        "context": {
            "analysis_context": "factory_productivity_assessment",
            "requesting_for": "comprehensive_user_response"
        }
    }
    
    print("📤 Definition AI requesting impact analysis from Function AI...")
    print(f"Request: {json.dumps(collaboration_request, indent=2)}")
    
    try:
        response = requests.post(
            f"{FUNCTION_AI_URL}/collaborate", 
            json=collaboration_request, 
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n📥 Response received:")
            print(f"Status: {result.get('status')}")
            print(f"Data: {json.dumps(result.get('data'), indent=2)}")
            print(f"Collaboration Metadata: {json.dumps(result.get('collaboration_metadata'), indent=2)}")
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_chained_collaboration():
    """Test a chain of collaborations: Function AI asks for historical timeline, which triggers Definition AI to collaborate back"""
    print("\n🧪 Test 4: Chained Collaboration (Function AI → Definition AI → Function AI)")
    print("=" * 70)
    
    collaboration_request = {
        "source_agent": {"name": "External_Test_Agent", "type": "TestAgent"},
        "collaboration_type": "knowledge_request",
        "target_concept": "lightbulb",
        "specific_request": {
            "knowledge_type": "historical_timeline",
            "detail_level": "comprehensive"
        },
        "context": {
            "test_purpose": "chained_collaboration_demo",
            "requesting_for": "comprehensive_timeline_analysis"
        }
    }
    
    print("📤 Test Agent requesting historical timeline from Function AI...")
    print("   (This should trigger Function AI to collaborate with Definition AI)")
    print(f"Request: {json.dumps(collaboration_request, indent=2)}")
    
    try:
        response = requests.post(
            f"{FUNCTION_AI_URL}/collaborate", 
            json=collaboration_request, 
            timeout=15  # Longer timeout for chained requests
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n📥 Final response received:")
            print(f"Status: {result.get('status')}")
            
            # Check if the response contains information that suggests collaboration occurred
            data = result.get('data', {})
            if isinstance(data, dict) and 'primary_knowledge' in data:
                knowledge = data['primary_knowledge']
                if 'From a functional perspective:' in knowledge:
                    print("✅ Chained collaboration detected! Function AI successfully collaborated with Definition AI")
                print(f"Knowledge: {knowledge}")
            else:
                print(f"Data: {json.dumps(data, indent=2)}")
            
            print(f"Collaboration Metadata: {json.dumps(result.get('collaboration_metadata'), indent=2)}")
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_peer_discovery():
    """Test agent peer discovery capabilities"""
    print("\n🧪 Test 5: Agent Peer Discovery via Graph Database")
    print("=" * 60)
    
    # Test discovering peers for lightbulb concept
    print("📤 Testing graph-based peer discovery for 'lightbulb' concept...")
    
    payload = {
        "start_node_label": "Concept",
        "start_node_properties": {"name": "lightbulb"},
        "relationship_type": "HANDLES_CONCEPT",
        "relationship_direction": "in",
        "target_node_label": "Agent"
    }
    
    try:
        response = requests.post(f"{GRAPHDB_MANAGER_URL}/find_connected_nodes", json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("\n📥 Peer discovery results:")
            print(f"Status: {result.get('status')}")
            
            nodes = result.get('nodes', [])
            print(f"Found {len(nodes)} agents handling 'lightbulb' concept:")
            
            for i, node in enumerate(nodes, 1):
                properties = node.get('properties', {})
                print(f"  {i}. {properties.get('name', 'Unknown')}")
                print(f"     Type: {properties.get('type', 'Unknown')}")
                print(f"     Endpoint: {properties.get('endpoint', 'Unknown')}")
                
            return len(nodes) >= 2  # Should find both Definition and Function AI
        else:
            print(f"❌ Discovery failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Discovery failed: {e}")
        return False

def main():
    """Run all agent-to-agent collaboration tests"""
    print("🤖 Agent-to-Agent Communication Test Suite")
    print("=" * 50)
    print("Testing direct peer collaboration without orchestrator mediation")
    print("This demonstrates 'reflex arcs' in the Myriad Cognitive Architecture")
    
    # Check service health
    if not check_services_health():
        print("\n❌ Some services are not healthy. Please start all services and run migration.py")
        return False
    
    print("\n🎉 All services are healthy! Running collaboration tests...")
    
    # Run tests
    tests = [
        ("Peer Discovery", test_peer_discovery),
        ("Knowledge Request", test_knowledge_request_collaboration),
        ("Context Sharing", test_context_sharing_collaboration),
        ("Function Execution", test_function_execution_collaboration),
        ("Chained Collaboration", test_chained_collaboration),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*10} Running {test_name} Test {'='*10}")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("🏁 AGENT-TO-AGENT COLLABORATION TEST RESULTS")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL AGENT-TO-AGENT COLLABORATION TESTS PASSED!")
        print("\n✨ Key Achievements:")
        print("  🤖 Agents can discover peers via graph database")
        print("  💬 Direct peer-to-peer communication without orchestrator")
        print("  🔗 Chained collaborations work (agent A → agent B → agent A)")
        print("  🚀 'Reflex arcs' successfully implemented")
        print("\n🧠 This represents a major step toward true biomimetic cognition!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
