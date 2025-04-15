# Standard Libraries
from tomllib import loads as tomlloads
from pathlib import Path
import json

# External Libraries
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Custom Libraries
from data_classes import Response, Recipe, Ingredient, json_mapper
from db_models import recipe_to_db, db_to_recipe, ingredient_to_db, db_to_ingredient, Base, RecipeDB, IngredientDB


class Client:

    def __init__(self):

        # Set up SQL database

        self.engine = create_engine("sqlite:///../assets/database.db")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        # Query vars
        self.base_url: str = "https://api.spoonacular.com/recipes/complexSearch"
        self.api_key = tomlloads((Path(__file__).parent.parent / "assets" / "config.toml").read_text())["apikey"]

    # Main functions
    def get_recipes(
        self,
        include_ingredients: str,
        exclude_ingredients: str,
        cuisine: str,
        intolerances: str,
        diet:str):

        # Add required params
        params = {
            "includeIngredients": include_ingredients,
            "instructionsRequired": True,
            "addRecipeInformation": None,
            "addRecipeInstructions": None,
            "apiKey": self.api_key
        }

        # Add optional params
        if exclude_ingredients:
            params["excludeIngredients"] = exclude_ingredients
        if cuisine:
            params["cuisine"] = cuisine
        if intolerances:
            params["intolerances"] = intolerances
        if diet:
            params["diet"] = diet

        request_url = requests.Request(method="GET", url=self.base_url, params=params).prepare().url

        # Query Spoonacular API
        response = json_mapper(json.loads(requests.get(request_url).text), Response)

        # Dummy response
        response = json_mapper(self.get_dummy_data(), Response)

        return response.results


    def save_recipe(self, recipe: Recipe):
        with self.Session() as session:
            recipe_db_class = recipe_to_db(recipe)
            session.add(recipe_db_class)
            session.commit()

        return "200"


    def delete_recipe(self, recipe_id: int) -> int:
        with self.Session() as session:
            try:
                session.query(RecipeDB).filter_by(id=recipe_id).delete()
                session.commit()
                
            except Exception as e:
                session.rollback()
                raise e
        return "200"


    def list_recipes(self):
        with self.Session() as session:
            return [db_to_recipe(recipe) for recipe in session.query(RecipeDB).all()]


    def add_ingredient(self, ingredient: Ingredient):
        with self.Session() as session:
            ingredient_db_class = ingredient_to_db(ingredient)
            session.add(ingredient_db_class)
            session.commit()
        
        return "200"

    def remove_ingredient(self, ingredient_id: int) -> int:
        with self.Session() as session:
            try:
                session.query(IngredientDB).filter_by(id=ingredient_id).delete()
                session.commit()
                
            except Exception as e:
                session.rollback()
                raise e
        return "200"

    def list_ingredients(self):
        with self.Session() as session:
            return [db_to_ingredient(ingredient) for ingredient in session.query(IngredientDB).all()]


    def get_dummy_data(self) -> dict:
        with open('../assets/cached.json') as f:
            return json.load(f, strict=False)