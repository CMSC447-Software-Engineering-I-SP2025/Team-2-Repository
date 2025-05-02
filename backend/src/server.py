"""Main file for this project."""
# ==================================================================================================================================
# IMPORTS

# Standard Libraries
import json
from pathlib import Path

# Custom Libraries
from data_classes import Response, json_mapper
from db_models import (
    Base,
    IngredientDB,
    RecipeDB,
    UserDB,
    db_to_ingredient,
    db_to_recipe,
    ingredient_to_db,
    recipe_to_db,
)

# External Libraries
from flask import Flask, jsonify, render_template_string, request, session
from flask_cors import CORS
from requests import Request
from requests import get as reqget
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tomllib import loads as tomlloads
from werkzeug.security import check_password_hash, generate_password_hash

# ==================================================================================================================================
# GLOBAL ITEMS
#

# Load config file
config_options = tomlloads((Path(__file__).parent.parent / "assets" / "config.toml").read_text())

# Database connection
class DB:
    """Database connector."""

    def __init__(self) -> None:
        """Initialize the database."""
        self.engine = create_engine(f"sqlite:///{(Path(__file__).resolve().parent.parent / 'assets' / 'database.db').as_posix()}")
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)
        self.base_url = "https://api.spoonacular.com/recipes/complexSearch"
        self.api_key = config_options["apikey"]

# Initialize DB and Flask app
db = DB()
app = Flask(__name__)
app.secret_key = config_options["secret_key"]

# Temp Forms
LOGIN_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="post" action="/login">
        <label>Username:</label><br>
        <input type="text" name="username" required><br>
        <label>Password:</label><br>
        <input type="password" name="password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="/register">Register here</a></p>
</body>
</html>
"""

REGISTER_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
</head>
<body>
    <h2>Register</h2>
    <form id="registerForm">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <button type="submit">Register</button>
    </form>
    <div id="message"></div>
    <script>
        document.getElementById('registerForm').onsubmit = async function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const response = await fetch('/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, password})
            });
            const data = await response.json();
            document.getElementById('message').innerText = data.message || data.error;
        };
    </script>
</body>
</html>
"""

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
    r"/saverecipe*": {
        "origins": "http://localhost:5173",
        "methods": ["PUT"],
        "allow_headers": ["Content-Type"],
    },
    r"/deleterecipe*": {
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
})

# ==================================================================================================================================
# CORE BUSINESS LOGIC

@app.route(rule="/register", methods=["POST", "GET"])
def register() -> dict:
    """Register a user.

    Returns:
        dict: Response.

    """
    if request.method == "GET":
        return render_template_string(REGISTER_FORM)

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


@app.route(rule="/login", methods=["GET", "POST"])
def login() -> str:
    """Log user in.

    Returns:
        Text: Success message.

    """
    # User is already logged in
    if "user_id" in session:
        return render_template_string("<p>You are already logged in as {{username}}. <a href='http://localhost:5173/'>Go to home</a></p>", username=session.get("username"))

    # Return login form
    if request.method == "GET":
        return render_template_string(LOGIN_FORM)

    # POST: handle login
    data = request.form if request.form else request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return render_template_string(LOGIN_FORM + "<p style='color:red;'>Username and password required.</p>"), 400

    # Check if login credentials are correct
    with db.DBSession() as session_db:
        user = session_db.query(UserDB).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return render_template_string("<p>Logged in successfully! <a href='http://localhost:5173/'>Go to home</a></p>")
        return render_template_string(LOGIN_FORM + "<p style='color:red;'>Invalid credentials.</p>"), 401


@app.route(rule="/logout", methods=["POST", "GET"])
def logout() -> str:
    """Log user out.

    Returns:
        Text: Success message.

    """
    session.pop("user_id", None)
    session.pop("username", None)
    return render_template_string("<p>Logged out successfully!</p>")


