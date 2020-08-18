import json

from app.api.auth import views
from app.tests import mock_objects


# Test user registration passes
def test_user_registration(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_by_email", mock_objects.get_no_user_by_email,
    )

    monkeypatch.setattr(views, "add_user", mock_objects.add_user)

    client = test_app.test_client()

    response = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test_user@mail.com",
                "password": "test_password",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 201:
        raise AssertionError

    data = response.get_json()
    if "password" in data.keys():
        raise AssertionError
    if data["id"] != 1:
        raise AssertionError
    if data["username"] != "test_user":
        raise AssertionError
    if data["email"] != "test_user@mail.com":
        raise AssertionError


# Test user registration fails due to empty data
def test_user_registration_empty_data(test_app):
    client = test_app.test_client()

    response = client.post(
        "/auth/register",
        data=json.dumps({}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 400:
        raise AssertionError

    data = response.get_json()
    if "Input payload validation failed" not in data["message"]:
        raise AssertionError


# Test user registration fails due to invalid data
def test_user_registration_invalid_data(test_app):
    client = test_app.test_client()

    response = client.post(
        "/auth/register",
        data=json.dumps({"username": "test_user"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 400:
        raise AssertionError

    data = response.get_json()
    if "Input payload validation failed" not in data["message"]:
        raise AssertionError


# Test user registration fails due to duplicate entry
def test_user_registration_duplicate_entry(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_by_email", mock_objects.get_user_by_email
    )

    monkeypatch.setattr(views, "add_user", mock_objects.add_user)

    client = test_app.test_client()

    response = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test_user@email.com",
                "password": "test_password",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 400:
        raise AssertionError

    data = response.get_json()
    if "test_user@email.com is already registered" not in data["message"]:
        raise AssertionError


# Test user registration fails due to invalid headers
def test_user_registration_invalid_header(test_app):
    client = test_app.test_client()
    response = client.post(
        "/auth/register",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 415:
        raise AssertionError

    data = response.get_json()
    if "define Content-Type header" not in data["message"]:
        raise AssertionError

    response = client.post(
        "/auth/register",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code != 415:
        raise AssertionError

    data = response.get_json()
    if "supported is application/json" not in data["message"]:
        raise AssertionError


# Test user login passes
def test_user_login(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_by_email", mock_objects.get_user_object_by_email,
    )
    monkeypatch.setattr(views, "add_token", mock_objects.add_token)
    monkeypatch.setattr(
        views, "password_matches", mock_objects.password_matches
    )

    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps(
            {"email": "test_user@mail.com", "password": "test_password"}
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 200:
        raise AssertionError

    data = response.get_json()

    if not data["access_token"]:
        raise AssertionError
    if not data["refresh_token"]:
        raise AssertionError


# Test user login fails due to wrong password
def test_user_login_wrong_password(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_by_email", mock_objects.get_user_by_email,
    )
    monkeypatch.setattr(
        views, "password_matches", mock_objects.password_not_matches
    )
    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps(
            {"email": "test_user@mail.com", "password": "test_password"}
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 401:
        raise AssertionError

    data = response.get_json()

    if "Invalid password for" not in data["message"]:
        raise AssertionError


# Test user login fails due to unregistered user
def test_user_login_unregistered_user(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_by_email", mock_objects.get_no_user_by_email,
    )
    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps(
            {"email": "test_user@mail.com", "password": "test_password"}
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 404:
        raise AssertionError

    data = response.get_json()

    if "test_user@mail.com does not exists" not in data["message"]:
        raise AssertionError


# Test user login fails due to invalid header
def test_user_login_invalid_header(test_app):
    client = test_app.test_client()
    response = client.post(
        "/auth/login",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 415:
        raise AssertionError

    data = response.get_json()
    if "define Content-Type header" not in data["message"]:
        raise AssertionError

    response = client.post(
        "/auth/login",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code != 415:
        raise AssertionError

    data = response.get_json()
    if "supported is application/json" not in data["message"]:
        raise AssertionError


# Test refresh token passes
def test_refresh_token(test_app, monkeypatch):
    monkeypatch.setattr(
        views, "get_user_id_by_token", mock_objects.get_user_id_by_token,
    )
    monkeypatch.setattr(views, "update_token", mock_objects.update_token)

    client = test_app.test_client()
    response = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "refresh_token"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 200:
        raise AssertionError

    data = response.get_json()
    if not data["refresh_token"]:
        raise AssertionError
    if not data["access_token"]:
        raise AssertionError


# Test refresh token fails due to expired token
def test_refresh_token_expired(test_app, monkeypatch):
    monkeypatch.setattr(
        views,
        "get_user_id_by_token",
        mock_objects.get_expired_token_exception,
    )
    monkeypatch.setattr(views, "update_token", mock_objects.update_token)

    client = test_app.test_client()
    response = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "refresh_token"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 401:
        raise AssertionError

    data = response.get_json()
    if "Token expired" not in data["message"]:
        raise AssertionError


# Test refresh token fails due to invalid token
def test_refresh_token_invalid(test_app, monkeypatch):
    monkeypatch.setattr(
        views,
        "get_user_id_by_token",
        mock_objects.get_invalid_token_exception,
    )
    monkeypatch.setattr(views, "update_token", mock_objects.update_token)

    client = test_app.test_client()
    response = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "refresh_token"}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 401:
        raise AssertionError

    data = response.get_json()
    if "Invalid token" not in data["message"]:
        raise AssertionError


# Test refresh token fails due to invalid headers
def test_refresh_token_invalid_header(test_app):
    client = test_app.test_client()
    response = client.post(
        "/auth/refresh",
        data=json.dumps({"refresh_token": "refresh"}),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 415:
        raise AssertionError

    data = response.get_json()
    if "define Content-Type header" not in data["message"]:
        raise AssertionError

    response = client.post(
        "/auth/refresh",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code != 415:
        raise AssertionError

    data = response.get_json()
    if "supported is application/json" not in data["message"]:
        raise AssertionError
