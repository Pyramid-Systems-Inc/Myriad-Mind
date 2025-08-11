import pytest
import json
from unittest.mock import patch, MagicMock
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

@patch('orchestration.lifecycle_manager.app.docker_client')
@patch('orchestration.lifecycle_manager.app.os.makedirs')
@patch('orchestration.lifecycle_manager.app.os.path.exists', return_value=False)
@patch('builtins.open')
@patch('orchestration.lifecycle_manager.app.shutil.copyfile')
def test_create_agent_success_mocked(mock_copy, mock_open, mock_exists, mock_makedirs, mock_docker_client, client):
    """Test the /create_agent endpoint with Docker interactions mocked."""
    # Mock the Docker client's methods
    mock_image = MagicMock()
    mock_image.tags = ['new_concept_factbase_ai:latest']
    mock_container = MagicMock()
    mock_container.id = 'mock_container_id'
    mock_container.name = 'new_concept_factbase_ai'
    
    mock_docker_client.images.build.return_value = (mock_image, [])
    mock_docker_client.containers.run.return_value = mock_container
    
    payload = {
        "concept_name": "new concept",
        "agent_type": "FactBase"
    }
    response = client.post('/create_agent',
                           data=json.dumps(payload),
                           content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['agent_name'] == 'New_concept_FactBase_AI'
    assert data['container_id'] == 'mock_container_id'
    assert 'deployed successfully' in data['message']
    
    # Verify that file and docker operations were called
    mock_makedirs.assert_called_once()
    mock_copy.assert_called_once()
    mock_docker_client.images.build.assert_called_once()
    mock_docker_client.containers.run.assert_called_once()

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

@patch('orchestration.lifecycle_manager.app.os.path.exists', return_value=True)
def test_create_agent_already_exists(mock_exists, client):
    """Test creating an agent that already exists."""
    payload = {
        "concept_name": "existing concept",
        "agent_type": "FactBase"
    }
    response = client.post('/create_agent',
                           data=json.dumps(payload),
                           content_type='application/json')
                            
    assert response.status_code == 409
    data = json.loads(response.data)
    assert data['status'] == 'error'
    assert "already exists" in data['message']