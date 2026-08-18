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


# -------------------------------------------------------------------
# DATA-DRIVEN TEST 1: Retrieve multiple users by ID
# -------------------------------------------------------------------
@pytest.mark.parametrize("user_id, expected_name", [
    (1, "Leanne Graham"),
    (2, "Ervin Howell"),
    (3, "Clementine Bauch"),
    (4, "Patricia Lebsack")
])
def test_get_multiple_users_by_id(api_client, user_id, expected_name):
    response = api_client.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2.0
    
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == expected_name


# -------------------------------------------------------------------
# DATA-DRIVEN TEST 2: Create multiple users with varying payloads
# -------------------------------------------------------------------
@pytest.mark.parametrize("name, username, email", [
    ("Jane Doe", "janedoe", "jane@example.com"),
    ("Alex Smith", "alexs", "alex@company.org"),
    ("Sam Wilson", "samw", "sam@techcorp.io")
])
def test_create_multiple_users(api_client, name, username, email):
    user_payload = {
        "name": name,
        "username": username,
        "email": email
    }
    response = api_client.post(f"{BASE_URL}/users", json=user_payload)
    assert response.status_code == 201
    assert response.elapsed.total_seconds() < 2.0
    
    data = response.json()
    assert isinstance(data["id"], int)
    assert data["name"] == name
    assert data["username"] == username
    assert data["email"] == email


# -------------------------------------------------------------------
# DATA-DRIVEN TEST 3: Negative testing for non-existent users
# -------------------------------------------------------------------
@pytest.mark.parametrize("invalid_user_id", [9999, 8888, 7777])
def test_get_non_existent_user_returns_404(api_client, invalid_user_id):
    response = api_client.get(f"{BASE_URL}/users/{invalid_user_id}")
    assert response.status_code == 404