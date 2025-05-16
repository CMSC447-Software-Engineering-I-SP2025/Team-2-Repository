import pytest, server
import tempfile
import os

from server import app as flask_app
from server import DB, Base
from db_data_models import UserDB
from werkzeug.security import generate_password_hash
from pathlib import Path
from backend.tests.utils.globals import username, password


@pytest.fixture
def test_db(monkeypatch):
    # Create a temp file and close it
    db_fd, raw_path = tempfile.mkstemp()
    os.close(db_fd)

    # Convert to proper URI
    db_path = Path(raw_path).as_posix()
    db_uri = f"sqlite:///{db_path}"
    test_db = DB(db_uri)

    # Replace real DB instance
    server.db = test_db

    yield test_db

    # Cleanup: wipe all data within table (not schema)
    session = test_db.DBSession()

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()

    try:
        os.unlink(db_path)
    except PermissionError:
        pass

@pytest.fixture
def test_user(test_db):
    """Insert a test user into the temporary database"""
    session = test_db.DBSession()

    user = UserDB(
        username=username,
        password_hash=generate_password_hash(password)
    )

    session.add(user)
    session.commit()

    # Save .id before closing
    user_id = user.id
    session.expunge(user)
    session.close()

    # Copy over and return
    user.id = user_id
    return user


@pytest.fixture
def app():
    flask_app.config.update({"TESTING": True})
    with flask_app.app_context():
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()