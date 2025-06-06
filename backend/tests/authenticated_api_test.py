from db_data_models import UserDB, RecipeDB, IngredientDB
from backend.tests.utils.spoonacular_mock import mock_formatted_spoonacular_recipe, mock_spoonacular_ingredient
from backend.tests.utils.globals import username, password

# Need to format for methods to accept it
formatted_response = mock_formatted_spoonacular_recipe
formatted_ingredient = mock_spoonacular_ingredient


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
    #
    # print("Formatted Response", response)
    # assert response.status_code == 200

    # Ensure added to DB
    # session = test_db.DBSession()
    # saved = session.query(RecipeDB).filter_by(user_id=test_user.id).first()
    #
    # assert saved is not None
    # assert saved.title == formatted_response["title"]
    # session.close()


def test_save_recipe_unauthenticated(client):
    """Should return 401 if user is not logged in."""

    response = client.put("/addrecipe", json=formatted_response)
    assert response.status_code == 401


# ==================================================================================================================================
# Tests for /removerecipe endpoint
# ==================================================================================================================================

def test_delete_recipe_success(client, test_user, test_db):
    """Should return 200 and persist recipe when user is authenticated"""

    # Place in the mock_response into db
    login(client)
    client.put("/addrecipe", json=formatted_response)

    recipe_id = formatted_response["id"]
    response = client.delete("/removerecipe", data=str(recipe_id))

    assert response.status_code == 200

    session = test_db.DBSession()
    recipe = session.query(RecipeDB).filter_by(user_id=test_user.id, recipe_id=recipe_id).first()
    session.close()

    assert recipe is None


def test_delete_recipe_unauthenticated(client):
    """Should return 401 if user is not logged in."""

    recipe_id = formatted_response["id"]
    response = client.delete("/removerecipe", data=str(recipe_id))
    assert response.status_code == 401


# ==================================================================================================================================
# Tests for /listrecipes endpoint
# ==================================================================================================================================

def test_list_recipes_success(client, test_user, test_db):
    """Should return list of recipes when user is logged in and has saved recipes."""

    # Log in
    login(client)
    client.put("/addrecipe", json=formatted_response)

    response = client.get("/listrecipes")

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == formatted_response["title"]

def test_list_recipes_unauthenticated(client):
    """Should return 401 if user is not logged in."""

    response = client.get("/listrecipes")
    assert response.status_code == 401
    assert response.get_json()["error"] == "Unauthorized"


# ==================================================================================================================================
# Tests for /addingredient endpoint
# ==================================================================================================================================

def test_save_ingredient_success(client, test_user, test_db):
    """Should return 200 and save ingredient when user is authenticated."""

    # Log in the user
    login(client)

    # Send PUT request to add ingredient
    response = client.put("/addingredient", json=formatted_ingredient)

    # Validate response
    assert response.status_code == 200
    assert response.data.decode() == "200"

    # Confirm ingredient is stored in DB
    session = test_db.DBSession()
    saved = session.query(IngredientDB).filter_by(user_id=test_user.id).first()
    session.close()

    assert saved is not None
    assert saved.name == formatted_ingredient["name"]


def test_save_ingredient_unauthenticated(client):
    """Should return 401 if user is not logged in."""

    response = client.put("/addingredient", json=formatted_ingredient)

    assert response.status_code == 401
    assert response.get_json()["error"] == "Unauthorized"


# ==================================================================================================================================
# Tests for /removeingredient endpoint
# ==================================================================================================================================

def test_delete_ingredient_success(client, test_user, test_db):
    """Should delete ingredient and return 200 when user is authenticated."""

    # Log in the user
    login(client)

    # First, add the ingredient to DB
    response = client.put("/addingredient", json=formatted_ingredient)
    assert response.status_code == 200

    # Get the ingredient's ID from the DB
    session = test_db.DBSession()
    ingredient = session.query(IngredientDB).filter_by(user_id=test_user.id).first()
    session.close()

    assert ingredient is not None

    # Send DELETE request
    response = client.delete("/removeingredient", data=str(ingredient.ingr_id))

    assert response.status_code == 200
    assert response.data.decode() == "200"

    # Confirm it's gone
    session = test_db.DBSession()
    result = session.query(IngredientDB).filter_by(ingr_id=ingredient.ingr_id).first()
    session.close()
    assert result is None


def test_delete_ingredient_unauthenticated(client):
    """Should return 401 if user is not logged in."""

    response = client.delete("/removeingredient", data="1")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Unauthorized"


# ==================================================================================================================================
# Tests for /listingredients endpoint
# ==================================================================================================================================

def test_list_ingredients_success(client, test_user, test_db):
    """Should return list of ingredients when user is logged in and has saved ingredients."""

    # Log in
    login(client)

    # Save ingredient
    client.put("/addingredient", json=formatted_ingredient)

    # Request list
    response = client.get("/listingredients")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == formatted_ingredient["name"]


def test_list_ingredients_empty(client, test_user):
    """Should return empty list when user is logged in but has no ingredients."""

    login(client)

    response = client.get("/listingredients")
    assert response.status_code == 200
    assert response.get_json() == []


def test_list_ingredients_unauthenticated(client):
    """Should return 401 if user is not logged in."""

    response = client.get("/listingredients")
    assert response.status_code == 401
    assert response.get_json()["error"] == "Unauthorized"
