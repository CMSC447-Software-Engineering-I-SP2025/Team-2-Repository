import pytest
from server import app as flask_app
from flask import Flask, json


# Mocks a spoonacular request
mock_spoonacular_response = {
    "results": [
        {
            "id": 659581,
            "title": "Mock Scotch Eggs",
            "image": "https://img.spoonacular.com/recipes/659581-312x231.jpg",
            "servings": 8,
            "usedIngredientCount": 1,
            "missedIngredientCount": 2,
            "analyzedInstructions": [
                {
                    "name": "",
                    "steps": [
                        {
                            "number": 1,
                            "step": "Wrap sausage around egg",
                            "ingredients": [
                                {"id": 1129, "name": "hard boiled egg", "quantity": None, "image": "hard-boiled-egg.png"},
                                {"id": 18079, "name": "breadcrumbs", "quantity": None, "image": "breadcrumbs.jpg"}
                            ],
                            "equipment": [
                                {
                                    "id": 404727,
                                    "name": "baking sheet",
                                    "image": "https://spoonacular.com/cdn/equipment_100x100/baking-sheet.jpg",
                                    "temperature": None
                                }
                            ],
                            "length": {
                                "number": 20,
                                "unit": "minutes"
                            }
                        }
                    ]
                }
            ],
            "nutrition": {
                "nutrients": [
                    {"name": "Calories", "amount": 296.48, "unit": "kcal", "percentOfDailyNeeds": 14.82},
                    {"name": "Protein", "amount": 16.6, "unit": "g", "percentOfDailyNeeds": 33.19},
                    {"name": "Fat", "amount": 20.47, "unit": "g", "percentOfDailyNeeds": 31.48}
                ]
            }
        }
    ]
}

# Logs into database
def login(client):
    return client.post("/login", json={"username": "test", "password": "password"})

# ==================================================================================================================================
# Tests for /recipes endpoint
# ==================================================================================================================================

# Tests that get recipes work
def test_get_recipes_success(client, mocker):
    # Wrap our mock response in a mock object to simulate a result
    mock_response = mocker.Mock()
    mock_response.text = json.dumps(mock_spoonacular_response)

    mock_reqget = mocker.patch('server.reqget')
    mock_reqget.return_value = mock_response

    # Intercepts spoonacular call with mock call
    response = client.get("recipes?includeIngredients=sausage")

    # Verifying what was returned matches expected response
    assert response.status_code == 200

    data = response.get_json()[0]
    assert data["title"] == "Mock Scotch Eggs"
    assert data["id"] == 659581

# ==================================================================================================================================
# Tests for /addrecipe endpoint
# ==================================================================================================================================


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
