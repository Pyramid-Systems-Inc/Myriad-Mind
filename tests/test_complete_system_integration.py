#!/usr/bin/env python3
"""
Complete System Integration Test
Implements Task 3.2.6: Integration Testing with Complete System

This test verifies end-to-end functionality from raw query through Input Processor,
Orchestrator, agents, and Output Processor to final formatted response.
"""

import json
import requests
import time
import sys
from typing import Dict, Any, Optional

def test_service_health():
    """Test that all services are running and healthy"""
    services = {
        'Input Processor': 'http://localhost:5003/health',
        'Output Processor': 'http://localhost:5004/health',
        'Lightbulb Definition AI': 'http://localhost:5001/health',
        'Lightbulb Function AI': 'http://localhost:5002/health',
        'GraphDB Manager AI': 'http://localhost:5008/health',
        'Integration Tester AI': 'http://localhost:5009/health'
    }
    
    print("🔍 Checking service health...")
    all_healthy = True
    
    for service_name, health_url in services.items():
        try:
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {service_name}: Healthy")
            else:
                print(f"  ❌ {service_name}: Unhealthy (status: {response.status_code})")
                all_healthy = False
        except requests.exceptions.RequestException as e:
            print(f"  ❌ {service_name}: Cannot connect ({e})")
            all_healthy = False
    
    return all_healthy

def test_input_processor_integration():
    """Test Input Processor generates valid task lists"""
    print("\n🧠 Testing Input Processor Integration...")
    
    test_query = "Why was the lightbulb important for factories?"
    
    try:
        payload = {"query": test_query}
        response = requests.post(
            'http://localhost:5003/process/basic',
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            task_list = data['task_list']
            
            print(f"  ✅ Input Processor generated task list")
            print(f"     Query ID: {task_list['query_id']}")
            print(f"     Tasks: {len(task_list['tasks'])}")
            
            for i, task in enumerate(task_list['tasks'], 1):
                print(f"     Task {i}: {task['intent']} -> {task['concept']}")
            
            return task_list
        else:
            print(f"  ❌ Input Processor failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ❌ Input Processor error: {e}")
        return None

def test_orchestrator_integration(task_list: Dict[str, Any]):
    """
    Test Orchestrator by sending the task list to the Integration Tester service,
    which runs the orchestration logic inside the Docker network.
    """
    print("\n🎯 Testing Orchestrator Integration (via Integration Tester AI)...")
    
    try:
        # The payload for the tester is just the list of tasks
        payload = {"tasks": task_list['tasks']}
        response = requests.post(
            'http://localhost:5009/run_orchestration',
            json=payload,
            timeout=20 # Allow more time for orchestration
        )

        if response.status_code != 200:
            print(f"  ❌ Integration Tester service returned an error: {response.status_code}")
            print(f"     Response: {response.text}")
            return None

        data = response.json()
        if data['status'] != 'success':
            print(f"  ❌ Orchestration failed inside the tester: {data.get('message')}")
            return None
            
        results = data['results']
        print(f"  ✅ Orchestrator processed {len(results)} tasks")
        
        successful_results = {}
        for task_id, result in results.items():
            status = result.get('status', 'unknown')
            agent_name = result.get('agent_name', 'unknown')
            
            if status == 'success':
                successful_results[task_id] = result
                data_preview = str(result.get('data', ''))[:50]
                print(f"     Task {task_id}: ✅ {agent_name} - {data_preview}...")
            else:
                error_msg = result.get('error_message', 'No details')
                print(f"     Task {task_id}: ❌ {agent_name} - {status} ({error_msg})")
        
        if successful_results:
            # Create collected results format for Output Processor
            collected_results = {
                "query_id": task_list['query_id'],
                "collected_results": successful_results
            }
            return collected_results
        else:
            print("  ❌ No successful agent responses")
            return None
            
    except Exception as e:
        print(f"  ❌ Orchestrator integration failed: {e}")
        return None

def test_output_processor_integration(collected_results: Dict[str, Any]):
    """Test Output Processor synthesizes and formats final response"""
    print("\n📝 Testing Output Processor Integration...")
    
    try:
        response = requests.post(
            'http://localhost:5004/synthesize/basic',
            json=collected_results,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"  ✅ Output Processor synthesis successful")
            print(f"     Query ID: {data['query_id']}")
            print(f"     Confidence: {data['confidence']:.2f}")
            print(f"     Processing time: {data['processing_time_ms']}ms")
            print(f"     Final answer preview: {data['final_answer'][:100]}...")
            
            return data
        else:
            print(f"  ❌ Output Processor failed: {response.status_code}")
            print(f"     Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"  ❌ Output Processor error: {e}")
        return None

def test_complete_end_to_end():
    """Test complete end-to-end flow with timing"""
    print("\n🎯 Testing Complete End-to-End Flow...")
    
    start_time = time.time()
    
    # Step 1: Input Processing
    step1_start = time.time()
    task_list = test_input_processor_integration()
    step1_time = time.time() - step1_start
    
    if not task_list:
        print("  ❌ End-to-end test failed at Input Processing")
        return False
    
    # Step 2: Orchestration
    step2_start = time.time()
    collected_results = test_orchestrator_integration(task_list)
    step2_time = time.time() - step2_start
    
    if not collected_results:
        print("  ❌ End-to-end test failed at Orchestration")
        return False
    
    # Step 3: Output Processing
    step3_start = time.time()
    final_response = test_output_processor_integration(collected_results)
    step3_time = time.time() - step3_start
    
    if not final_response:
        print("  ❌ End-to-end test failed at Output Processing")
        return False
    
    total_time = time.time() - start_time
    
    print(f"\n✅ Complete End-to-End Test SUCCESSFUL!")
    print(f"   Total time: {total_time:.2f}s")
    print(f"   Step 1 (Input): {step1_time:.2f}s")
    print(f"   Step 2 (Orchestration): {step2_time:.2f}s")
    print(f"   Step 3 (Output): {step3_time:.2f}s")
    print(f"   Final answer: {final_response['final_answer']}")
    
    return True

def main():
    """Run complete system integration tests"""
    print("🧪 Complete System Integration Tests")
    print("=" * 60)
    
    # Check service health first
    if not test_service_health():
        print("\n❌ Some services are not healthy. Please start all services:")
        print("   docker-compose up --build")
        return False
    
    print("\n🎉 All services are healthy! Running integration tests...")
    
    # Test complete end-to-end
    print("\n" + "=" * 40)
    print("COMPLETE END-TO-END TEST")
    print("=" * 40)
    
    success = test_complete_end_to_end()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
    else:
        print("❌ Some integration tests failed.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)