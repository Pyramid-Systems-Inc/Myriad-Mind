import requests
import time
import pytest

ORCHESTRATOR_URL = "http://localhost:5000"

def test_orchestrator_health():
    """Test orchestrator health endpoint"""
    try:
        response = requests.get(f"{ORCHESTRATOR_URL}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "orchestrator"
        print("✅ Health check passed")
    except requests.exceptions.ConnectionError:
        pytest.skip("Orchestrator service not running")

def test_orchestrator_status():
    """Test orchestrator status endpoint"""
    try:
        response = requests.get(f"{ORCHESTRATOR_URL}/status", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "orchestrator"
        assert "dependencies" in data
        assert "environment" in data
        print("✅ Status check passed")
    except requests.exceptions.ConnectionError:
        pytest.skip("Orchestrator service not running")

def test_orchestrator_process_query_simple():
    """Test query processing with simple format"""
    try:
        response = requests.post(
            f"{ORCHESTRATOR_URL}/process",
            json={"query": "Define a lightbulb", "user_id": "test"},
            timeout=30
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "result" in data
        print(f"✅ Simple query processing passed: {data['result'].get('status', 'unknown')}")
    except requests.exceptions.ConnectionError:
        pytest.skip("Orchestrator service not running")

def test_orchestrator_process_tasks():
    """Test query processing with tasks format"""
    try:
        tasks = [
            {
                "task_id": 1,
                "concept": "lightbulb",
                "intent": "define",
                "args": {}
            },
            {
                "task_id": 2,
                "concept": "lightbulb",
                "intent": "function",
                "args": {}
            }
        ]
        
        response = requests.post(
            f"{ORCHESTRATOR_URL}/process",
            json={"tasks": tasks},
            timeout=30
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "results" in data
        assert len(data["results"]) == 2
        print(f"✅ Tasks processing passed: {len(data['results'])} tasks completed")
    except requests.exceptions.ConnectionError:
        pytest.skip("Orchestrator service not running")

def test_orchestrator_list_agents():
    """Test agent listing"""
    try:
        response = requests.get(f"{ORCHESTRATOR_URL}/agents", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert "count" in data
        print(f"✅ Agent listing passed: {data['count']} agents found")
    except requests.exceptions.ConnectionError:
        pytest.skip("Orchestrator service not running")

def test_orchestrator_metrics():
    """Test metrics endpoint"""
    try:
        response = requests.get(f"{ORCHESTRATOR_URL}/metrics", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["service"] == "orchestrator"
        assert "features" in data
        print("✅ Metrics retrieval passed")
    except requests.exceptions.ConnectionError:
        pytest.skip("Orchestrator service not running")

def test_orchestrator_discover_agent():
    """Test agent discovery"""
    try:
        response = requests.post(
            f"{ORCHESTRATOR_URL}/discover",
            json={"concept": "lightbulb", "intent": "define"},
            timeout=10
        )
        # Either 200 (found) or 404 (not found) are acceptable
        assert response.status_code in [200, 404]
        data = response.json()
        assert "status" in data
        assert "concept" in data
        print(f"✅ Agent discovery passed: {data['status']}")
    except requests.exceptions.ConnectionError:
        pytest.skip("Orchestrator service not running")

def test_orchestrator_error_handling():
    """Test error handling with invalid request"""
    try:
        response = requests.post(
            f"{ORCHESTRATOR_URL}/process",
            json={},  # Empty request
            timeout=5
        )
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        print("✅ Error handling passed")
    except requests.exceptions.ConnectionError:
        pytest.skip("Orchestrator service not running")

if __name__ == "__main__":
    print("Running Orchestrator Service Integration Tests\n")
    print(f"Target: {ORCHESTRATOR_URL}\n")
    
    tests = [
        ("Health Check", test_orchestrator_health),
        ("Status Check", test_orchestrator_status),
        ("Simple Query", test_orchestrator_process_query_simple),
        ("Task Processing", test_orchestrator_process_tasks),
        ("List Agents", test_orchestrator_list_agents),
        ("Metrics", test_orchestrator_metrics),
        ("Discover Agent", test_orchestrator_discover_agent),
        ("Error Handling", test_orchestrator_error_handling)
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for name, test_func in tests:
        print(f"\n🧪 Running: {name}")
        try:
            test_func()
            passed += 1
        except pytest.skip.Exception as e:
            print(f"⏭️  Skipped: {e}")
            skipped += 1
        except AssertionError as e:
            print(f"❌ Failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Error: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"Test Results: {passed} passed, {failed} failed, {skipped} skipped")
    print("="*50)