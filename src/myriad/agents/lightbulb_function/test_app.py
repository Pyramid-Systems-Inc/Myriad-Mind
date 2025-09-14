import pytest
import json
from app import app, lightbulb_state

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset lightbulb state before each test
        lightbulb_state["is_on"] = False
        lightbulb_state["brightness"] = 0
        yield client

def test_explain_limitation_intent_success(client):
    """Test that the /query endpoint correctly handles the 'explain_limitation' intent"""
    # Prepare the request payload according to Orchestrator-to-Agent Protocol
    payload = {"intent": "explain_limitation"}
    
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
    
    # Verify correct values - this validates the roadmap requirement
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "success"
    assert response_data["data"] == "it generates significant waste heat, making it inefficient."

def test_turn_on_intent_success(client):
    """Test that the lightbulb can be turned on"""
    payload = {"intent": "turn_on"}
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "success"
    assert "turned on" in response_data["data"]
    assert "100%" in response_data["data"]  # Default brightness

def test_turn_off_intent_success(client):
    """Test that the lightbulb can be turned off"""
    payload = {"intent": "turn_off"}
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "success"
    assert response_data["data"] == "Lightbulb turned off"

def test_dim_intent_success(client):
    """Test that the lightbulb brightness can be set"""
    payload = {"intent": "dim", "args": {"brightness": 75}}
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "success"
    assert "75%" in response_data["data"]

def test_dim_intent_default_brightness(client):
    """Test that dim intent uses default brightness when not specified (missing args key)"""
    payload = {"intent": "dim"} # Tests data.get('args', {}).get('brightness', 50) when 'args' is missing
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "success"
    assert "50%" in response_data["data"]  # Default brightness

def test_dim_intent_invalid_brightness_high(client):
    """Test that dim intent rejects brightness values above 100"""
    payload = {"intent": "dim", "args": {"brightness": 150}}
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "error"
    assert "between 0 and 100" in response_data["data"]

def test_dim_intent_invalid_brightness_low(client):
    """Test that dim intent rejects brightness values below 0"""
    payload = {"intent": "dim", "args": {"brightness": -10}}
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "error"
    assert "between 0 and 100" in response_data["data"]

def test_dim_intent_invalid_brightness_type(client):
    """Test that dim intent rejects non-numeric brightness values"""
    payload = {"intent": "dim", "args": {"brightness": "invalid"}}
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "error"
    assert "Invalid brightness value" in response_data["data"]

def test_status_intent_success(client):
    """Test that the status intent returns current lightbulb state"""
    payload = {"intent": "status"}
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "success"
    assert "Lightbulb is" in response_data["data"]

def test_status_after_operations(client):
    """Test status reflects state changes after operations"""
    # Turn on the lightbulb
    client.post('/query',
                data=json.dumps({"intent": "turn_on"}),
                content_type='application/json')
    
    # Check status
    response = client.post('/query',
                          data=json.dumps({"intent": "status"}),
                          content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    
    assert "on" in response_data["data"]
    assert "100%" in response_data["data"]

def test_unknown_intent_error(client):
    """Test that unknown intents return an error"""
    payload = {"intent": "unknown_intent"}
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
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
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "error"
    assert "Missing 'intent'" in response_data["data"]

def test_dim_intent_brightness_zero(client):
    """Test dimming to 0, which should turn the light off."""
    payload = {"intent": "dim", "args": {"brightness": 0}}
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "success"
    assert "Lightbulb brightness set to 0%" in response_data["data"]
    assert lightbulb_state["is_on"] == False
    assert lightbulb_state["brightness"] == 0

def test_dim_intent_empty_args_object(client):
    """Test dim intent with an empty args object, should use default brightness."""
    payload = {"intent": "dim", "args": {}} # Tests data.get('args', {}).get('brightness', 50) when 'args' is an empty dict
    
    response = client.post('/query',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "success"
    assert "Lightbulb brightness set to 50%" in response_data["data"] # Default brightness
    assert lightbulb_state["is_on"] == True
    assert lightbulb_state["brightness"] == 50

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    
    assert response_data["status"] == "healthy"
    assert response_data["agent"] == "Lightbulb_Function_AI"

def test_malformed_json_error(client):
    """Test that malformed JSON returns an error"""
    response = client.post('/query',
                          data='{"invalid": json}',
                          content_type='application/json')
    
    assert response.status_code == 500
    response_data = json.loads(response.data)
    
    assert response_data["agent_name"] == "Lightbulb_Function_AI"
    assert response_data["status"] == "error"