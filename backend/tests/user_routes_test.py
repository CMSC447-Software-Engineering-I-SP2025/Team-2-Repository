from db_data_models import UserDB
import pytest


# ==================================================================================================================================
# Tests for /register endpoint
# ==================================================================================================================================

def test_register_success(client, test_db):
    """Should return 201 and store user when registration is successful."""

    response = client.post("/register", json={
        "username": "newuser",
        "password": "password123",
    })

    assert response.status_code == 201
    assert response.get_json().get("message") == "User registered successfully"

    # Ensure user was stored in database
    session = test_db.DBSession()
    user = session.query(UserDB).filter_by(username="newuser").first()
    assert user is not None
    session.close()

def test_register_duplicate_username(client, test_db):
    """Should return 409 and print an error if username already exists."""

    client.post("/register", json={
        "username": "newuser",
        "password": "password123",
    })

    response = client.post("/register", json={
        "username": "newuser",
        "password": "password123",
    })

    assert response.status_code == 409
    assert response.get_json().get("error") == "Username already exists"

    # Ensure a second user was not stored in Database
    session = test_db.DBSession()
    users = session.query(UserDB).filter_by(username="newuser").all()
    assert len(users) == 1
    session.close()

@pytest.mark.parametrize("username, password, desc", [
    ("", "somepass", "no_username"),         # missing username
    ("newuser", "", "no_password"),          # missing password
    (None, "somepass", "null_username"),       # None username
    ("newuser", None, "null_password"),        # None password
    ("", "", "no_both"),                        # missing both
    (None, None, "null_both")                  # None both
])
def test_register_missing_credentials(client, test_db, username, password, desc):
    """Should return 400 and print an error if required fields are missing."""

    response = client.post("/register", json={
        "username": username,
        "password": password,
    })

    assert response.status_code == 400, f"Failed on: {desc}"
    assert response.get_json().get("error") == "Username and password required"

    session = test_db.DBSession()
    user = session.query(UserDB).filter_by(username=username).first()
    assert user is None
    session.close()


# ==================================================================================================================================
# Tests for /login endpoint
# ==================================================================================================================================

def test_login_success(client, test_db):
    """Should return 200 and allow user to login when successful."""

    client.post("/register", json={
        "username": "newuser",
        "password": "password123",
    })

    response = client.post("/login", json={
        "username": "newuser",
        "password": "password123",
    })

    assert response.status_code == 200
    assert response.data.decode() == "newuser" #Ensure username is correctly returned

    # Ensure session variables were set
    with client.session_transaction() as session:
        assert session.get("user_id") is not None
        assert session.get("username") == "newuser"


@pytest.mark.parametrize("username, password, desc", [
    ("nonexistent", "somepass", "invalid username"),
    ("validuser", "wrongpass", "invalid password")
])
def test_login_invalid_credentials(client, test_db, username, password, desc):
    """Should return 401 and not set session for invalid credentials

        Injects cases via parameterize
    """

    client.post("/register", json={
        "username": "validuser",
        "password": "correctpass"
    })

    response = client.post("/login", json={
        "username": username,
        "password": password
    })

    assert response.status_code == 401, f"Failed on: {desc}"
    assert response.get_json()["error"] == "Invalid credentials"

    with client.session_transaction() as sess:
        assert "user_id" not in sess


@pytest.mark.parametrize("username, password, desc", [
    ("", "somepass", "no_username"),             # missing username
    ("validuser", "", "no_password"),            # missing password
    (None, "somepass", "null_username"),           # None username
    ("validuser", None, "null_password"),          # None password
    ("", "", "no_both"),                     # both empty
    (None, None, "null_both"),                 # both None
])
def test_login_missing_credentials(client, test_db, username, password, desc):
    """Should return 400 and error when username or password is missing."""

    response = client.post("/login", json={
        "username": username,
        "password": password
    })

    assert response.status_code == 400, f"Failed on: {desc}"
    assert response.get_json()["error"] == "Username and password required"

    with client.session_transaction() as sess:
        assert "user_id" not in sess

# ==================================================================================================================================
# Tests for /logout endpoint
# ==================================================================================================================================

def test_logout_success(client, test_user):
    """Should return 200 and return successful logout message"""


    # Manually log in the test user (simulate session-based login)
    with client.session_transaction() as sess:
        sess["user_id"] = test_user.id
        sess["username"] = test_user.username

    # Call logout
    response = client.get("/logout")

    assert response.status_code == 200
    assert response.get_json()["message"] in "Logged out successfully"

    # Session should now be cleared
    with client.session_transaction() as sess:
        assert "user_id" not in sess
        assert "username" not in sess

# ==================================================================================================================================
# Tests for /loginstatus endpoint
# ==================================================================================================================================

def test_loginstatus_logged_in(client, test_user):
    """Returns 200 and username when logged in"""

    with client.session_transaction() as sess:
        sess["user_id"] = test_user.id
        sess["username"] = test_user.username

    response = client.get("/loginstatus")

    assert response.status_code == 200
    assert response.data.decode() == test_user.username


def test_loginstatus_logged_out(client):
    """Returns 200 and empty string when user not logged in"""

    response = client.get("/loginstatus")

    assert response.status_code == 200
    assert response.data.decode() == ""


# ==================================================================================================================================
# Tests for /my-account endpoint
# ==================================================================================================================================
def test_my_account_logged_in(client, test_user):
    """Should return 200 and show account info when logged in."""

    with client.session_transaction() as sess:
        sess["user_id"] = test_user.id
        sess["username"] = test_user.username

    response = client.get("/my-account")

    assert response.status_code == 200
    assert f"Logged in as: <strong>{test_user.username}</strong>" in response.data.decode()


def test_my_account_not_logged_in(client):
    """Should return 401 and login prompt when not logged in."""

    response = client.get("/my-account")

    assert response.status_code == 401
    assert "You are not logged in" in response.data.decode()
    assert "Login here" in response.data.decode()