@app.route(rule="/my-account")
def my_account() -> str:
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
    exclude_ingredients = request.args.get("excludeIngredients", default="", type=str)
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
        "number": 15,
        "apiKey": db.api_key,
    }

    # Build optional params
    if exclude_ingredients:
        params["excludeIngredients"] = exclude_ingredients
    if cuisine:
        params["cuisine"] = cuisine
    if intolerances:
        params["intolerances"] = intolerances
    if diet:
        params["diet"] = diet

    # Dummy data
    #json_mapper(get_dummy_data(), Response).results


    # return  json_mapper(json_data=json.loads(reqget(url=Request(method="GET", url=db.base_url, params=params).prepare().url,timeout=5).text), data_class=Response).results

    # Sequential request
    request_url = Request(method="GET", url=db.base_url, params=params).prepare().url  # Build URL
    raw_response = reqget(url = request_url, timeout=5)  # Get the raw text resonse
    json_response = json.loads(raw_response.text)  # Turn raw text into JSON
    mapped_json_response = json_mapper(json_data=json_response,
                                       data_class=Response)  # Map JSON into a Response object.
    final_results = mapped_json_response.results  # Get results from response object.


    # Make request and return data.
    return final_results

@app.route("/saverecipe", methods=["PUT"])
def api_save_recipe() -> str:
    """Save a recipe to the database.

    Raises:
        e: MySQL error.

    Returns:
        str: Success message.

    """
    # Write data to database
    with db.DBSession() as db_session:
        try:
            recipe_db_class = recipe_to_db(request.get_json())
            recipe_db_class.user_id = session["user_id"]
            db_session.add(recipe_db_class)
            db_session.commit()
        except Exception as e:
            session.rollback()
            raise e
    return "200"


@app.route("/deleterecipe", methods=["DELETE"])
def api_delete_recipe() -> str:
    """Delete a recipe from the database.

    Raises:
        e: MySQL error.

    Returns:
        str: Success message.

    """
    # Query database for recipes.
    with db.DBSession() as db_session:
        try:
            db_session.query(RecipeDB).filter_by(id=int(request.get_data(as_text=True))).delete()
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
    return "200"


@app.route("/listrecipes", methods=["GET"])
def api_list_recipes() -> dict:
    """List all saved recipes.

    Raises:
        e: MySQL error.

    Returns:
        dict: List of saved recipes.

    """
    # Query database for recipes.
    with db.DBSession() as db_session:
        try:
            recipes = [db_to_recipe(recipe) for recipe in db_session.query(RecipeDB).all()]
            return jsonify(recipes)
        except Exception as e:
            db_session.rollback()
            raise e


@app.route("/addingredient", methods=["PUT"])
def api_save_ingredient() -> str:
    """Add an ingredient to the pantry.

    Raises:
        e: MySQL error.

    Returns:
        str: Success message.

    """
    # Write data to database
    with db.DBSession() as db_session:
        try:
            ingredient_db_class = ingredient_to_db(request.get_json())
            db_session.add(ingredient_db_class)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
    return "200"


@app.route("/removeingredient", methods=["DELETE"])
def api_delete_ingredient() -> str:
    """Remove an ingredient from the pantry.

    Raises:
        e: MySQL error.

    Returns:
        str: Success message.

    """
    # Write data to database
    with db.DBSession() as db_session:
        try:
            db_session.query(IngredientDB).filter_by(id=int(request.get_data(as_text=True))).delete()
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
    return "200"


@app.route("/listingredients", methods=["GET"])
def api_list_ingredients() -> dict:
    """List all saved ingredients.

    Raises:
        e: MySQL error.

    Returns:
        dict: List of saved ingredients.

    """
    with db.DBSession() as db_session:
        try:
            return jsonify([db_to_ingredient(ingr) for ingr in db_session.query(IngredientDB).all()])
        except Exception as e:
                db_session.rollback()
                raise e


# ==================================================================================================================================
# BEGIN PROGRAM EXECUTION
#

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
