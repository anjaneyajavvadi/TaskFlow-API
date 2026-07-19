def get_token(client):

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

    return response.get_json()["access_token"]


def test_create_task(client):

    token = get_token(client)

    response = client.post(
        "/api/tasks/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Flask Project",
            "description": "Complete API",
            "status": "pending",
            "priority": "high"
        }
    )

    assert response.status_code == 201


def test_get_tasks(client):

    token = get_token(client)

    client.post(
        "/api/tasks/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Task One"
        }
    )

    response = client.get(
        "/api/tasks/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] == 1


def test_update_task(client):

    token = get_token(client)

    response = client.post(
        "/api/tasks/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Task"
        }
    )

    task_id = response.get_json()["task"]["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "status": "completed"
        }
    )

    assert response.status_code == 200


def test_delete_task(client):

    token = get_token(client)

    response = client.post(
        "/api/tasks/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Task"
        }
    )

    task_id = response.get_json()["task"]["id"]

    response = client.delete(
        f"/api/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200