import pytest
from server import app as flask_app
from flask import Flask, json
from .spoonacular_mock import mock_spoonacular_response



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
