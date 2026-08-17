import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture
def api_client():
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Authorization": "Bearer mock_token_qa_suite_2026"
    })
    return session


def test_create_new_user(api_client):
    """POST: Validate 201 status, payload creation, and response time < 2s"""
    user_payload = {
        "name": "Jane Doe",
        "username": "janedoe",
        "email": "jane@example.com"
    }
    
    response = api_client.post(f"{BASE_URL}/users", json=user_payload)
    
    # HTTP Status Assertion
    assert response.status_code == 201
    
    # SLA Response Time Assertion (< 2.0 seconds)
    assert response.elapsed.total_seconds() < 2.0, f"Response too slow: {response.elapsed.total_seconds()}s"
    
    # Body Payload & Structure Assertions
    data = response.json()
    assert isinstance(data["id"], int)
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"


def test_get_user_by_id(api_client):
    """GET: Validate 200 status, schema keys, and response time < 2s"""
    user_id = 1
    
    response = api_client.get(f"{BASE_URL}/users/{user_id}")
    
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2.0
    
    data = response.json()
    # Validate required schema keys exist in the response
    required_keys = {"id", "name", "username", "email", "address", "phone", "website", "company"}
    assert required_keys.issubset(data.keys()), "Missing required schema fields"
    assert data["id"] == user_id


def test_update_user(api_client):
    """PUT: Validate 200 status and updated values"""
    user_id = 1
    updated_payload = {
        "name": "Jane Doe Updated",
        "username": "janedoe_v2",
        "email": "jane_updated@example.com"
    }
    
    response = api_client.put(f"{BASE_URL}/users/{user_id}", json=updated_payload)
    
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2.0
    
    data = response.json()
    assert data["name"] == "Jane Doe Updated"
    assert data["username"] == "janedoe_v2"


def test_delete_user(api_client):
    """DELETE: Validate 200 status and response time < 2s"""
    user_id = 1
    
    response = api_client.delete(f"{BASE_URL}/users/{user_id}")
    
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2.0