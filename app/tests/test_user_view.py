import json


# Test user creation passes
def test_add_user(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/users",
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

    if response.status_code != 201:
        raise AssertionError

    data = response.get_json()
    if "id" not in data.keys():
        raise AssertionError
    if "test_user@email.com" not in data["message"]:
        raise AssertionError


# Test user creation fails due to empty data
def test_add_user_empty_data(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/users",
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


# Test user creation fails due to invalid data
def test_add_user_invalid_data(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
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


# Test user creation fails due to duplicate entry
def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
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
    response = client.post(
        "/users",
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
    if response.status_code != 400:
        raise AssertionError

    data = response.get_json()
    if "test_user@mail.com is already registered" not in data["message"]:
        raise AssertionError


# Test user creation fails due to invalid content-type header
def test_add_user_invalid_header(test_app, test_database):
    client = test_app.test_client()
    response = client.post(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 415:
        raise AssertionError

    data = response.get_json()
    if "define Content-Type header" not in data["message"]:
        raise AssertionError

    response = client.post(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code != 415:
        raise AssertionError

    data = response.get_json()
    if "supported is application/json" not in data["message"]:
        raise AssertionError


# Test fetching user list passes
def test_get_users(test_app, test_database, add_user):
    add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    add_user(
        username="test_user_two",
        email="test_user_two@mail.com",
        password="test_password_two",
    )

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_user_one@mail.com",
                "password": "test_password_one",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    access_token = data["access_token"]

    client = test_app.test_client()
    response = client.get(
        "/users",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )

    if response.status_code != 200:
        raise AssertionError

    data = response.get_json()

    if len(data) != 2:
        raise AssertionError
    if "test_user_one" not in data[0]["username"]:
        raise AssertionError
    if "test_user_one@mail.com" not in data[0]["email"]:
        raise AssertionError
    if "password" in data[0]:
        raise AssertionError

    if "test_user_two" not in data[1]["username"]:
        raise AssertionError
    if "test_user_two@mail.com" not in data[1]["email"]:
        raise AssertionError
    if "password" in data[1]:
        raise AssertionError


# Test fetching user list fails due to missing token
def test_get_users_missing_token(test_app, test_database, add_user):
    add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    add_user(
        username="test_user_two",
        email="test_user_two@mail.com",
        password="test_password_two",
    )

    client = test_app.test_client()

    response = client.get("/users", headers={"Accept": "application/json"})
    if response.status_code != 403:
        raise AssertionError

    data = response.get_json()
    if "Token required" not in data["message"]:
        raise AssertionError


# Test fetching user list fails due to expired token
def test_get_users_expired_token(test_app, test_database, add_user):
    add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    add_user(
        username="test_user_two",
        email="test_user_two@mail.com",
        password="test_password_two",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_user_one@mail.com",
                "password": "test_password_one",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    access_token = data["access_token"]

    response = client.get(
        "/users",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    if response.status_code != 401:
        raise AssertionError

    data = response.get_json()
    if "Token expired" not in data["message"]:
        raise AssertionError


# Test fetching user list fails due to invalid token
def test_get_users_invalid_token(test_app, test_database, add_user):
    add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )
    add_user(
        username="test_user_two",
        email="test_user_two@mail.com",
        password="test_password_two",
    )

    client = test_app.test_client()

    response = client.get(
        "/users",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer invalid_token",
        },
    )
    if response.status_code != 401:
        raise AssertionError

    data = response.get_json()
    if "Invalid token" not in data["message"]:
        raise AssertionError


# Test fetching single user passes
def test_single_user(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")
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
    data = response.get_json()
    access_token = data["access_token"]

    response = client.get(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    if response.status_code != 200:
        raise AssertionError

    data = response.get_json()
    if data["id"] != user.id:
        raise AssertionError
    if data["username"] != "test_user":
        raise AssertionError
    if data["email"] != "test_user@mail.com":
        raise AssertionError
    if "password" in data.keys():
        raise AssertionError


# Test fetching single user fails due to incorrect id
def test_single_user_invalid_id(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.post(
        "/auth/login",
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
    data = response.get_json()
    access_token = data["access_token"]

    response = client.get(
        "/users/2",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    if response.status_code != 404:
        raise AssertionError

    data = response.get_json()
    if "does not exist" not in data["message"]:
        raise AssertionError


# Test fetching single user fails due to missing token
def test_single_user_missing_token(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.get(
        f"/users/{user.id}", headers={"Accept": "application/json"}
    )

    if response.status_code != 403:
        raise AssertionError

    data = response.get_json()
    if "Token required" not in data["message"]:
        raise AssertionError


# Test fetching single user fails due to expired token
def test_single_user_expired_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_user_one@mail.com",
                "password": "test_password_one",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    access_token = data["access_token"]

    response = client.get(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    if response.status_code != 401:
        raise AssertionError

    data = response.get_json()
    if "Token expired" not in data["message"]:
        raise AssertionError


# Test fetching single user fails due to invalid token
def test_single_user_invalid_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    client = test_app.test_client()

    response = client.get(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer invalid_token",
        },
    )
    if response.status_code != 401:
        raise AssertionError

    data = response.get_json()
    if "Invalid token" not in data["message"]:
        raise AssertionError


# Test removing a user passes
def test_remove_user(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.post(
        "/auth/login",
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
    data = response.get_json()
    access_token = data["access_token"]

    response = client.delete(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    if response.status_code != 204:
        raise AssertionError


# Test removing a user fails due to invalid id
def test_remove_user_invalid_id(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.post(
        "/auth/login",
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
    data = response.get_json()
    access_token = data["access_token"]

    response = client.delete(
        "/users/2",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    if response.status_code != 404:
        raise AssertionError

    data = response.get_json()
    if "does not exist" not in data["message"]:
        raise AssertionError


# Test removing a user fails due to missing token
def test_remove_user_missing_token(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.delete(
        f"/users/{user.id}", headers={"Accept": "application/json"}
    )

    if response.status_code != 403:
        raise AssertionError

    data = response.get_json()
    if "Token required" not in data["message"]:
        raise AssertionError


# Test removing a user fails due to expired token
def test_remove_user_expired_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_user_one@mail.com",
                "password": "test_password_one",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    access_token = data["access_token"]

    response = client.delete(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    if response.status_code != 401:
        raise AssertionError

    data = response.get_json()
    if "Token expired" not in data["message"]:
        raise AssertionError


# Test removing a user fails due to invalid token
def test_remove_user_invalid_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    client = test_app.test_client()

    response = client.delete(
        f"/users/{user.id}",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer invalid_token",
        },
    )
    if response.status_code != 401:
        raise AssertionError

    data = response.get_json()
    if "Invalid token" not in data["message"]:
        raise AssertionError


# Test update a user passes
def test_update_user(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
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
    data = response.get_json()
    access_token = data["access_token"]

    response = client.put(
        f"/users/{user.id}",
        data=json.dumps(
            {
                "username": "test_user_update",
                "email": "test_user_update@mail.com",
            }
        ),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )

    if response.status_code != 200:
        raise AssertionError

    data = response.get_json()
    if data["id"] != 1:
        raise AssertionError(data)
    if data["username"] != "test_user_update":
        raise AssertionError
    if data["email"] != "test_user_update@mail.com":
        raise AssertionError


# Test update a user fails due to empty data
def test_update_user_empty_data(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")

    client = test_app.test_client()

    response = client.put(
        f"/users/{user.id}",
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


# Test update a user fails due to invalid id
def test_update_user_invalid_id(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
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
    data = response.get_json()
    access_token = data["access_token"]

    response = client.put(
        "/users/10",
        data=json.dumps(
            {
                "username": "test_user_update",
                "email": "test_user_update@mail.com",
            }
        ),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )

    if response.status_code != 404:
        raise AssertionError

    data = response.get_json()
    if "does not exist" not in data["message"]:
        raise AssertionError


# Test update a user fails due to invalid headers
def test_update_user_invalid_headers(test_app, test_database, add_user):
    add_user("test_user", "test_user@mail.com", "test_password")

    client = test_app.test_client()
    response = client.put(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Accept": "application/json"},
    )
    if response.status_code != 415:
        raise AssertionError

    data = response.get_json()
    if "define Content-Type header" not in data["message"]:
        raise AssertionError

    response = client.post(
        "/users",
        data=json.dumps({"email": "test_user@email.com"}),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code != 415:
        raise AssertionError

    data = response.get_json()
    if "supported is application/json" not in data["message"]:
        raise AssertionError


# Test update a user fails due to missing token
def test_update_user_missing_token(test_app, test_database, add_user):
    user = add_user("test_user", "test_user@mail.com", "test_password")
    client = test_app.test_client()

    response = client.put(
        f"/users/{user.id}",
        data=json.dumps(
            {
                "username": "test_user_update",
                "email": "test_user_update@mail.com",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    if response.status_code != 403:
        raise AssertionError

    data = response.get_json()
    if "Token required" not in data["message"]:
        raise AssertionError


# Test update a user fails due to expired token
def test_update_user_expired_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    test_app.config["ACCESS_TOKEN_EXPIRATION"] = -1

    client = test_app.test_client()

    response = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_user_one@mail.com",
                "password": "test_password_one",
            }
        ),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    data = response.get_json()
    access_token = data["access_token"]

    response = client.put(
        f"/users/{user.id}",
        data=json.dumps(
            {
                "username": "test_user_update",
                "email": "test_user_update@mail.com",
            }
        ),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 401:
        raise AssertionError

    data = response.get_json()
    if "Token expired" not in data["message"]:
        raise AssertionError


# Test update a user fails due to invalid token
def test_update_user_invalid_token(test_app, test_database, add_user):
    user = add_user(
        username="test_user_one",
        email="test_user_one@mail.com",
        password="test_password_one",
    )

    client = test_app.test_client()

    response = client.put(
        f"/users/{user.id}",
        data=json.dumps(
            {
                "username": "test_user_update",
                "email": "test_user_update@mail.com",
            }
        ),
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer invalid_token",
            "Content-Type": "application/json",
        },
    )
    if response.status_code != 401:
        raise AssertionError

    data = response.get_json()
    if "Invalid token" not in data["message"]:
        raise AssertionError
