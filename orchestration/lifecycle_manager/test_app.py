import pytest
import json
from .app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'Lifecycle Manager'

def test_create_agent_success(client):
    """Test the /create_agent endpoint with a valid request."""
    payload = {
        "concept_name": "new concept",
        "agent_type": "FactBase"
    }
    response = client.post('/create_agent',
                           data=json.dumps(payload),
                           content_type='application/json')
    
    assert response.status_code == 202
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['agent_name'] == 'New_concept_FactBase_AI'
    assert 'endpoint' in data
    assert 'Mocked' in data['message']

def test_create_agent_missing_fields(client):
    """Test the /create_agent endpoint with missing fields."""
    payload = {"concept_name": "incomplete"}
    response = client.post('/create_agent',
                           data=json.dumps(payload),
                           content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert "Missing 'concept_name' or 'agent_type'" in data['message']

def test_create_agent_empty_request(client):
    """Test the /create_agent endpoint with an empty request."""
    response = client.post('/create_agent',
                           data=json.dumps({}),
                           content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'