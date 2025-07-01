#!/usr/bin/env python3
"""
Integration Test for Enhanced Input Processor
Implements Task 3.1.8: Integration Testing with Existing System

This test verifies that the Enhanced Input Processor integrates properly
with the existing Orchestrator and agents for end-to-end functionality.
"""

import json
import requests
import time
import sys
from typing import Dict, Any

def test_input_processor_service():
    """Test that the Input Processor service is running and responsive"""
    try:
        response = requests.get('http://localhost:5003/health', timeout=5)
        if response.status_code == 200:
            print("✅ Input Processor service is healthy")
            health_data = response.json()
            print(f"   Service: {health_data.get('service')}")
            print(f"   Version: {health_data.get('version')}")
            print(f"   Capabilities: {health_data.get('capabilities')}")
            return True
        else:
            print(f"❌ Input Processor health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to Input Processor service: {e}")
        return False

def test_query_analysis():
    """Test the query analysis endpoint"""
    print("\n--- Testing Query Analysis ---")
    
    test_queries = [
        "What is a lightbulb?",
        "Why was the lightbulb important for factories?",
        "Compare LED and incandescent lighting",
        "Tell me about drive"  # Ambiguous query
    ]
    
    for query in test_queries:
        print(f"\nAnalyzing: '{query}'")
        
        try:
            payload = {"query": query}
            response = requests.post(
                'http://localhost:5003/analyze',
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                analysis = data['analysis']
                
                print(f"  Intent: {analysis['intent_analysis']['primary_intent']} "
                      f"(confidence: {analysis['intent_analysis']['confidence']:.2f})")
                print(f"  Concepts: {analysis['parsed_query']['concepts']}")
                print(f"  Complexity: {analysis['parsed_query']['complexity_score']:.2f}")
                print(f"  Estimated agents: {analysis['parsed_query']['estimated_agents_needed']}")
                
                if analysis['ambiguity_analysis']['is_ambiguous']:
                    print(f"  ⚠️  Ambiguity detected: {analysis['ambiguity_analysis']['ambiguous_elements']}")
                    print(f"      Suggestions: {analysis['ambiguity_analysis']['suggested_clarifications']}")
                else:
                    print("  ✅ No ambiguity detected")
                    
            else:
                print(f"  ❌ Analysis failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Request failed: {e}")

def test_basic_task_generation():
    """Test basic task list generation for orchestrator compatibility"""
    print("\n--- Testing Basic Task Generation ---")
    
    query = "What is a lightbulb?"
    print(f"Processing: '{query}'")
    
    try:
        payload = {"query": query}
        response = requests.post(
            'http://localhost:5003/process/basic',
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            task_list = data['task_list']
            
            print(f"✅ Generated task list with query_id: {task_list['query_id']}")
            print(f"   Number of tasks: {len(task_list['tasks'])}")
            
            for i, task in enumerate(task_list['tasks'], 1):
                print(f"   Task {i}: {task['intent']} -> {task['concept']}")
                if task.get('args'):
                    print(f"      Args: {task['args']}")
            
            return task_list
        else:
            print(f"❌ Task generation failed: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def test_enhanced_task_generation():
    """Test enhanced task list generation with full protocol"""
    print("\n--- Testing Enhanced Task Generation ---")
    
    query = "Why was the lightbulb important for factories during industrialization?"
    print(f"Processing complex query: '{query}'")
    
    try:
        payload = {
            "query": query,
            "user_context": {
                "session_id": "integration_test_session",
                "preferred_detail_level": "detailed"
            }
        }
        
        response = requests.post(
            'http://localhost:5003/process',
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            enhanced_task_list = data['enhanced_task_list']
            
            print(f"✅ Generated enhanced task list")
            print(f"   Protocol version: {enhanced_task_list['protocol_version']}")
            print(f"   Query ID: {enhanced_task_list['query_metadata']['query_id']}")
            print(f"   Number of tasks: {len(enhanced_task_list['task_list'])}")
            
            # Show parsed query details
            parsed = enhanced_task_list['parsed_query']
            print(f"   Primary intent: {parsed['primary_intent']}")
            print(f"   Concepts: {parsed['concepts']}")
            print(f"   Relationships: {len(parsed['relationships'])} found")
            print(f"   Complexity score: {parsed['complexity_score']:.2f}")
            
            # Show tasks with priorities and dependencies
            for task in enhanced_task_list['task_list']:
                deps = f" (depends on: {task['dependencies']})" if task['dependencies'] else ""
                print(f"   Task {task['task_id']}: {task['intent']} -> {task['concept']} "
                      f"[Priority: {task['priority']}]{deps}")
            
            # Check for ambiguity info
            if enhanced_task_list.get('ambiguity_info'):
                ambiguity = enhanced_task_list['ambiguity_info']
                if ambiguity['detected']:
                    print(f"   ⚠️  Ambiguity detected: {ambiguity['elements']}")
                    if ambiguity.get('resolution'):
                        print(f"      Resolved: {ambiguity['resolution']['resolved']}")
            
            return enhanced_task_list
        else:
            print(f"❌ Enhanced task generation failed: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def test_orchestrator_integration():
    """Test integration with the existing orchestrator"""
    print("\n--- Testing Orchestrator Integration ---")
    
    # First, generate a task list from the Input Processor
    task_list = test_basic_task_generation()
    if not task_list:
        print("❌ Cannot test orchestrator integration - task generation failed")
        return False
    
    # Import the orchestrator to test integration
    try:
        sys.path.append('.')
        from orchestration.orchestrator import process_tasks
        
        print("✅ Successfully imported orchestrator")
        
        # Process the tasks using the existing orchestrator
        print("Processing tasks through orchestrator...")
        results = process_tasks(task_list['tasks'])
        
        print(f"✅ Orchestrator processed {len(results)} tasks")
        
        for task_id, result in results.items():
            status = result.get('status', 'unknown')
            agent_name = result.get('agent_name', 'unknown')
            print(f"   Task {task_id}: {status} from {agent_name}")
            
            if status == 'success':
                data_preview = str(result.get('data', ''))[:50]
                print(f"      Data: {data_preview}...")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import orchestrator: {e}")
        return False
    except Exception as e:
        print(f"❌ Orchestrator integration failed: {e}")
        return False

def test_end_to_end_flow():
    """Test complete end-to-end flow from query to agent results"""
    print("\n--- Testing End-to-End Flow ---")
    
    query = "Define a lightbulb and explain its limitation"
    print(f"End-to-end test with query: '{query}'")
    
    # Step 1: Process query through Input Processor
    try:
        payload = {"query": query}
        response = requests.post(
            'http://localhost:5003/process/basic',
            json=payload,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ Input processing failed: {response.status_code}")
            return False
        
        task_list = response.json()['task_list']
        print(f"✅ Step 1: Input Processor generated {len(task_list['tasks'])} tasks")
        
    except Exception as e:
        print(f"❌ Step 1 failed: {e}")
        return False
    
    # Step 2: Process through Orchestrator
    try:
        sys.path.append('.')
        from orchestration.orchestrator import process_tasks
        
        results = process_tasks(task_list['tasks'])
        print(f"✅ Step 2: Orchestrator processed tasks, got {len(results)} results")
        
        # Check if we got successful results
        successful_results = [r for r in results.values() if r.get('status') == 'success']
        if successful_results:
            print(f"✅ Step 3: Got {len(successful_results)} successful agent responses")
            
            # Show sample results
            for i, result in enumerate(successful_results[:2], 1):
                agent_name = result.get('agent_name', 'Unknown')
                data_preview = str(result.get('data', ''))[:100]
                print(f"   Result {i} from {agent_name}: {data_preview}...")
            
            print("✅ End-to-end flow completed successfully!")
            return True
        else:
            print("❌ No successful agent responses received")
            return False
            
    except Exception as e:
        print(f"❌ Steps 2-3 failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🧪 Enhanced Input Processor Integration Tests")
    print("=" * 50)
    
    # Test service availability
    if not test_input_processor_service():
        print("\n❌ Input Processor service is not available. Please start it first:")
        print("   docker-compose up input_processor")
        print("   or")
        print("   python -m processing.input_processor.app")
        return False
    
    # Run all tests
    test_query_analysis()
    test_basic_task_generation()
    test_enhanced_task_generation()
    
    # Integration tests (require orchestrator)
    orchestrator_works = test_orchestrator_integration()
    if orchestrator_works:
        test_end_to_end_flow()
    else:
        print("\n⚠️  Orchestrator integration tests skipped - orchestrator not available")
    
    print("\n" + "=" * 50)
    print("🎉 Integration testing completed!")
    print("\nNext steps:")
    print("1. Start all services: docker-compose up --build")
    print("2. Test the complete system with various queries")
    print("3. Monitor performance and accuracy")

if __name__ == "__main__":
    main()
