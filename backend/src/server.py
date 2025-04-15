# External Libraries
from flask import Flask, request
from flask_cors import CORS
from data_classes import Recipe

# Custom Imports
import client

# Configure globals
app = Flask(__name__)
client = client.Client()

# Configure allowed methods
CORS(app, resources={
    r"/recipes*": {
        "origins": "http://localhost:5173",
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    },

    r"/saverecipe*": {
        "origins": "http://localhost:5173",
        "methods": ["PUT"],
        "allow_headers": ["Content-Type"]
    },

    r"/deleterecipe*": {
        "origins": "http://localhost:5173",
        "methods": ["DELETE"],
        "allow_headers": ["Content-Type"]
    },

    r"/listrecipes*": {
    "origins": "http://localhost:5173",
    "methods": ["GET"],
    "allow_headers": ["Content-Type"]
    },

    r"/addingredient*": {
    "origins": "http://localhost:5173",
    "methods": ["PUT"],
    "allow_headers": ["Content-Type"]
    },

    r"/removeingredient*": {
    "origins": "http://localhost:5173",
    "methods": ["DELETE"],
    "allow_headers": ["Content-Type"]
    },

    r"/listingredients*": {
    "origins": "http://localhost:5173",
    "methods": ["GET"],
    "allow_headers": ["Content-Type"]
    },
})


# Define Routes
@app.route('/recipes', methods=['GET'])
def get_recipes():

    # Get query parameters
    include_ingredients: str = request.args.get('includeIngredients', type=str)
    exclude_ingredients: str = request.args.get('excludeIngredients', default='', type=str)
    cuisine: str = request.args.get('cuisine', default='', type=str)
    intolerances: str = request.args.get('intolerances', default='', type=str)
    diet: str = request.args.get('diet', default='', type=str)

    return client.get_recipes(
        include_ingredients=include_ingredients,
        exclude_ingredients=exclude_ingredients,
        cuisine=cuisine,
        intolerances=intolerances,
        diet=diet,
    )


@app.route('/saverecipe', methods=['PUT'])
def save_recipe():
    return client.save_recipe(request.get_json())


@app.route('/deleterecipe', methods=['DELETE'])
def delete_recipe():
    return client.delete_recipe(recipe_id=request.get_data(as_text=True))


@app.route('/listrecipes', methods=['GET'])
def list_recipes() -> list[Recipe]:
    return client.list_recipes()


@app.route('/addingredient', methods=['PUT'])
def add_ingredient():
    return client.add_ingredient(request.get_json())


@app.route('/removeingredient', methods=['DELETE'])
def delete_ingredient():
    return client.remove_ingredient(ingredient_id=request.get_data(as_text=True))

@app.route('/listingredients', methods=['GET'])
def list_ingredients():
    return client.list_ingredients()


# Run the App
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
