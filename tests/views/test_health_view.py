from app.api.health import views
from tests.views import mocks


# Test health check passes
def test_health_check_passes(test_app, monkeypatch):
    monkeypatch.setattr(views, "get_health_status", mocks.health_check_pass)
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
