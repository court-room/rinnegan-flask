from app.api.health import views
from tests import mock_objects


# Test health check passes
def test_health_check_passes(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_health_status", mock_objects.health_check_pass
    )
    client = test_app.test_client()
    response = client.get(
        "/health",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["health"] == "good"


# Test health check fails
def test_health_check_fails(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_health_status", mock_objects.health_check_fails
    )
    client = test_app.test_client()
    response = client.get(
        "/health",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 404

    data = response.get_json()
    assert data["health"] == "bad"
