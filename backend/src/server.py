"""Main file for this project."""
# ==================================================================================================================================
# IMPORTS
# ==================================================================================================================================


# Standard Libraries
from __future__ import annotations
import json
from pathlib import Path
from typing import Any  #TODO remove if not needed

# Custom Libraries
from backend_data_models import Response
from db_data_models import (
    Base,
    IngredientDB,
    RecipeDB,
    UserDB,
)

# External Libraries
from flask import Flask, jsonify, render_template_string, request, session
from flask_cors import CORS
from mappers import ingredient_mapper, recipe_mapper, response_mapper
from requests import Request
from requests import get as reqget
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tomllib import loads as tomlloads
from werkzeug.security import check_password_hash, generate_password_hash

# ==================================================================================================================================
# GLOBAL ITEMS
# ==================================================================================================================================


# Load config file
config_options = tomlloads((Path(__file__).parent.parent / "assets" / "config.toml").read_text())

# Database connection
class DB:
    """Database connector."""

    def __init__(self, db_uri=None) -> None:
        """Initialize the database."""
        if db_uri is None:
            db_path = Path(__file__).resolve().parent.parent / 'assets' / 'database.db'
            db_uri = f"sqlite:///{db_path.as_posix()}"

        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)
        self.base_url = "https://api.spoonacular.com/recipes/complexSearch"
        self.api_key = config_options["apikey"]

# Initialize DB and Flask app
db = DB()
app = Flask(__name__)
app.secret_key = config_options["secret_key"]


def get_dummy_data() -> dict:
    """Get dummy data for testing.

    Returns:
        dict: Dummy data.

    """
    with Path.open(Path(__file__).parent.parent / "assets" / "cached.json") as f:
        return json.load(f, strict=False)

# CORS security parameters
CORS(app, resources={
    r"/recipes*": {
        "origins": "http://localhost:5173",
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"],
    },
    r"/addrecipe*": {
        "origins": "http://localhost:5173",
        "methods": ["PUT"],
        "allow_headers": ["Content-Type"],
    },
    r"/removerecipe*": {
        "origins": "http://localhost:5173",
        "methods": ["DELETE"],
        "allow_headers": ["Content-Type"],
    },
    r"/listrecipes*": {
        "origins": "http://localhost:5173",
        "methods": ["GET"],
        "allow_headers": ["Content-Type"],
    },
    r"/addingredient*": {
        "origins": "http://localhost:5173",
        "methods": ["PUT"],
        "allow_headers": ["Content-Type"],
    },
    r"/removeingredient*": {
        "origins": "http://localhost:5173",
        "methods": ["DELETE"],
        "allow_headers": ["Content-Type"],
    },
    r"/listingredients*": {
        "origins": "http://localhost:5173",
        "methods": ["GET"],
        "allow_headers": ["Content-Type"],
    },
    r"/register*": {
        "origins": "http://localhost:5173",
        "methods": ["POST", "GET"],
        "allow_headers": ["Content-Type"],
    },
    r"/login*": {
        "origins": "http://localhost:5173",
        "methods": ["POST", "GET"],
        "allow_headers": ["Content-Type"],
    },
    r"/logout*": {
    "origins": "http://localhost:5173",
    "methods": ["POST"],
    "allow_headers": ["Content-Type"],
    },
    r"/loginstatus*": {
        "origins": "http://localhost:5173",
        "methods": ["GET"],
        "allow_headers": ["Content-Type"],
    },
},
supports_credentials=True,
)

# ==================================================================================================================================
# CORE BUSINESS LOGIC
# ==================================================================================================================================


@app.route(rule="/register", methods=["POST"])
def register() -> str | tuple[Response, int]:
    """Register a user.

    Returns:
        dict: Response.

    """

    # POST: handle registration
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    with db.DBSession() as session_db:
        if session_db.query(UserDB).filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 409
        user = UserDB(
            username=username,
            password_hash=generate_password_hash(password),
        )
        session_db.add(user)
        session_db.commit()
    return jsonify({"message": "User registered successfully"}), 201


