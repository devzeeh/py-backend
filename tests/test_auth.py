import json

def test_register_user(client):
    """Test that a new user can successfully register"""
    response = client.post("/api/v1/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword123"
    })

    data = response.get_json()

    # Assert that the HTTP status code is 201 Created
    assert response.status_code == 201
    # Assert the response structure
    assert "message" in data
    assert data["message"] == "User registered successfully" # Same as the message in the route