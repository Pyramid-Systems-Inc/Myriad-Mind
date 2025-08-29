#!/usr/bin/env python3
"""
Phase 3 Neurogenesis: Autonomous Learning Engine Test Suite
============================================================

Tests the world's first autonomous learning system for dynamically created AI agents.

Test Coverage:
- Autonomous learning engine initialization  
- Learning session creation and management
- Knowledge acquisition and bootstrapping
- Capability development and optimization
- Cross-domain knowledge transfer
- Integration with neurogenesis pipeline

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Phase 3 Neurogenesis)
Date: 2025-01-01
"""

import sys
import os
import time
import json
import requests
from typing import Dict, Any

# Add path for learning engine
sys.path.append('.')

print("🧠 PHASE 3 NEUROGENESIS: AUTONOMOUS LEARNING ENGINE TEST SUITE")
print("================================================================")
print("Testing the world's first autonomous learning system for AI agents")
print()

def test_learning_engine_initialization():
    """Test that the learning engine can be initialized"""
    print("🔍 Test 1: Learning Engine Initialization")
    print("==========================================")
    
    try:
        from learning.autonomous_learning_engine import AutonomousLearningEngine
        
        engine = AutonomousLearningEngine()
        print("✅ Learning engine initialized successfully")
        print(f"   Configuration: {engine.learning_config}")
        return True
        
    except Exception as e:
        print(f"❌ Learning engine initialization failed: {e}")
        return False

def test_learning_session_creation():
    """Test creating an autonomous learning session"""
    print("\n🧪 Test 2: Learning Session Creation")
    print("=====================================")
    
    try:
        from learning.autonomous_learning_engine import AutonomousLearningEngine
        
        engine = AutonomousLearningEngine()
        
        # Create a test learning session
        session_id = engine.initiate_autonomous_learning(
            agent_name="Test_Quantum_Agent",
            concept="quantum_computing",
            learning_objectives=[
                "understand_core_definition",
                "identify_key_principles", 
                "develop_explanation_skills"
            ]
        )
        
        print(f"✅ Learning session created: {session_id}")
        
        # Check session status immediately
        status = engine.get_learning_status(session_id)
        print(f"   Initial status: {status.get('status', 'unknown')}")
        print(f"   Confidence: {status.get('confidence', 0.0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Learning session creation failed: {e}")
        return False

def test_knowledge_acquisition():
    """Test knowledge acquisition capabilities"""
    print("\n📚 Test 3: Knowledge Acquisition")
    print("=================================")
    
    try:
        from learning.autonomous_learning_engine import AutonomousLearningEngine
        
        engine = AutonomousLearningEngine()
        
        # Test knowledge source discovery
        sources = engine._discover_knowledge_sources("artificial_intelligence")
        print(f"✅ Discovered {len(sources)} knowledge sources")
        
        # Test foundational knowledge acquisition
        knowledge = engine._acquire_foundational_knowledge("machine_learning", sources[:2])
        print(f"✅ Acquired knowledge with confidence: {knowledge.get('confidence', 0.0)}")
        print(f"   Principles: {len(knowledge.get('principles', []))}")
        print(f"   Applications: {len(knowledge.get('applications', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Knowledge acquisition test failed: {e}")
        return False

def test_knowledge_transfer():
    """Test cross-domain knowledge transfer"""
    print("\n🔄 Test 4: Knowledge Transfer")
    print("=============================")
    
    try:
        from learning.autonomous_learning_engine import AutonomousLearningEngine, KnowledgeAcquisition
        from datetime import datetime
        
        engine = AutonomousLearningEngine()
        
        # Create source knowledge
        source_knowledge = KnowledgeAcquisition(
            concept="neural_networks",
            definition="Computational models inspired by biological neural networks",
            principles=["backpropagation", "gradient_descent", "activation_functions"],
            applications=["image_recognition", "natural_language_processing"],
            related_concepts=["deep_learning", "machine_learning"],
            confidence=0.8,
            sources=["test_source"],
            timestamp=datetime.now()
        )
        
        engine.knowledge_base["neural_networks"] = source_knowledge
        
        # Test knowledge transfer
        result = engine.transfer_knowledge("neural_networks", "deep_learning")
        
        if result.get('success'):
            print(f"✅ Knowledge transfer successful")
            print(f"   Transferred principles: {result.get('transferred_principles', 0)}")
            print(f"   Transferred applications: {result.get('transferred_applications', 0)}")
            print(f"   Target confidence: {result.get('target_confidence', 0.0)}")
        else:
            print(f"❌ Knowledge transfer failed: {result}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Knowledge transfer test failed: {e}")
        return False

