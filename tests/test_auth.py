def test_register(client):

    response = client.post(
        "/api/auth/register",
        json={
            "username": "loki",
            "email": "loki@gmail.com",
            "password": "123456"
        }
    )
    print(response.get_json())

    assert response.status_code == 201


def test_login(client):

    client.post(
        "/api/auth/register",
        json={
            "username": "loki",
            "email": "loki@gmail.com",
            "password": "123456"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "loki@gmail.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "access_token" in data