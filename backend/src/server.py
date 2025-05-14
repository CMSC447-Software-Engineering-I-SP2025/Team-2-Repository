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
        "number": 1,
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
    #print("Saving Recipe: ", request.get_json())
    #recipe_data = request.get_json()

    recipe_data = \
    {
      "id": 641122,
      "image": "https://img.spoonacular.com/recipes/641122-312x231.jpg",
      "imageType": "jpg",
      "title": "Curry Leaves Potato Chips",
      "readyInMinutes": 45,
      "servings": 3,
      "sourceUrl": "https://www.foodista.com/recipe/S6M8SF2T/curry-leaves-potato-chips",
      "vegetarian": True,
      "vegan": True,
      "glutenFree": True,
      "dairyFree": True,
      "veryHealthy": False,
      "cheap": False,
      "veryPopular": False,
      "sustainable": False,
      "lowFodmap": True,
      "weightWatcherSmartPoints": 5,
      "gaps": "no",
      "preparationMinutes": None,
      "cookingMinutes": None,
      "aggregateLikes": 4,
      "healthScore": 18,
      "creditsText": "Foodista.com – The Cooking Encyclopedia Everyone Can Edit",
      "license": "CC BY 3.0",
      "sourceName": "Foodista",
      "pricePerServing": 54.5,
      "extendedIngredients": [
        {
          "id": 10011355,
          "aisle": "Produce",
          "image": "red-potatoes.jpg",
          "consistency": "SOLID",
          "name": "potatoes - remove skin",
          "nameClean": "potatoes - remove skin",
          "original": "3 potatoes - remove skin, sliced thinly and soaked in ice water for 10-15 minutes.",
          "originalName": "potatoes - remove skin, sliced thinly and soaked in ice water for 10-15 minutes",
          "amount": 3,
          "unit": "",
          "meta": [
            "sliced",
            "for 10-15 minutes."
          ],
          "measures": {
            "us": {
              "amount": 3,
              "unitShort": "",
              "unitLong": ""
            },
            "metric": {
              "amount": 3,
              "unitShort": "",
              "unitLong": ""
            }
          }
        },
        {
          "id": 2009,
          "aisle": "Spices and Seasonings",
          "image": "chili-powder.jpg",
          "consistency": "SOLID",
          "name": "chili powder",
          "nameClean": "chili powder",
          "original": "1 tsp plain chili powder",
          "originalName": "plain chili powder",
          "amount": 1,
          "unit": "tsp",
          "meta": [
            "plain"
          ],
          "measures": {
            "us": {
              "amount": 1,
              "unitShort": "tsp",
              "unitLong": "teaspoon"
            },
            "metric": {
              "amount": 1,
              "unitShort": "tsp",
              "unitLong": "teaspoon"
            }
          }
        },
        {
          "id": 93604,
          "aisle": "Ethnic Foods",
          "image": "curry-leaves.jpg",
          "consistency": "SOLID",
          "name": "curry leaves",
          "nameClean": "curry leaves",
          "original": "3-4 sprigs curry leaves",
          "originalName": "curry leaves",
          "amount": 3,
          "unit": "sprigs",
          "meta": [],
          "measures": {
            "us": {
              "amount": 3,
              "unitShort": "sprigs",
              "unitLong": "sprigs"
            },
            "metric": {
              "amount": 3,
              "unitShort": "sprigs",
              "unitLong": "sprigs"
            }
          }
        },
        {
          "id": 2047,
          "aisle": "Spices and Seasonings",
          "image": "salt.jpg",
          "consistency": "SOLID",
          "name": "salt",
          "nameClean": "salt",
          "original": "Salt for taste",
          "originalName": "Salt for taste",
          "amount": 3,
          "unit": "servings",
          "meta": [
            "for taste"
          ],
          "measures": {
            "us": {
              "amount": 3,
              "unitShort": "servings",
              "unitLong": "servings"
            },
            "metric": {
              "amount": 3,
              "unitShort": "servings",
              "unitLong": "servings"
            }
          }
        },
        {
          "id": 4582,
          "aisle": "Oil, Vinegar, Salad Dressing",
          "image": "vegetable-oil.jpg",
          "consistency": "LIQUID",
          "name": "oil",
          "nameClean": "oil",
          "original": "Oil for frying",
          "originalName": "Oil for frying",
          "amount": 3,
          "unit": "servings",
          "meta": [
            "for frying"
          ],
          "measures": {
            "us": {
              "amount": 3,
              "unitShort": "servings",
              "unitLong": "servings"
            },
            "metric": {
              "amount": 3,
              "unitShort": "servings",
              "unitLong": "servings"
            }
          }
        }
      ],
      "nutrition": {
        "nutrients": [
          {
            "name": "Calories",
            "amount": 177.47,
            "unit": "kcal",
            "percentOfDailyNeeds": 8.87
          },
          {
            "name": "Fat",
            "amount": 3.24,
            "unit": "g",
            "percentOfDailyNeeds": 4.98
          },
          {
            "name": "Saturated Fat",
            "amount": 0.3,
            "unit": "g",
            "percentOfDailyNeeds": 1.89
          },
          {
            "name": "Carbohydrates",
            "amount": 34.5,
            "unit": "g",
            "percentOfDailyNeeds": 11.5
          },
          {
            "name": "Net Carbohydrates",
            "amount": 30.5,
            "unit": "g",
            "percentOfDailyNeeds": 11.09
          },
          {
            "name": "Sugar",
            "amount": 2.81,
            "unit": "g",
            "percentOfDailyNeeds": 3.12
          },
          {
            "name": "Cholesterol",
            "amount": 0,
            "unit": "mg",
            "percentOfDailyNeeds": 0
          },
          {
            "name": "Sodium",
            "amount": 246.89,
            "unit": "mg",
            "percentOfDailyNeeds": 10.73
          },
          {
            "name": "Alcohol",
            "amount": 0,
            "unit": "g",
            "percentOfDailyNeeds": 100
          },
          {
            "name": "Alcohol %",
            "amount": 0,
            "unit": "%",
            "percentOfDailyNeeds": 100
          },
          {
            "name": "Protein",
            "amount": 4.21,
            "unit": "g",
            "percentOfDailyNeeds": 8.42
          },
          {
            "name": "Vitamin B3",
            "amount": 25.55,
            "unit": "mg",
            "percentOfDailyNeeds": 127.76
          },
          {
            "name": "Vitamin C",
            "amount": 58.32,
            "unit": "mg",
            "percentOfDailyNeeds": 70.7
          },
          {
            "name": "Folate",
            "amount": 273.59,
            "unit": "µg",
            "percentOfDailyNeeds": 68.4
          },
          {
            "name": "Potassium",
            "amount": 986.74,
            "unit": "mg",
            "percentOfDailyNeeds": 28.19
          },
          {
            "name": "Vitamin B6",
            "amount": 0.38,
            "unit": "mg",
            "percentOfDailyNeeds": 19.05
          },
          {
            "name": "Fiber",
            "amount": 4,
            "unit": "g",
            "percentOfDailyNeeds": 15.99
          },
          {
            "name": "Manganese",
            "amount": 0.32,
            "unit": "mg",
            "percentOfDailyNeeds": 15.88
          },
          {
            "name": "Copper",
            "amount": 0.3,
            "unit": "mg",
            "percentOfDailyNeeds": 14.78
          },
          {
            "name": "Phosphorus",
            "amount": 133.2,
            "unit": "mg",
            "percentOfDailyNeeds": 13.32
          },
          {
            "name": "Magnesium",
            "amount": 48.65,
            "unit": "mg",
            "percentOfDailyNeeds": 12.16
          },
          {
            "name": "Vitamin B1",
            "amount": 0.18,
            "unit": "mg",
            "percentOfDailyNeeds": 11.71
          },
          {
            "name": "Iron",
            "amount": 1.72,
            "unit": "mg",
            "percentOfDailyNeeds": 9.56
          },
          {
            "name": "Vitamin K",
            "amount": 9.12,
            "unit": "µg",
            "percentOfDailyNeeds": 8.69
          },
          {
            "name": "Vitamin A",
            "amount": 357.36,
            "unit": "IU",
            "percentOfDailyNeeds": 7.15
          },
          {
            "name": "Vitamin B5",
            "amount": 0.6,
            "unit": "mg",
            "percentOfDailyNeeds": 6.02
          },
          {
            "name": "Vitamin E",
            "amount": 0.85,
            "unit": "mg",
            "percentOfDailyNeeds": 5.7
          },
          {
            "name": "Zinc",
            "amount": 0.74,
            "unit": "mg",
            "percentOfDailyNeeds": 4.96
          },
          {
            "name": "Vitamin B2",
            "amount": 0.08,
            "unit": "mg",
            "percentOfDailyNeeds": 4.51
          },
          {
            "name": "Calcium",
            "amount": 32.69,
            "unit": "mg",
            "percentOfDailyNeeds": 3.27
          },
          {
            "name": "Selenium",
            "amount": 1.25,
            "unit": "µg",
            "percentOfDailyNeeds": 1.78
          }
        ],
        "properties": [
          {
            "name": "Glycemic Index",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Glycemic Load",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Inflammation Score",
            "amount": -7,
            "unit": ""
          },
          {
            "name": "Nutrition Score",
            "amount": 18.339999893437263,
            "unit": "%"
          }
        ],
        "flavonoids": [
          {
            "name": "Cyanidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Petunidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Delphinidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Malvidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Pelargonidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Peonidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Catechin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Epigallocatechin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Epicatechin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Epicatechin 3-gallate",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Epigallocatechin 3-gallate",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Theaflavin",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Thearubigins",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Eriodictyol",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Hesperetin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Naringenin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Apigenin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Luteolin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Isorhamnetin",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Kaempferol",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Myricetin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Quercetin",
            "amount": 1.38,
            "unit": "mg"
          },
          {
            "name": "Theaflavin-3,3'-digallate",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Theaflavin-3'-gallate",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Theaflavin-3-gallate",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Gallocatechin",
            "amount": 0,
            "unit": "mg"
          }
        ],
        "ingredients": [
          {
            "id": 10011355,
            "name": "potatoes - remove skin",
            "amount": 1,
            "unit": "",
            "nutrients": [
              {
                "name": "Folic Acid",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Net Carbohydrates",
                "amount": 30.25,
                "unit": "g",
                "percentOfDailyNeeds": 11.09
              },
              {
                "name": "Vitamin K",
                "amount": 6.18,
                "unit": "µg",
                "percentOfDailyNeeds": 8.69
              },
              {
                "name": "Vitamin B12",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Calcium",
                "amount": 21.3,
                "unit": "mg",
                "percentOfDailyNeeds": 3.27
              },
              {
                "name": "Phosphorus",
                "amount": 129.93,
                "unit": "mg",
                "percentOfDailyNeeds": 13.32
              },
              {
                "name": "Manganese",
                "amount": 0.3,
                "unit": "mg",
                "percentOfDailyNeeds": 15.88
              },
              {
                "name": "Poly Unsaturated Fat",
                "amount": 0.13,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Sugar",
                "amount": 2.75,
                "unit": "g",
                "percentOfDailyNeeds": 3.12
              },
              {
                "name": "Sodium",
                "amount": 38.34,
                "unit": "mg",
                "percentOfDailyNeeds": 10.73
              },
              {
                "name": "Vitamin B6",
                "amount": 0.36,
                "unit": "mg",
                "percentOfDailyNeeds": 19.05
              },
              {
                "name": "Calories",
                "amount": 149.1,
                "unit": "kcal",
                "percentOfDailyNeeds": 8.87
              },
              {
                "name": "Magnesium",
                "amount": 46.86,
                "unit": "mg",
                "percentOfDailyNeeds": 12.16
              },
              {
                "name": "Lycopene",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Cholesterol",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fat",
                "amount": 0.3,
                "unit": "g",
                "percentOfDailyNeeds": 4.98
              },
              {
                "name": "Selenium",
                "amount": 1.06,
                "unit": "µg",
                "percentOfDailyNeeds": 1.78
              },
              {
                "name": "Vitamin B5",
                "amount": 0.59,
                "unit": "mg",
                "percentOfDailyNeeds": 6.02
              },
              {
                "name": "Vitamin D",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Iron",
                "amount": 1.55,
                "unit": "mg",
                "percentOfDailyNeeds": 9.56
              },
              {
                "name": "Vitamin A",
                "amount": 14.91,
                "unit": "IU",
                "percentOfDailyNeeds": 7.15
              },
              {
                "name": "Alcohol",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 100
              },
              {
                "name": "Folate",
                "amount": 38.34,
                "unit": "µg",
                "percentOfDailyNeeds": 68.4
              },
              {
                "name": "Mono Unsaturated Fat",
                "amount": 0.01,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Vitamin E",
                "amount": 0.02,
                "unit": "mg",
                "percentOfDailyNeeds": 5.7
              },
              {
                "name": "Copper",
                "amount": 0.29,
                "unit": "mg",
                "percentOfDailyNeeds": 14.78
              },
              {
                "name": "Choline",
                "amount": 34.93,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Caffeine",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fiber",
                "amount": 3.62,
                "unit": "g",
                "percentOfDailyNeeds": 15.99
              },
              {
                "name": "Vitamin B2",
                "amount": 0.07,
                "unit": "mg",
                "percentOfDailyNeeds": 4.51
              },
              {
                "name": "Vitamin B3",
                "amount": 2.45,
                "unit": "mg",
                "percentOfDailyNeeds": 127.76
              },
              {
                "name": "Protein",
                "amount": 4.03,
                "unit": "g",
                "percentOfDailyNeeds": 8.42
              },
              {
                "name": "Vitamin C",
                "amount": 18.32,
                "unit": "mg",
                "percentOfDailyNeeds": 70.7
              },
              {
                "name": "Saturated Fat",
                "amount": 0.07,
                "unit": "g",
                "percentOfDailyNeeds": 1.89
              },
              {
                "name": "Vitamin B1",
                "amount": 0.17,
                "unit": "mg",
                "percentOfDailyNeeds": 11.71
              },
              {
                "name": "Carbohydrates",
                "amount": 33.87,
                "unit": "g",
                "percentOfDailyNeeds": 11.5
              },
              {
                "name": "Potassium",
                "amount": 969.15,
                "unit": "mg",
                "percentOfDailyNeeds": 28.19
              },
              {
                "name": "Zinc",
                "amount": 0.7,
                "unit": "mg",
                "percentOfDailyNeeds": 4.96
              }
            ]
          },
          {
            "id": 2009,
            "name": "chili powder",
            "amount": 0.33,
            "unit": "tsp",
            "nutrients": [
              {
                "name": "Folic Acid",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Net Carbohydrates",
                "amount": 0.13,
                "unit": "g",
                "percentOfDailyNeeds": 11.09
              },
              {
                "name": "Trans Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 110.6
              },
              {
                "name": "Vitamin K",
                "amount": 0.95,
                "unit": "µg",
                "percentOfDailyNeeds": 8.69
              },
              {
                "name": "Vitamin B12",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Calcium",
                "amount": 2.97,
                "unit": "mg",
                "percentOfDailyNeeds": 3.27
              },
              {
                "name": "Phosphorus",
                "amount": 2.7,
                "unit": "mg",
                "percentOfDailyNeeds": 13.32
              },
              {
                "name": "Manganese",
                "amount": 0.02,
                "unit": "mg",
                "percentOfDailyNeeds": 15.88
              },
              {
                "name": "Poly Unsaturated Fat",
                "amount": 0.07,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Sugar",
                "amount": 0.06,
                "unit": "g",
                "percentOfDailyNeeds": 3.12
              },
              {
                "name": "Sodium",
                "amount": 14.76,
                "unit": "mg",
                "percentOfDailyNeeds": 10.73
              },
              {
                "name": "Vitamin B6",
                "amount": 0.02,
                "unit": "mg",
                "percentOfDailyNeeds": 19.05
              },
              {
                "name": "Calories",
                "amount": 2.54,
                "unit": "kcal",
                "percentOfDailyNeeds": 8.87
              },
              {
                "name": "Magnesium",
                "amount": 1.34,
                "unit": "mg",
                "percentOfDailyNeeds": 12.16
              },
              {
                "name": "Lycopene",
                "amount": 0.19,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Cholesterol",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fat",
                "amount": 0.13,
                "unit": "g",
                "percentOfDailyNeeds": 4.98
              },
              {
                "name": "Selenium",
                "amount": 0.18,
                "unit": "µg",
                "percentOfDailyNeeds": 1.78
              },
              {
                "name": "Vitamin B5",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 6.02
              },
              {
                "name": "Vitamin D",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Iron",
                "amount": 0.16,
                "unit": "mg",
                "percentOfDailyNeeds": 9.56
              },
              {
                "name": "Vitamin A",
                "amount": 266.85,
                "unit": "IU",
                "percentOfDailyNeeds": 7.15
              },
              {
                "name": "Alcohol",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 100
              },
              {
                "name": "Folate",
                "amount": 0.25,
                "unit": "µg",
                "percentOfDailyNeeds": 68.4
              },
              {
                "name": "Mono Unsaturated Fat",
                "amount": 0.03,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Vitamin E",
                "amount": 0.34,
                "unit": "mg",
                "percentOfDailyNeeds": 5.7
              },
              {
                "name": "Copper",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 14.78
              },
              {
                "name": "Choline",
                "amount": 0.6,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Caffeine",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fiber",
                "amount": 0.31,
                "unit": "g",
                "percentOfDailyNeeds": 15.99
              },
              {
                "name": "Vitamin B2",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 4.51
              },
              {
                "name": "Vitamin B3",
                "amount": 0.1,
                "unit": "mg",
                "percentOfDailyNeeds": 127.76
              },
              {
                "name": "Protein",
                "amount": 0.12,
                "unit": "g",
                "percentOfDailyNeeds": 8.42
              },
              {
                "name": "Vitamin C",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 70.7
              },
              {
                "name": "Saturated Fat",
                "amount": 0.02,
                "unit": "g",
                "percentOfDailyNeeds": 1.89
              },
              {
                "name": "Vitamin B1",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 11.71
              },
              {
                "name": "Carbohydrates",
                "amount": 0.45,
                "unit": "g",
                "percentOfDailyNeeds": 11.5
              },
              {
                "name": "Potassium",
                "amount": 17.55,
                "unit": "mg",
                "percentOfDailyNeeds": 28.19
              },
              {
                "name": "Zinc",
                "amount": 0.04,
                "unit": "mg",
                "percentOfDailyNeeds": 4.96
              }
            ]
          },
          {
            "id": 93604,
            "name": "curry leaves",
            "amount": 1,
            "unit": "sprigs",
            "nutrients": [
              {
                "name": "Net Carbohydrates",
                "amount": 0.12,
                "unit": "g",
                "percentOfDailyNeeds": 11.09
              },
              {
                "name": "Trans Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 110.6
              },
              {
                "name": "Vitamin K",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 8.69
              },
              {
                "name": "Vitamin B12",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Calcium",
                "amount": 8.3,
                "unit": "mg",
                "percentOfDailyNeeds": 3.27
              },
              {
                "name": "Phosphorus",
                "amount": 0.57,
                "unit": "mg",
                "percentOfDailyNeeds": 13.32
              },
              {
                "name": "Manganese",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 15.88
              },
              {
                "name": "Poly Unsaturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fluoride",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Sugar",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 3.12
              },
              {
                "name": "Sodium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 10.73
              },
              {
                "name": "Vitamin B6",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 19.05
              },
              {
                "name": "Calories",
                "amount": 1.08,
                "unit": "kcal",
                "percentOfDailyNeeds": 8.87
              },
              {
                "name": "Magnesium",
                "amount": 0.44,
                "unit": "mg",
                "percentOfDailyNeeds": 12.16
              },
              {
                "name": "Cholesterol",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fat",
                "amount": 0.01,
                "unit": "g",
                "percentOfDailyNeeds": 4.98
              },
              {
                "name": "Selenium",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 1.78
              },
              {
                "name": "Vitamin B5",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 6.02
              },
              {
                "name": "Vitamin D",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Iron",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 9.56
              },
              {
                "name": "Vitamin A",
                "amount": 75.6,
                "unit": "IU",
                "percentOfDailyNeeds": 7.15
              },
              {
                "name": "Alcohol",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 100
              },
              {
                "name": "Folate",
                "amount": 235,
                "unit": "µg",
                "percentOfDailyNeeds": 68.4
              },
              {
                "name": "Mono Unsaturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Vitamin E",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 5.7
              },
              {
                "name": "Copper",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 14.78
              },
              {
                "name": "Caffeine",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fiber",
                "amount": 0.06,
                "unit": "g",
                "percentOfDailyNeeds": 15.99
              },
              {
                "name": "Vitamin B2",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.51
              },
              {
                "name": "Vitamin B3",
                "amount": 23,
                "unit": "mg",
                "percentOfDailyNeeds": 127.76
              },
              {
                "name": "Protein",
                "amount": 0.06,
                "unit": "g",
                "percentOfDailyNeeds": 8.42
              },
              {
                "name": "Vitamin C",
                "amount": 40,
                "unit": "mg",
                "percentOfDailyNeeds": 70.7
              },
              {
                "name": "Saturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 1.89
              },
              {
                "name": "Vitamin B1",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 11.71
              },
              {
                "name": "Carbohydrates",
                "amount": 0.19,
                "unit": "g",
                "percentOfDailyNeeds": 11.5
              },
              {
                "name": "Potassium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 28.19
              },
              {
                "name": "Zinc",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.96
              }
            ]
          },
          {
            "id": 2047,
            "name": "salt",
            "amount": 1,
            "unit": "servings",
            "nutrients": [
              {
                "name": "Folic Acid",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Net Carbohydrates",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 11.09
              },
              {
                "name": "Vitamin K",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 8.69
              },
              {
                "name": "Vitamin B12",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Calcium",
                "amount": 0.12,
                "unit": "mg",
                "percentOfDailyNeeds": 3.27
              },
              {
                "name": "Phosphorus",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 13.32
              },
              {
                "name": "Manganese",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 15.88
              },
              {
                "name": "Poly Unsaturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fluoride",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Sugar",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 3.12
              },
              {
                "name": "Sodium",
                "amount": 193.79,
                "unit": "mg",
                "percentOfDailyNeeds": 10.73
              },
              {
                "name": "Vitamin B6",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 19.05
              },
              {
                "name": "Calories",
                "amount": 0,
                "unit": "kcal",
                "percentOfDailyNeeds": 8.87
              },
              {
                "name": "Magnesium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 12.16
              },
              {
                "name": "Lycopene",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Cholesterol",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 4.98
              },
              {
                "name": "Selenium",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 1.78
              },
              {
                "name": "Vitamin B5",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 6.02
              },
              {
                "name": "Vitamin D",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Iron",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 9.56
              },
              {
                "name": "Vitamin A",
                "amount": 0,
                "unit": "IU",
                "percentOfDailyNeeds": 7.15
              },
              {
                "name": "Alcohol",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 100
              },
              {
                "name": "Folate",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 68.4
              },
              {
                "name": "Mono Unsaturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Vitamin E",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 5.7
              },
              {
                "name": "Copper",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 14.78
              },
              {
                "name": "Choline",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Caffeine",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fiber",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 15.99
              },
              {
                "name": "Vitamin B2",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.51
              },
              {
                "name": "Vitamin B3",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 127.76
              },
              {
                "name": "Protein",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 8.42
              },
              {
                "name": "Vitamin C",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 70.7
              },
              {
                "name": "Saturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 1.89
              },
              {
                "name": "Vitamin B1",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 11.71
              },
              {
                "name": "Carbohydrates",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 11.5
              },
              {
                "name": "Potassium",
                "amount": 0.04,
                "unit": "mg",
                "percentOfDailyNeeds": 28.19
              },
              {
                "name": "Zinc",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.96
              }
            ]
          },
          {
            "id": 4582,
            "name": "oil",
            "amount": 1,
            "unit": "servings",
            "nutrients": [
              {
                "name": "Folic Acid",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Net Carbohydrates",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 11.09
              },
              {
                "name": "Trans Fat",
                "amount": 0.06,
                "unit": "g",
                "percentOfDailyNeeds": 110.6
              },
              {
                "name": "Vitamin K",
                "amount": 9.98,
                "unit": "µg",
                "percentOfDailyNeeds": 8.69
              },
              {
                "name": "Vitamin B12",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Calcium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 3.27
              },
              {
                "name": "Phosphorus",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 13.32
              },
              {
                "name": "Manganese",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 15.88
              },
              {
                "name": "Poly Unsaturated Fat",
                "amount": 3.93,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Sugar",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 3.12
              },
              {
                "name": "Sodium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 10.73
              },
              {
                "name": "Vitamin B6",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 19.05
              },
              {
                "name": "Calories",
                "amount": 123.76,
                "unit": "kcal",
                "percentOfDailyNeeds": 8.87
              },
              {
                "name": "Magnesium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 12.16
              },
              {
                "name": "Lycopene",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Cholesterol",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fat",
                "amount": 14,
                "unit": "g",
                "percentOfDailyNeeds": 4.98
              },
              {
                "name": "Selenium",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 1.78
              },
              {
                "name": "Vitamin B5",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 6.02
              },
              {
                "name": "Vitamin D",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Iron",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 9.56
              },
              {
                "name": "Vitamin A",
                "amount": 0,
                "unit": "IU",
                "percentOfDailyNeeds": 7.15
              },
              {
                "name": "Alcohol",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 100
              },
              {
                "name": "Folate",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 68.4
              },
              {
                "name": "Mono Unsaturated Fat",
                "amount": 8.86,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Vitamin E",
                "amount": 2.45,
                "unit": "mg",
                "percentOfDailyNeeds": 5.7
              },
              {
                "name": "Copper",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 14.78
              },
              {
                "name": "Choline",
                "amount": 0.03,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Caffeine",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fiber",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 15.99
              },
              {
                "name": "Vitamin B2",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.51
              },
              {
                "name": "Vitamin B3",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 127.76
              },
              {
                "name": "Protein",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 8.42
              },
              {
                "name": "Vitamin C",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 70.7
              },
              {
                "name": "Saturated Fat",
                "amount": 1.03,
                "unit": "g",
                "percentOfDailyNeeds": 1.89
              },
              {
                "name": "Vitamin B1",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 11.71
              },
              {
                "name": "Carbohydrates",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 11.5
              },
              {
                "name": "Potassium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 28.19
              },
              {
                "name": "Zinc",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.96
              }
            ]
          }
        ],
        "caloricBreakdown": {
          "percentProtein": 9.15,
          "percentFat": 15.83,
          "percentCarbs": 75.02
        },
        "weightPerServing": {
          "amount": 229,
          "unit": "g"
        }
      },
      "summary": "Curry Leaves Potato Chips requires approximately <b>45 minutes</b> from start to finish. This recipe serves 3 and costs 55 cents per serving. One portion of this dish contains around <b>4g of protein</b>, <b>3g of fat</b>, and a total of <b>177 calories</b>. 4 people were glad they tried this recipe. If you have oil, chili powder, salt, and a few other ingredients on hand, you can make it. It is brought to you by Foodista. Not a lot of people really liked this side dish. This recipe is typical of American cuisine. It is a good option if you're following a <b>gluten free, dairy free, lacto ovo vegetarian, and fodmap friendly</b> diet. All things considered, we decided this recipe <b>deserves a spoonacular score of 92%</b>. This score is outstanding. Users who liked this recipe also liked <a href=\"https://spoonacular.com/recipes/chicken-stir-fry-with-potato-cashews-and-curry-leaves-202216\">Chicken Stir Fry with Potato, Cashews, and Curry Leaves</a>, <a href=\"https://spoonacular.com/recipes/yam-leaves-stir-fried-sweet-potato-leaves-960798\">Yam Leaves, Stir-Fried Sweet Potato Leaves</a>, and <a href=\"https://spoonacular.com/recipes/curry-leaves-chutney-how-to-make-curry-leaves-chutney-487613\">curry leaves chutney , how to make curry leaves chutney</a>.",
      "cuisines": [
        "American"
      ],
      "dishTypes": [
        "side dish"
      ],
      "diets": [
        "gluten free",
        "dairy free",
        "lacto ovo vegetarian",
        "fodmap friendly",
        "whole 30",
        "vegan"
      ],
      "occasions": [],
      "analyzedInstructions": [
        {
          "name": "",
          "steps": [
            {
              "number": 1,
              "step": "Wipe/pat dry potatoes.",
              "ingredients": [
                {
                  "id": 11352,
                  "name": "potato",
                  "localizedName": "potato",
                  "image": "potatoes-yukon-gold.png"
                }
              ],
              "equipment": []
            },
            {
              "number": 2,
              "step": "Mix in chili powder and salt.",
              "ingredients": [
                {
                  "id": 2009,
                  "name": "chili powder",
                  "localizedName": "chili powder",
                  "image": "chili-powder.jpg"
                },
                {
                  "id": 2047,
                  "name": "salt",
                  "localizedName": "salt",
                  "image": "salt.jpg"
                }
              ],
              "equipment": []
            },
            {
              "number": 3,
              "step": "Heat oil and fry in batches till crunchy and crispy.",
              "ingredients": [
                {
                  "id": 4582,
                  "name": "cooking oil",
                  "localizedName": "cooking oil",
                  "image": "vegetable-oil.jpg"
                }
              ],
              "equipment": []
            },
            {
              "number": 4,
              "step": "Remove and keep aside.",
              "ingredients": [],
              "equipment": []
            },
            {
              "number": 5,
              "step": "In the same oil, fry curry leaves till crispy too.",
              "ingredients": [
                {
                  "id": 93604,
                  "name": "curry leaves",
                  "localizedName": "curry leaves",
                  "image": "curry-leaves.jpg"
                },
                {
                  "id": 4582,
                  "name": "cooking oil",
                  "localizedName": "cooking oil",
                  "image": "vegetable-oil.jpg"
                }
              ],
              "equipment": []
            },
            {
              "number": 6,
              "step": "Scoop out and add over chips.",
              "ingredients": [
                {
                  "id": 11408,
                  "name": "french fries",
                  "localizedName": "french fries",
                  "image": "french-fries-isolated.jpg"
                }
              ],
              "equipment": []
            },
            {
              "number": 7,
              "step": "Crush and toss the leaves with the chips.",
              "ingredients": [
                {
                  "id": 11408,
                  "name": "french fries",
                  "localizedName": "french fries",
                  "image": "french-fries-isolated.jpg"
                }
              ],
              "equipment": []
            }
          ]
        }
      ],
      "spoonacularScore": 70.99125671386719,
      "spoonacularSourceUrl": "https://spoonacular.com/curry-leaves-potato-chips-641122",
      "usedIngredientCount": 1,
      "missedIngredientCount": 2,
      "likes": 0,
      "missedIngredients": [
        {
          "id": 2009,
          "amount": 1,
          "unit": "tsp",
          "unitLong": "teaspoon",
          "unitShort": "tsp",
          "aisle": "Spices and Seasonings",
          "name": "chili powder",
          "original": "1 tsp plain chili powder",
          "originalName": "plain chili powder",
          "meta": [
            "plain"
          ],
          "extendedName": "plain chili powder",
          "image": "https://img.spoonacular.com/ingredients_100x100/chili-powder.jpg"
        },
        {
          "id": 93604,
          "amount": 3,
          "unit": "sprigs",
          "unitLong": "sprigs",
          "unitShort": "sprigs",
          "aisle": "Ethnic Foods",
          "name": "curry leaves",
          "original": "3-4 sprigs curry leaves",
          "originalName": "curry leaves",
          "meta": [],
          "image": "https://img.spoonacular.com/ingredients_100x100/curry-leaves.jpg"
        }
      ],
      "usedIngredients": [
        {
          "id": 10011355,
          "amount": 3,
          "unit": "",
          "unitLong": "",
          "unitShort": "",
          "aisle": "Produce",
          "name": "potatoes - remove skin",
          "original": "3 potatoes - remove skin, sliced thinly and soaked in ice water for 10-15 minutes.",
          "originalName": "potatoes - remove skin, sliced thinly and soaked in ice water for 10-15 minutes",
          "meta": [
            "sliced",
            "for 10-15 minutes."
          ],
          "image": "https://img.spoonacular.com/ingredients_100x100/red-potatoes.jpg"
        }
      ],
      "unusedIngredients": []
    }

    user_id  = session.get("user_id")

    # If null user_id
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # Write data to database
    with db.DBSession() as db_session:
        try:
            recipe_db_class = recipe_mapper(recipe_data)
            print("\n"*5 + "here0")
            recipe_db_class.user_id = user_id
            print("\n"*5 + "here1")
            db_session.add(recipe_db_class)
            print("\n"*5 + "here2")
            db_session.commit()
            print("\n"*5 + "here3")
            
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
