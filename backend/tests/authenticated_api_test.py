import pytest

from db_data_models import UserDB, RecipeDB
from .spoonacular_mock import mock_spoonacular_response
from backend.tests.globals import username, password

# Need to format for methods to accept it
formatted_response = mock_spoonacular_response["results"][0]

# Logs into database
def login(client):
    return client.post("/login", json={"username": username, "password": password})



# ==================================================================================================================================
# Tests for /addrecipe endpoint
# ==================================================================================================================================

def test_save_recipe_success(client, test_user, test_db):
    """Should return 200 and persist recipe when user is authenticated"""

    login(client)
    response = client.put("/addrecipe", json=formatted_response)

    assert response.status_code == 200

    # Ensure added to DB
    session = test_db.DBSession()
    saved = session.query(RecipeDB).filter_by(user_id=test_user.id).first()

    assert saved is not None
    assert saved.title == formatted_response["title"]
    session.close()



# ==================================================================================================================================
# Tests for /removerecipe endpoint
# ==================================================================================================================================

# ==================================================================================================================================
# Tests for /listrecipes endpoint
# ==================================================================================================================================

# ==================================================================================================================================
# Tests for /addingredient endpoint
# ==================================================================================================================================

# ==================================================================================================================================
# Tests for /removeingredient endpoint
# ==================================================================================================================================

# ==================================================================================================================================
# Tests for /listingredients endpoint
# ==================================================================================================================================