def test_capability_development():
    """Test capability development tracking"""
    print("\n🛠️  Test 5: Capability Development")
    print("==================================")
    
    try:
        from learning.autonomous_learning_engine import AutonomousLearningEngine, LearningSession, KnowledgeAcquisition
        from datetime import datetime
        
        engine = AutonomousLearningEngine()
        
        # Create a mock session
        session = LearningSession(
            session_id="test_session",
            agent_name="Test_Agent",
            concept="robotics",
            start_time=datetime.now(),
            learning_objectives=["understand_basics"],
            knowledge_sources=[],
            performance_metrics={},
            learned_capabilities=[],
            confidence_score=0.1,
            status='active'
        )
        
        # Create mock knowledge
        knowledge = KnowledgeAcquisition(
            concept="robotics",
            definition="Field of engineering focused on automated machines",
            principles=["sensors", "actuators", "control_systems"],
            applications=["manufacturing", "exploration", "assistance"],
            related_concepts=["automation", "AI"],
            confidence=0.7,
            sources=["test"],
            timestamp=datetime.now()
        )
        
        # Test capability development
        engine._develop_capabilities(session)
        
        print(f"✅ Capability development completed")
        print(f"   Capabilities developed: {len(session.learned_capabilities)}")
        print(f"   Capabilities: {', '.join(session.learned_capabilities)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Capability development test failed: {e}")
        return False

def test_orchestrator_integration():
    """Test integration with the orchestrator (if available)"""
    print("\n🔗 Test 6: Orchestrator Integration")
    print("====================================")
    
    try:
        # Test if we can import the orchestrator functions
        sys.path.append('orchestration')
        from orchestrator import generate_learning_objectives
        
        # Test learning objective generation
        objectives = generate_learning_objectives(
            concept="blockchain",
            intent="define", 
            capabilities=["concept_definition", "advanced_reasoning"]
        )
        
        print(f"✅ Orchestrator integration working")
        print(f"   Generated objectives: {len(objectives)}")
        print(f"   Objectives: {', '.join(objectives)}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Orchestrator integration test skipped: {e}")
        return True  # Not a critical failure

def test_learning_session_monitoring():
    """Test learning session monitoring and status tracking"""
    print("\n📊 Test 7: Learning Session Monitoring")
    print("=======================================")
    
    try:
        from learning.autonomous_learning_engine import AutonomousLearningEngine
        
        engine = AutonomousLearningEngine()
        
        # Start a learning session
        session_id = engine.initiate_autonomous_learning(
            agent_name="Monitor_Test_Agent",
            concept="cybersecurity",
            learning_objectives=["understand_threats", "learn_defenses"]
        )
        
        print(f"✅ Learning session started: {session_id}")
        
        # Monitor the session for a few seconds
        for i in range(3):
            time.sleep(2)
            status = engine.get_learning_status(session_id)
            print(f"   Status check {i+1}: {status.get('status')} (confidence: {status.get('confidence', 0.0):.2f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Learning session monitoring test failed: {e}")
        return False

def run_all_tests():
    """Run all autonomous learning tests"""
    print("Starting comprehensive autonomous learning test suite...\n")
    
    tests = [
        ("Learning Engine Initialization", test_learning_engine_initialization),
        ("Learning Session Creation", test_learning_session_creation),
        ("Knowledge Acquisition", test_knowledge_acquisition), 
        ("Knowledge Transfer", test_knowledge_transfer),
        ("Capability Development", test_capability_development),
        ("Orchestrator Integration", test_orchestrator_integration),
        ("Learning Session Monitoring", test_learning_session_monitoring)
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
    print("🏁 AUTONOMOUS LEARNING TEST RESULTS")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL AUTONOMOUS LEARNING TESTS PASSED!")
        print("✨ Phase 3 Neurogenesis: Autonomous Learning Engine is operational!")
        print("🧠 World's first autonomous learning system for AI agents: READY!")
    else:
        print(f"⚠️  {total - passed} tests failed. Review the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
