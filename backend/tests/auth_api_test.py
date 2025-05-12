from db_data_models import UserDB


# ==================================================================================================================================
# Tests for /register endpoint
# ==================================================================================================================================


# Tests registering in a successful scenario
def test_register_success(client, test_db):
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

# Tests registering when username already exists
def test_register_duplicate_username(client, test_db):
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

# Tests registering when no password supplied
def test_register_no_password(client, test_db):
    response = client.post("/register", json={
        "username": "newuser",
    })

    assert response.status_code == 400
    assert response.get_json().get("error") == "Username and password required"


# ==================================================================================================================================
# Tests for /login endpoint
# ==================================================================================================================================

# ==================================================================================================================================
# Tests for /logout endpoint
# ==================================================================================================================================

# ==================================================================================================================================
# Tests for /loginstatus endpoint
# ==================================================================================================================================

# ==================================================================================================================================
# Tests for /my-account endpoint
# ==================================================================================================================================