@app.route(rule="/login", methods=["POST"])
def login() -> str | tuple[Response, int] | tuple[str, int]:
    """Log user in.

    Returns:
        Text: Success message.

    """
    # User is already logged in
    if "user_id" in session:
        return render_template_string("<p>You are already logged in as {{username}}. <a href='http://localhost:5173/'>Go to home</a></p>", username=session.get("username"))

    # POST: handle login
    data = request.form if request.form else request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # Check if login credentials are correct
    with db.DBSession() as session_db:
        user = session_db.query(UserDB).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return user.username, 200
        return jsonify({"error": "Invalid credentials"}), 401


@app.route(rule="/logout", methods=["POST", "GET"])
def logout() -> tuple[Response, int]:
    """Log user out.

    Returns:
        tuple: JSON message and status code

    """
    session.pop("user_id", None)
    session.pop("username", None)
    return jsonify({"message": "Logged out successfully"}), 200


@app.route(rule="/loginstatus", methods=["GET"])
def loginstatus() -> tuple[Any | None, int] | tuple[str, int]:
    """Return username if user is logged in else empty string.

    Returns:
        str | None: username or none

    """
    if session.get("username") :
        return (session.get("username"), 200)
    return ("", 200)


@app.route(rule="/my-account")
def my_account() -> tuple[str, int] | str:
    """View account info.

    Returns:
        Text: Account info or error message.

    """
    # User is not logged in
    if "username" not in session:
        return "<p>You are not logged in. <a href='/login'>Login here</a></p>", 401

    # User is logged in
    username = session["username"]

    # We may fetch more user info here.

    return render_template_string(f"""
        <h2>My Account</h2>
        <p>Logged in as: <strong>{username}</strong></p>
        <p><a href='/logout'>Logout</a></p>
    """)


@app.route("/recipes", methods=["GET"])
def api_get_recipes() -> dict:
    """Search for recipes from Spoonacular.

    Returns:
        dict: Returned recipes.

    """
    # Get data from request
    include_ingredients = request.args.get("includeIngredients", type=str)
    cuisine = request.args.get("cuisine", default="", type=str)
    intolerances = request.args.get("intolerances", default="", type=str)
    diet = request.args.get("diet", default="", type=str)

    # Build required params
    params = {
        "includeIngredients": include_ingredients,
        "instructionsRequired": True,
        "addRecipeInformation": True,
        "addRecipeInstructions": True,
        "addRecipeNutrition": True,
        "fillIngredients": True,
        "sort": "min-missing-ingredients",
        "number": 1,
        "apiKey": db.api_key,
    }

    # Build optional params
    if cuisine:
        params["cuisine"] = cuisine
    if intolerances:
        params["intolerances"] = intolerances
    if diet:
        params["diet"] = diet

    # Get dummy data
    #final_results = response_mapper(get_dummy_data(), Response).results

    # Request, get, and return data (Expanded)
    url = Request(method="GET", url=db.base_url, params=params).prepare().url
    spoonacular_response = reqget(url, timeout=5).text
    json_data = json.loads(spoonacular_response)
    mapped_data = response_mapper(json_data).results
    return mapped_data

    # Request, get, and return data (One liner).
    # return response_mapper(json_data=json.loads(reqget(url=Request(method="GET", url=db.base_url, params=params).prepare().url,timeout=5).text)).results


@app.route("/addrecipe", methods=["PUT"])
def api_save_recipe() -> tuple[Response, int] | str:
    """Save a recipe to the database.

    Raises:
        e: MySQL error.

    Returns:
        str: Success message.

    """
    recipe_data = request.get_json()
    user_id  = session.get("user_id")

    # If null user_id
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Write data to database
    with db.DBSession() as db_session:
        try:
            recipe_db_class = recipe_mapper(recipe_data)
            recipe_db_class.user_id = user_id
            db_session.add(recipe_db_class)
            db_session.commit()

        except Exception as e:
            db_session.rollback()
            raise e
    return "200"


@app.route("/removerecipe", methods=["DELETE"])
def api_delete_recipe() -> tuple[Response, int] | str:
    """Delete a recipe from the database.

    Raises:
        e: MySQL error.

    Returns:
        str: Success message.

    """
    user_id  = session.get("user_id")
    recipe_id = int(request.get_data(as_text=True))

    # If null user_id
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Delete specified recipe
    with db.DBSession() as db_session:
        try:
            db_session.query(RecipeDB).filter_by(recipe_id=recipe_id, user_id=user_id).delete()
            db_session.commit()

        # Handle errors
        except Exception as e:
            db_session.rollback()
            raise e
    return "200"


