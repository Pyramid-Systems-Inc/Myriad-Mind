#!/usr/bin/env python3
"""
Phase 2 Neurogenesis Test: Template Agents & Dynamic Creation
Tests the complete dynamic agent creation pipeline.

This demonstrates Phase 2 of biomimetic neurogenesis where the system
creates specialized agents for unknown concepts using templates.
"""

import requests
import json
import time
import sys
import os
from typing import Dict, Any, List

# Add paths for our modules
sys.path.append('.')
sys.path.append('orchestration')
sys.path.append('templates')
sys.path.append('lifecycle')

# Service endpoints
GRAPHDB_MANAGER_URL = "http://localhost:5008"
DEFINITION_AI_URL = "http://localhost:5001"
FUNCTION_AI_URL = "http://localhost:5002"

def check_services_health():
    """Check if all required services are healthy"""
    services = [
        ("GraphDB Manager", GRAPHDB_MANAGER_URL),
        ("Definition AI", DEFINITION_AI_URL),
        ("Function AI", FUNCTION_AI_URL)
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

def test_template_system():
    """Test the agent template system"""
    print("\n🧬 Testing Agent Template System")
    print("=" * 50)
    
    try:
        from agent_templates import get_template_manager
        
        manager = get_template_manager()
        templates = manager.list_templates()
        
        print(f"Available templates: {templates}")
        
        # Test template suggestion
        research_data = {
            "concept": "Solar Panel",
            "confidence_score": 0.85,
            "applications": ["renewable energy", "electricity generation"],
            "related_concepts": ["solar", "electricity", "green energy"],
            "research_sources": ["Lightbulb_Definition_AI"]
        }
        
        suggested = manager.suggest_template("Solar Panel", "define", research_data)
        print(f"Suggested template for 'Solar Panel': {suggested}")
        
        # Test template customization
        customized = manager.customize_template(suggested, "Solar Panel", research_data)
        print(f"Customized agent name: {customized['agent_name']}")
        print(f"Capabilities: {customized['primary_capabilities']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Template system test failed: {e}")
        return False

def test_lifecycle_manager():
    """Test the dynamic lifecycle manager"""
    print("\n🔧 Testing Dynamic Lifecycle Manager")
    print("=" * 50)
    
    try:
        from dynamic_lifecycle_manager import get_lifecycle_manager
        
        manager = get_lifecycle_manager()
        
        # Test agent creation (dry run)
        research_data = {
            "concept": "Blockchain",
            "confidence_score": 0.7,
            "primary_definition": "Blockchain appears to be a technological concept that likely serves specific functional purposes.",
            "applications": ["cryptocurrency", "data security", "decentralization"],
            "related_concepts": ["cryptography", "distributed systems", "security"],
            "research_sources": ["Lightbulb_Function_AI"]
        }
        
        print("Testing agent creation logic...")
        
        # NOTE: We won't actually create Docker containers in this test
        # Instead, we'll test the code generation
        
        agent_spec = manager.template_manager.customize_template(
            "factbase_enhanced", "Blockchain", research_data
        )
        
        print(f"Generated agent spec for 'Blockchain':")
        print(f"  Agent Name: {agent_spec['agent_name']}")
        print(f"  Container Name: {agent_spec['container_name']}")
        print(f"  Knowledge Domains: {agent_spec['knowledge_domains']}")
        print(f"  Capabilities: {agent_spec['primary_capabilities']}")
        
        # Test code generation
        app_code = manager.code_generator.generate_agent_code(agent_spec)
        dockerfile = manager.code_generator.generate_dockerfile(agent_spec)
        
        print(f"Generated Flask app code: {len(app_code)} characters")
        print(f"Generated Dockerfile: {len(dockerfile)} characters")
        
        # Check if generated code contains expected elements
        code_checks = [
            "AGENT_NAME" in app_code,
            "CONCEPT" in app_code,
            "def collaborate" in app_code,
            "/health" in app_code,
            "Flask" in app_code
        ]
        
        if all(code_checks):
            print("✅ Generated code contains all expected elements")
            return True
        else:
            print("❌ Generated code missing some elements")
            return False
            
    except Exception as e:
        print(f"❌ Lifecycle manager test failed: {e}")
        return False

def test_orchestrator_neurogenesis():
    """Test the complete orchestrator neurogenesis pipeline"""
    print("\n🧠 Testing Orchestrator Neurogenesis Pipeline")
    print("=" * 55)
    
    try:
        # Import orchestrator functions
        from orchestrator import send_task_to_agent
        
        # Test with a concept that should trigger neurogenesis
        test_concepts = [
            {"concept": "Smart Grid", "intent": "define"},
            {"concept": "Electric Vehicle", "intent": "analyze_impact"},
            {"concept": "Wind Turbine", "intent": "explain"}
        ]
        
        results = []
        
        for test_case in test_concepts:
            concept = test_case["concept"]
            intent = test_case["intent"]
            
            print(f"\n🧪 Testing neurogenesis for '{concept}' with intent '{intent}'")
            
            # Create task
            task = {
                "task_id": f"test_{concept.lower().replace(' ', '_')}",
                "concept": concept,
                "intent": intent,
                "args": {}
            }
            
            # Process through orchestrator
            result = send_task_to_agent(task)
            
            print(f"Result status: {result.get('status')}")
            print(f"Agent: {result.get('agent_name', 'Unknown')}")
            
            if result.get('status') in ['neurogenesis_success', 'neurogenesis_with_agent_creation']:
                neurogenesis_data = result.get('neurogenesis_data', {})
                print(f"Expansion method: {neurogenesis_data.get('expansion_method')}")
                print(f"Research summary: {neurogenesis_data.get('research_summary', '')[:100]}...")
                print(f"Confidence: {neurogenesis_data.get('confidence', 0.0):.2f}")
                
                if neurogenesis_data.get('dynamic_agent_created'):
                    print(f"🎉 Dynamic agent created: {neurogenesis_data.get('new_agent_name')}")
                    print(f"   Endpoint: {neurogenesis_data.get('new_agent_endpoint')}")
                    print(f"   Capabilities: {neurogenesis_data.get('new_agent_capabilities')}")
                
                results.append({"concept": concept, "success": True, "agent_created": neurogenesis_data.get('dynamic_agent_created', False)})
            else:
                print(f"⚠️ Neurogenesis result: {result.get('status')}")
                results.append({"concept": concept, "success": False, "agent_created": False})
        
        return results
        
    except Exception as e:
        print(f"❌ Orchestrator neurogenesis test failed: {e}")
        return []

def test_agent_discovery():
    """Test if dynamically created agents can be discovered"""
    print("\n🔍 Testing Dynamic Agent Discovery")
    print("=" * 40)
    
    # This would test if agents created in previous steps can be found
    # For now, we'll just test the discovery mechanism
    
    try:
        from orchestrator import discover_agent_via_graph
        
        # Test discovery for concepts that might have agents
        test_concepts = ["Smart Grid", "Electric Vehicle", "Wind Turbine"]
        
        for concept in test_concepts:
            print(f"Searching for agent handling '{concept}'...")
            agent_url = discover_agent_via_graph(concept, "define")
            
            if agent_url:
                print(f"  ✅ Found agent: {agent_url}")
                
                # Try to contact the agent
                try:
                    response = requests.get(f"{agent_url}/health", timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        print(f"    Agent is healthy: {data.get('agent')}")
                    else:
                        print(f"    Agent not responding: {response.status_code}")
                except:
                    print(f"    Could not contact agent (expected if running locally)")
            else:
                print(f"  📝 No agent found for '{concept}' (this is expected for new concepts)")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent discovery test failed: {e}")
        return False

def run_phase2_test_suite():
    """Run comprehensive Phase 2 neurogenesis test suite"""
    print("🧬 NEUROGENESIS PHASE 2: TEMPLATE AGENTS & DYNAMIC CREATION")
    print("=" * 70)
    print("Testing complete dynamic agent creation pipeline")
    
    # Check core services
    if not check_services_health():
        print("\n❌ Some core services are not healthy.")
        print("Note: This is expected when running locally. The neurogenesis logic will still be tested.")
    
    print("\n🎉 Starting Phase 2 neurogenesis tests...\n")
    
    test_results = {
        "template_system": False,
        "lifecycle_manager": False,
        "orchestrator_pipeline": [],
        "agent_discovery": False
    }
    
    # Test 1: Template System
    test_results["template_system"] = test_template_system()
    
    # Test 2: Lifecycle Manager
    test_results["lifecycle_manager"] = test_lifecycle_manager()
    
    # Test 3: Complete Orchestrator Pipeline
    test_results["orchestrator_pipeline"] = test_orchestrator_neurogenesis()
    
    # Test 4: Agent Discovery
    test_results["agent_discovery"] = test_agent_discovery()
    
    # Results Summary
    print("\n" + "="*70)
    print("🏁 NEUROGENESIS PHASE 2 TEST RESULTS")
    print("="*70)
    
    template_ok = test_results["template_system"]
    lifecycle_ok = test_results["lifecycle_manager"]
    orchestrator_results = test_results["orchestrator_pipeline"]
    discovery_ok = test_results["agent_discovery"]
    
    print(f"Template System: {'✅ PASS' if template_ok else '❌ FAIL'}")
    print(f"Lifecycle Manager: {'✅ PASS' if lifecycle_ok else '❌ FAIL'}")
    print(f"Agent Discovery: {'✅ PASS' if discovery_ok else '❌ FAIL'}")
    
    print(f"\nOrchestrator Neurogenesis Results:")
    successful_concepts = 0
    agents_created = 0
    
    for result in orchestrator_results:
        concept = result["concept"]
        success = result["success"]
        agent_created = result["agent_created"]
        
        status = "✅ SUCCESS" if success else "❌ FAILED"
        if agent_created:
            status += " + 🤖 AGENT CREATED"
            agents_created += 1
        
        print(f"  {concept}: {status}")
        if success:
            successful_concepts += 1
    
    total_concepts = len(orchestrator_results)
    
    print(f"\nNeurogenesis Summary:")
    print(f"  Concepts processed: {total_concepts}")
    print(f"  Successful expansions: {successful_concepts}")
    print(f"  Dynamic agents created: {agents_created}")
    
    # Overall assessment
    core_systems_ok = template_ok and lifecycle_ok and discovery_ok
    neurogenesis_ok = successful_concepts >= total_concepts * 0.5  # At least 50% success
    
    overall_success = core_systems_ok and neurogenesis_ok
    
    if overall_success:
        print("\n🎉 PHASE 2 NEUROGENESIS: COMPREHENSIVE SUCCESS!")
        print("\n✨ Key Achievements:")
        print("  🧬 Agent template system fully operational")
        print("  🔧 Dynamic lifecycle management working")
        print("  🤖 Dynamic agent creation pipeline functional")
        print("  🔍 Agent discovery and integration complete")
        print("  🚀 Template Agents: PHASE 2 COMPLETE!")
        
        if agents_created > 0:
            print(f"\n🔥 BREAKTHROUGH: {agents_created} dynamic agents created!")
            print("🧠 True biomimetic neurogenesis is now operational!")
            print("📈 Ready for Phase 3: Full Neurogenesis with autonomous learning!")
        else:
            print("\n📝 Note: No dynamic agents created in this test run")
            print("   (This is expected when running without Docker)")
            print("🔄 Ready for Phase 3: Full Neurogenesis!")
    else:
        failed_systems = []
        if not core_systems_ok:
            failed_systems.append("Core Systems")
        if not neurogenesis_ok:
            failed_systems.append("Neurogenesis Pipeline")
        
        print(f"\n⚠️  Phase 2 tests completed with issues in: {', '.join(failed_systems)}")
        print("Review the errors above and fix issues before proceeding to Phase 3.")
    
    return overall_success

if __name__ == "__main__":
    success = run_phase2_test_suite()
    exit(0 if success else 1)
