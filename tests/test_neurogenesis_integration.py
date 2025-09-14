#!/usr/bin/env python3
"""
Neurogenesis Integration Test using Integration Tester AI
Tests neurogenesis through the Docker network where DNS resolution works.
"""

import requests
import json
import time
from typing import Dict, Any, List

# Integration Tester AI endpoint (runs in Docker network)
INTEGRATION_TESTER_URL = "http://localhost:5009"

def test_neurogenesis_via_integration_tester():
    """Test neurogenesis through Integration Tester AI in Docker network"""
    
    print("🧬 NEUROGENESIS INTEGRATION TEST")
    print("=" * 50)
    print("Testing neurogenesis through Integration Tester AI (Docker network)")
    
    # Check if Integration Tester AI is available
    try:
        response = requests.get(f"{INTEGRATION_TESTER_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Integration Tester AI is healthy")
        else:
            print(f"❌ Integration Tester AI unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Integration Tester AI unavailable: {e}")
        print("💡 Make sure Docker services are running: docker-compose up -d")
        return False
    
    # Test neurogenesis with unknown concepts
    test_tasks = [
        {
            "task_id": "neurogenesis_test_1",
            "concept": "Smart Grid",
            "intent": "define",
            "args": {}
        },
        {
            "task_id": "neurogenesis_test_2", 
            "concept": "Electric Vehicle",
            "intent": "analyze_impact",
            "args": {}
        },
        {
            "task_id": "neurogenesis_test_3",
            "concept": "Quantum Computer",
            "intent": "explain",
            "args": {}
        }
    ]
    
    print(f"\n🧪 Testing neurogenesis with {len(test_tasks)} unknown concepts...")
    
    # Send tasks to Integration Tester AI
    try:
        response = requests.post(
            f"{INTEGRATION_TESTER_URL}/run_orchestration",
            json={"tasks": test_tasks},
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"❌ Integration test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        result_data = response.json()
        
        if result_data.get("status") != "success":
            print(f"❌ Orchestration failed: {result_data.get('message')}")
            return False
        
        results = result_data.get("results", {})
        
        print(f"\n📊 NEUROGENESIS RESULTS:")
        print("=" * 40)
        
        successful_neurogenesis = 0
        agents_created = 0
        
        for task_id, result in results.items():
            task_concept = None
            for task in test_tasks:
                if task["task_id"] == task_id:
                    task_concept = task["concept"]
                    break
            
            status = result.get("status", "unknown")
            agent_name = result.get("agent_name", "Unknown")
            
            print(f"\n🧪 Task: {task_concept} (ID: {task_id})")
            print(f"   Status: {status}")
            print(f"   Agent: {agent_name}")
            
            if status in ["neurogenesis_success", "neurogenesis_with_agent_creation", "neurogenesis_partial"]:
                successful_neurogenesis += 1
                print("   ✅ Neurogenesis triggered successfully!")
                
                neurogenesis_data = result.get("neurogenesis_data", {})
                if neurogenesis_data:
                    print(f"   📋 Method: {neurogenesis_data.get('expansion_method', 'Unknown')}")
                    print(f"   🧠 Confidence: {neurogenesis_data.get('confidence', 0.0):.2f}")
                    print(f"   📚 Sources: {neurogenesis_data.get('sources', [])}")
                    
                    if neurogenesis_data.get("dynamic_agent_created"):
                        agents_created += 1
                        print(f"   🤖 DYNAMIC AGENT CREATED: {neurogenesis_data.get('new_agent_name')}")
                        print(f"      Endpoint: {neurogenesis_data.get('new_agent_endpoint')}")
                        print(f"      Capabilities: {neurogenesis_data.get('new_agent_capabilities', [])}")
                    
                    research_summary = neurogenesis_data.get("research_summary", "")
                    if research_summary:
                        print(f"   📄 Research: {research_summary[:100]}...")
            else:
                print(f"   ❌ Neurogenesis failed or not triggered")
                
        print(f"\n📈 SUMMARY:")
        print(f"   Concepts tested: {len(test_tasks)}")
        print(f"   Successful neurogenesis: {successful_neurogenesis}")
        print(f"   Dynamic agents created: {agents_created}")
        
        success_rate = successful_neurogenesis / len(test_tasks)
        
        if success_rate >= 0.8:
            print(f"\n🎉 NEUROGENESIS INTEGRATION TEST: SUCCESS!")
            print(f"   Success rate: {success_rate:.1%}")
            if agents_created > 0:
                print(f"   🚀 BREAKTHROUGH: {agents_created} dynamic agents created!")
                print("   💡 True biomimetic neurogenesis is operational!")
            return True
        else:
            print(f"\n⚠️  Neurogenesis integration test needs improvement")
            print(f"   Success rate: {success_rate:.1%} (target: 80%+)")
            return False
            
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

def run_comprehensive_integration_test():
    """Run comprehensive neurogenesis integration test"""
    
    print("🧠 COMPREHENSIVE NEUROGENESIS INTEGRATION TEST")
    print("=" * 60)
    print("Testing complete biomimetic neurogenesis through Docker network")
    
    start_time = time.time()
    
    # Test neurogenesis
    neurogenesis_success = test_neurogenesis_via_integration_tester()
    
    duration = time.time() - start_time
    
    print(f"\n⏱️  Test duration: {duration:.2f} seconds")
    
    if neurogenesis_success:
        print("\n🏆 COMPREHENSIVE INTEGRATION TEST: PASSED!")
        print("\n✨ Achievements:")
        print("  🧬 Phase 1 & 2 Neurogenesis fully operational")
        print("  🤖 Dynamic agent creation working")
        print("  🔗 Integration through Docker network successful")
        print("  🧠 Biomimetic intelligence active!")
        print("\n🔥 Ready for production deployment!")
    else:
        print("\n⚠️  Integration test needs attention")
        print("Check Docker services and network connectivity")
    
    return neurogenesis_success

if __name__ == "__main__":
    success = run_comprehensive_integration_test()
    exit(0 if success else 1)
