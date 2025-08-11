# orchestration/agent_registry_service/test_app.py
import pytest
import json
from .app import app, AGENT_DB

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    # Clear the in-memory DB before each test
    AGENT_DB.clear()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'Agent Registry Service'

def test_register_agent_success(client):
    """Test successful agent registration."""
    payload = {
      "agent_name": "Weather_AI",
      "concept": "weather",
      "intent_map": {
        "get_forecast": "/forecast",
        "get_current": "/current"
      },
      "endpoint": "http://weather_ai:5010"
    }
    response = client.post('/register', json=payload)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['registration_response']['status'] == 'success'
    assert len(AGENT_DB) == 2
    assert AGENT_DB[('weather', 'get_forecast')]['agent_name'] == 'Weather_AI'

def test_register_agent_invalid_payload(client):
    """Test agent registration with invalid payload."""
    payload = {"agent_name": "Incomplete_AI"}
    response = client.post('/register', json=payload)
    assert response.status_code == 400

def test_discover_agent_success(client):
    """Test successful agent discovery."""
    # First, register an agent
    register_payload = {
      "agent_name": "Weather_AI",
      "concept": "weather",
      "intent_map": { "get_forecast": "/forecast" },
      "endpoint": "http://weather_ai:5010"
    }
    client.post('/register', json=register_payload)

    # Now, discover it
    discover_payload = {"concept": "weather", "intent": "get_forecast"}
    response = client.post('/discover', json=discover_payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['agent_name'] == 'Weather_AI'
    assert data['endpoint'] == 'http://weather_ai:5010/forecast'

def test_discover_agent_not_found(client):
    """Test discovering a non-existent agent."""
    discover_payload = {"concept": "nonexistent", "intent": "action"}
    response = client.post('/discover', json=discover_payload)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['status'] == 'not_found'

def test_list_agents(client):
    """Test listing all registered agents."""
    register_payload = {
      "agent_name": "Weather_AI",
      "concept": "weather",
      "intent_map": { "get_forecast": "/forecast" },
      "endpoint": "http://weather_ai:5010"
    }
    client.post('/register', json=register_payload)

    response = client.get('/list')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "('weather', 'get_forecast')" in data['registered_agents']