@app.route("/listrecipes", methods=["GET"])
def api_list_recipes() -> Response | tuple[Response, int]:
    """List all saved recipes.

    Raises:
        e: MySQL error.

    Returns:
        dict: List of saved recipes.

    """
    user_id  = session.get("user_id")

    # If null user_id
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Query database for recipes.
    with db.DBSession() as db_session:
        try:
            recipes = [recipe_mapper(recipe) for recipe in db_session.query(RecipeDB).filter(RecipeDB.user_id == user_id).all()]
            return jsonify(recipes)
        except Exception as e:
            db_session.rollback()
            raise e


@app.route("/addingredient", methods=["PUT"])
def api_save_ingredient() -> tuple[Response, int] | str:
    """Add an ingredient to the pantry.

    Raises:
        e: MySQL error.

    Returns:
        str: Success message.

    """
    user_id  = session.get("user_id")

    # If null user_id
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Write data to database
    with db.DBSession() as db_session:
        try:
            ingredient_db_class = ingredient_mapper(request.get_json())
            ingredient_db_class.user_id = user_id

            existingRecord = db_session.query(IngredientDB).filter_by(ingr_id=ingredient_db_class.ingr_id, user_id=user_id)
            if (existingRecord):
                existingRecord.delete()
                
            db_session.add(ingredient_db_class)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
    return "200"


@app.route("/removeingredient", methods=["DELETE"])
def api_delete_ingredient() -> tuple[Response, int] | str:
    """Remove an ingredient from the pantry.

    Raises:
        e: MySQL error.

    Returns:
        str: Success message.

    """
    # Write data to database
    user_id  = session.get("user_id")
    ingredient_id = int(request.get_data(as_text=True))

    # If null user_id
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    with db.DBSession() as db_session:
        try:
            db_session.query(IngredientDB).filter_by(ingr_id=ingredient_id, user_id=user_id).delete()
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
    return "200"


@app.route("/listingredients", methods=["GET"])
def api_list_ingredients() -> Response | tuple[Response, int]:
    """List all saved ingredients.

    Raises:
        e: MySQL error.

    Returns:
        dict: List of saved ingredients.

    """
    user_id  = session.get("user_id")

    # If null user_id
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    with db.DBSession() as db_session:
        try:
            ingredients = db_session.query(IngredientDB).filter(IngredientDB.user_id == user_id).all()
            return jsonify([ingredient_mapper(ingr) for ingr in ingredients])

        except Exception as e:
            db_session.rollback()
            raise e


@app.route("/findmissing", methods=["GET"])
def find_missing_ingredients() -> list[str]:
    """Find all ingredients missing from a specified recipe.

    Returns:
        list[str]: List of missing ingredients.

    """
    # recipe = recipe_mapper(
    #     input_recipe={
    #         "id": 1956640,
    #         "image": 'https://img.spoonacular.com/recipes/1956640-312x231.jpg',
    #         "title": 'Margarita',
    #         "servings": 1,
    #         "ingredients": [
    #             Ingredient(id=1019159, name='lime slice', quantity=None, unit=None, image='lime-wedge.jpg'),
    #             Ingredient(id=0, name='cocktail', quantity=None, unit=None, image='rum-dark.jpg'),
    #             Ingredient(id=0, name='shake', quantity=None, unit=None, image=''),
    #             Ingredient(id=2047, name='salt', quantity=None, unit=None, image='salt.jpg'),
    #             Ingredient(id=10014412, name='ice', quantity=None, unit=None, image='ice-cubes.png'),
    #             Ingredient(id=1012034, name='dry seasoning rub', quantity=None, unit=None, image='seasoning.png')
    #         ],
    #         "nutrition": {}
    #     },
    # )


    # Expecting the frontend to send a RecipeDB object.

    # Get recipe from frontend
    recipe = recipe_mapper(request.get_json())

    # Get recipe ingredients
    recipe_ingredients: list[str] = [ingredient.name for ingredient in recipe.ingredients]

    # Get user ingredients
    user_ingredinets: list[str] = [ingr["name"] for ingr in api_list_ingredients().json]

    # Find / return missing ingredients
    return [ingr for ingr in recipe_ingredients if ingr not in user_ingredinets]


# ==================================================================================================================================
# BEGIN PROGRAM EXECUTION
# ==================================================================================================================================


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
