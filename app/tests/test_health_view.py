import json


# Test health check passes
def test_health_check_passes(test_app):
    client = test_app.test_client()

    response = client.get("/health", headers={"Accept": "application/json"})
    if response.status_code != 200:
        raise AssertionError

    data = json.loads(response.get_json())
    if data["health"] != "good":
        raise AssertionError


# Test health check fails
def test_health_check_fails(test_app):
    test_app.config["HEALTHCHECK_FILE_PATH"] = "dummy.txt"
    client = test_app.test_client()

    response = client.get("/health", headers={"Accept": "application/json"})
    if response.status_code != 404:
        raise AssertionError

    data = json.loads(response.get_json())
    if data["health"] != "bad":
        raise AssertionError


# Test health check fails due to invalid headers
def test_health_check_fails_invalid_headers(test_app):
    test_app.config["HEALTHCHECK_FILE_PATH"] = "dummy.txt"
    client = test_app.test_client()

    response = client.get("/health")
    if response.status_code != 415:
        raise AssertionError

    data = response.get_json()
    if "application/json" not in data["message"]:
        raise AssertionError
