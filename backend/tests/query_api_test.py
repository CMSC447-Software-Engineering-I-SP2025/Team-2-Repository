from server import app as flask_app
from flask import json
from backend.tests.utils.spoonacular_mock import mock_raw_spoonacular_recipe


# ==================================================================================================================================
# Tests for /recipes endpoint
# ==================================================================================================================================

# Tests that get recipes work
def test_get_recipes_success(client, mocker):
    # Wrap our mock response in a mock object to simulate a result
    mock_response = mocker.Mock()
    mock_response.text = json.dumps(mock_raw_spoonacular_recipe)

    mock_reqget = mocker.patch('server.reqget')
    mock_reqget.return_value = mock_response

    # Intercepts spoonacular call with mock call
    response = client.get("/recipes", query_string={"includeIngredients": "potatoes"})

    # Verifying what was returned matches expected response
    assert response.status_code == 200

    data = response.get_json()[0]
    assert data["title"] == "Curry Leaves Potato Chips"
    assert data["id"] == 641122
    assert "analyzedInstructions" in data

    assert "usedIngredientCount" in data
    assert "missedIngredientCount" in data
