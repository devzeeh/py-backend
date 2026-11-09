def test_rate_limit_exceeded(client):
    """Test that hitting the register endpoint too many times triggers a 429"""
    url = "/api/v1/register"
    payload = {
        "name": "RateTest",
        "email": "ratetest@example.com",
        "password": "securepassword123"
    }

    # Your limit is set to "5 per minute"
    # Fire 5 allowed requests
    for _ in range(5):
        response = client.post(url, json=payload)
        # We expect either 201 (created) or 400 (already exists), but NOT 429 yet
        assert response.status_code != 429

    # The 6th request should trip the rate limiter
    response_blocked = client.post(url, json=payload)
    assert response_blocked.status_code == 429
    
    data = response_blocked.get_json()
    # Flask-Limiter usually returns a descriptive error message
    assert "Rate limit exceeded" in str(data) or response_blocked.status_code == 429