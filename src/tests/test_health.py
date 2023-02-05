from fastapi.testclient import TestClient


def test_health(client: TestClient):
    response = client.get('/api/v1/healthcheck')

    assert response.status_code == 200

