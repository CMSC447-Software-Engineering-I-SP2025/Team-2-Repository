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

    def __init__(self) -> None:
        """Initialize the client object."""

        # Set up SQL database
        self.engine = create_engine(f"sqlite:///{(Path(__file__).resolve().parent.parent / 'assets' / 'database.db').as_posix()}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        # Query vars
        self.base_url: str = "https://api.spoonacular.com/recipes/complexSearch"
        self.api_key = tomlloads((Path(__file__).parent.parent / "assets" / "config.toml").read_text())["apikey"]

    # Main functions
    def get_recipes(self, include_ingredients: str, exclude_ingredients: str, cuisine: str, intolerances: str, diet:str) -> Response:
        """Query the spoonacular API for recipes.

        Args:
            include_ingredients (str): Ingredients the recipes should have.
            exclude_ingredients (str): Ingredients the recipes should NOT have.
            cuisine (str): Type of cuisine the recipes should be.
            intolerances (str): Allergens that the recipe should not include.
            diet (str): Diet that the recipe must follow.

        Returns:
            Response: Response data class object.
        """

        # Add required params
        params = {
            "includeIngredients": include_ingredients,
            "instructionsRequired": True,
            "addRecipeInformation": True,
            "addRecipeInstructions": True,
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

        request_url = requests.Request(method="GET", url=self.base_url, params=params).prepare().url     # Build the request
        print(request_url)
        response = json_mapper(json.loads(requests.get(request_url).text), Response)    # Query Spoonacular API        
        #response = json_mapper(self.get_dummy_data(), Response) # Dummy response
        print(response.results)

        return response.results


    def save_recipe(self, recipe: Recipe) -> str:
        """Save a recipe to the database.

        Args:
            recipe (Recipe): Recipe to save.

        Returns:
            str: Success response.
        """
        with self.Session() as session:
            recipe_db_class = recipe_to_db(recipe)
            session.add(recipe_db_class)
            session.commit()

        return "200"


    def delete_recipe(self, recipe_id: int) -> str:
        """Delete a recipe from the database.

        Args:
            recipe_id (int): ID of the recipe to delete.

        Raises:
            e: Error when writing to database.

        Returns:
            str: Success message.
        """
        with self.Session() as session:
            try:
                session.query(RecipeDB).filter_by(id=recipe_id).delete()
                session.commit()
                
            except Exception as e:
                session.rollback()
                raise e
        return "200"


    def list_recipes(self) -> list[Recipe]:
        """List all saved recipes.

        Returns:
            list[Recipe]: List of saved recipes.
        """
        with self.Session() as session:
            return [db_to_recipe(recipe) for recipe in session.query(RecipeDB).all()]


    def add_ingredient(self, ingredient: Ingredient) -> str:
        """Add an ingredient to the database.

        Args:
            ingredient (Ingredient): Ingredient to add to the database.

        Returns:
            str: Success string.
        """
        with self.Session() as session:
            ingredient_db_class = ingredient_to_db(ingredient)
            session.add(ingredient_db_class)
            session.commit()
        
        return "200"


    def remove_ingredient(self, ingredient_id: int) -> str:
        """Remove an ingredient to the database.

        Args:
            ingredient_id (int): ID of ingredient to delete.

        Raises:
            e: Error writing to database.

        Returns:
            str: Success string.
        """
        with self.Session() as session:
            try:
                session.query(IngredientDB).filter_by(id=ingredient_id).delete()
                session.commit()
                
            except Exception as e:
                session.rollback()
                raise e
        return "200"

    def list_ingredients(self) -> list[Ingredient]:
        """List all ingredients in the database.

        Returns:
            list[Ingredient]: List of ingredient dataclass objects. 
        """
        with self.Session() as session:
            return [db_to_ingredient(ingredient) for ingredient in session.query(IngredientDB).all()]


    def get_dummy_data(self) -> dict:
        """Get dummt data for testing.

        Returns:
            dict: Dummy data.
        """
        with open(Path(__file__).parent.parent / "assets" / "cached.json") as f:
            return json.load(f, strict=False)