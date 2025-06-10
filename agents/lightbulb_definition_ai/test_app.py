import pytest
import json
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_define_intent_success(client):
    """Test that the /query endpoint correctly handles the 'define' intent"""
    # Prepare the request payload according to Orchestrator-to-Agent Protocol
    payload = {"intent": "define"}
    
    # Make the POST request
    response = client.post('/query', 
                          data=json.dumps(payload),
                          content_type='application/json')
    
    # Assert response status
    assert response.status_code == 200
    
    # Parse response JSON
    response_data = json.loads(response.data)
    
    # Verify Agent-to-Orchestrator Protocol format
    assert "agent_name" in response_data
    assert "status" in response_data
    assert "data" in response_data
    
    # Verify correct values
    assert response_data["agent_name"] == "Lightbulb_Definition_AI"
    assert response_data["status"] == "success"
    assert response_data["data"] == "an electric device that produces light via an incandescent filament"

def test_unknown_intent_error(client):
    """Test that unknown intents return an error"""
    payload = {"intent": "unknown_intent"}
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Definition_AI"
    assert response_data["status"] == "error"
    assert "Unknown intent" in response_data["data"]

def test_missing_intent_error(client):
    """Test that missing intent returns an error"""
    payload = {}
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Definition_AI"
    assert response_data["status"] == "error"
    assert "Missing 'intent'" in response_data["data"]

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    
    assert response_data["status"] == "healthy"
    assert response_data["agent"] == "Lightbulb_Definition_AI"