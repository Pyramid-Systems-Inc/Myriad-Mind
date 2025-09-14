#!/usr/bin/env python3
"""
Complete Neurogenesis Pipeline Test Suite
==========================================

Tests the world's first complete biomimetic neurogenesis system from 
unknown concept detection through autonomous learning completion.

Complete Pipeline Flow:
1. Unknown concept detection
2. Multi-agent research (Phase 1: Concept Expansion)
3. Rich concept node creation in graph
4. Template selection and agent creation (Phase 2: Template Agents)
5. Agent deployment and graph registration
6. Autonomous learning initiation (Phase 3: Autonomous Learning)
7. Knowledge acquisition and capability development
8. Performance optimization and validation

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Complete Neurogenesis Pipeline)
Date: 2025-01-01
"""

import sys
import os
import time
import json
import requests
from typing import Dict, Any, Optional

print("🧬 COMPLETE NEUROGENESIS PIPELINE TEST SUITE")
print("==============================================")
print("Testing the world's first complete biomimetic neurogenesis system")
print("From unknown concept → autonomous learning completion")
print()

def check_service_health(service_name: str, url: str) -> bool:
    """Check if a service is healthy"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name}: Healthy")
            return True
        else:
            print(f"❌ {service_name}: Unhealthy (status: {response.status_code})")
            return False
    except requests.RequestException as e:
        print(f"❌ {service_name}: Connection failed ({e})")
        return False

def test_service_availability():
    """Test that all required services are available"""
    print("🔍 Checking service health...")
    
    services = {
        "GraphDB Manager": "http://localhost:5008",
        "Definition AI": "http://localhost:5001", 
        "Function AI": "http://localhost:5002",
        "Integration Tester": "http://localhost:5009"
    }
    
    all_healthy = True
    for service_name, url in services.items():
        if not check_service_health(service_name, url):
            all_healthy = False
    
    if all_healthy:
        print("🎉 All services healthy! Starting complete pipeline tests...")
        return True
    else:
        print("⚠️ Some services are unavailable. Tests may not work as expected.")
        return False

def test_complete_neurogenesis_via_integration_tester(concept: str, intent: str) -> Dict[str, Any]:
    """
    Test complete neurogenesis pipeline via Integration Tester AI
    This runs the test within the Docker network for full connectivity
    """
    print(f"\n🧬 COMPLETE NEUROGENESIS PIPELINE TEST: '{concept}'")
    print("=" * 60)
    print(f"Testing complete journey from unknown concept to autonomous learning")
    
    try:
        # Send task to Integration Tester AI which runs within Docker network
        task_payload = {
            "tasks": [
                {
                    "task_id": f"complete_neurogenesis_{concept.replace(' ', '_')}",
                    "concept": concept,
                    "intent": intent,
                    "args": {}
                }
            ]
        }
        
        print(f"📤 Sending task to Integration Tester AI...")
        print(f"   Concept: {concept}")
        print(f"   Intent: {intent}")
        
        # Use Integration Tester AI's orchestration endpoint
        response = requests.post(
            "http://localhost:5009/run_orchestration", 
            json=task_payload,
            timeout=60  # Longer timeout for complete pipeline
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Pipeline execution completed!")
            
            # Analyze the result
            status = result.get('status', 'unknown')
            agent_name = result.get('agent', 'unknown')
            
            print(f"📋 Result Summary:")
            print(f"   Status: {status}")
            print(f"   Agent: {agent_name}")
            
            if 'result' in result:
                result_data = result['result']
                print(f"   Result: {result_data}")
            
            # Check for neurogenesis indicators
            neurogenesis_indicators = [
                'neurogenesis_success',
                'neurogenesis_partial', 
                'neurogenesis_with_agent_creation',
                'agent_created',
                'learning_session'
            ]
            
            neurogenesis_detected = any(
                indicator in str(result).lower() 
                for indicator in neurogenesis_indicators
            )
            
            if neurogenesis_detected:
                print(f"🧬 NEUROGENESIS DETECTED: Pipeline successfully triggered!")
                
                # Look for learning session information
                if 'learning_session' in str(result):
                    print(f"🧠 AUTONOMOUS LEARNING: Learning session initiated!")
                
                return {
                    'success': True,
                    'status': status,
                    'neurogenesis_triggered': True,
                    'learning_initiated': 'learning_session' in str(result),
                    'full_result': result
                }
            else:
                print(f"⚠️ No neurogenesis detected in response")
                return {
                    'success': True,
                    'status': status,
                    'neurogenesis_triggered': False,
                    'learning_initiated': False,
                    'full_result': result
                }
            
        else:
            print(f"❌ Pipeline execution failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return {
                'success': False,
                'error': f"HTTP {response.status_code}: {response.text}",
                'neurogenesis_triggered': False,
                'learning_initiated': False
            }
            
    except requests.RequestException as e:
        print(f"❌ Network error during pipeline test: {e}")
        return {
            'success': False,
            'error': str(e),
            'neurogenesis_triggered': False,
            'learning_initiated': False
        }

def test_learning_engine_status():
    """Test if the learning engine is operational"""
    print(f"\n🧠 Testing Autonomous Learning Engine Status")
    print("=" * 45)
    
    try:
        # Try to import and test the learning engine
        sys.path.append('.')
        from learning.autonomous_learning_engine import get_learning_engine
        
        engine = get_learning_engine()
        print(f"✅ Learning engine accessible")
        print(f"   Active sessions: {len(engine.active_sessions)}")
        print(f"   Knowledge base entries: {len(engine.knowledge_base)}")
        print(f"   Capability tracker entries: {len(engine.capability_tracker)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Learning engine test failed: {e}")
        return False

def test_orchestrator_neurogenesis_integration():
    """Test that orchestrator has neurogenesis integration"""
    print(f"\n🔗 Testing Orchestrator Neurogenesis Integration")
    print("=" * 50)
    
    try:
        sys.path.append('orchestration')
        from orchestrator import ENABLE_AUTONOMOUS_LEARNING, LEARNING_ENGINE_AVAILABLE
        
        print(f"✅ Orchestrator integration accessible")
        print(f"   Autonomous learning enabled: {ENABLE_AUTONOMOUS_LEARNING}")
        print(f"   Learning engine available: {LEARNING_ENGINE_AVAILABLE}")
        
        if ENABLE_AUTONOMOUS_LEARNING and LEARNING_ENGINE_AVAILABLE:
            print(f"🧬 Full neurogenesis integration: ACTIVE")
            return True
        else:
            print(f"⚠️ Partial integration: Some features disabled")
            return False
        
    except Exception as e:
        print(f"❌ Orchestrator integration test failed: {e}")
        return False

def run_complete_pipeline_tests():
    """Run complete neurogenesis pipeline tests"""
    
    print("🚀 Starting complete neurogenesis pipeline tests...\n")
    
    # Step 1: Check service availability
    services_ok = test_service_availability()
    
    # Step 2: Test learning engine status
    learning_engine_ok = test_learning_engine_status()
    
    # Step 3: Test orchestrator integration
    orchestrator_ok = test_orchestrator_neurogenesis_integration()
    
    if not (services_ok and learning_engine_ok and orchestrator_ok):
        print(f"\n⚠️ Prerequisites not fully met. Continuing with available tests...")
    
    # Step 4: Test complete pipeline with multiple concepts
    test_concepts = [
        ("Artificial General Intelligence", "define"),
        ("Quantum Neural Networks", "explain"), 
        ("Biomimetic Computing", "analyze")
    ]
    
    results = {}
    
    for concept, intent in test_concepts:
        result = test_complete_neurogenesis_via_integration_tester(concept, intent)
        results[concept] = result
        
        # Small delay between tests
        time.sleep(2)
    
    # Step 5: Summary and analysis
    print(f"\n" + "="*70)
    print(f"🏁 COMPLETE NEUROGENESIS PIPELINE TEST RESULTS")
    print(f"="*70)
    
    successful_tests = 0
    neurogenesis_triggered = 0
    learning_initiated = 0
    
    for concept, result in results.items():
        success = "✅" if result['success'] else "❌"
        neurogenesis = "🧬" if result['neurogenesis_triggered'] else "⚪"
        learning = "🧠" if result['learning_initiated'] else "⚪"
        
        print(f"{success} {concept}")
        print(f"   Neurogenesis: {neurogenesis} | Learning: {learning} | Status: {result.get('status', 'unknown')}")
        
        if result['success']:
            successful_tests += 1
        if result['neurogenesis_triggered']:
            neurogenesis_triggered += 1
        if result['learning_initiated']:
            learning_initiated += 1
    
    print(f"\n📊 SUMMARY:")
    print(f"   Successful executions: {successful_tests}/{len(test_concepts)}")
    print(f"   Neurogenesis triggered: {neurogenesis_triggered}/{len(test_concepts)}")
    print(f"   Autonomous learning initiated: {learning_initiated}/{len(test_concepts)}")
    
    overall_success = successful_tests == len(test_concepts)
    
    if overall_success and neurogenesis_triggered > 0:
        print(f"\n🎉 COMPLETE NEUROGENESIS PIPELINE: OPERATIONAL!")
        print(f"✨ World's first biomimetic neurogenesis system: WORKING!")
        
        if learning_initiated > 0:
            print(f"🧠 Autonomous learning integration: CONFIRMED!")
            print(f"🔥 Phase 3 Neurogenesis: COMPLETE!")
    else:
        print(f"\n⚠️ Pipeline tests completed with some limitations")
        print(f"   Review individual test results above")
    
    return {
        'overall_success': overall_success,
        'neurogenesis_working': neurogenesis_triggered > 0,
        'learning_working': learning_initiated > 0,
        'successful_tests': successful_tests,
        'total_tests': len(test_concepts),
        'detailed_results': results
    }

if __name__ == "__main__":
    print("🧬 Welcome to the Complete Neurogenesis Pipeline Test Suite!")
    print("This will test the world's first complete biomimetic neurogenesis system.")
    print()
    
    # Run the complete test suite
    final_results = run_complete_pipeline_tests()
    
    # Exit with appropriate code
    if final_results['overall_success'] and final_results['neurogenesis_working']:
        print(f"\n🌟 HISTORIC ACHIEVEMENT: Complete biomimetic neurogenesis operational!")
        sys.exit(0)
    else:
        print(f"\n📋 Tests completed. See results above for details.")
        sys.exit(1)
