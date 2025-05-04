"""Core business logic."""
# Standard Libraries
from json import load as jsonload
from json import loads as jsonloads
from pathlib import Path
from typing import Any

# Custom Libraries
from data_classes import Ingredient, Recipe, Response, json_mapper
from db_data_models import (
    Base,
    IngredientDB,
    RecipeDB,
)
from mappers import ingredient_mapper, recipe_mapper

# External Libraries
from requests import Request
from requests import get as reqget
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tomllib import loads as tomlloads


class Client:
    """Client object to communicate with the frontend and database."""

    def __init__(self) -> None:
        """Initialize the client object."""

        # Get paths
        db_path: Path = Path(__file__).resolve().parent.parent / "assets" / "database.db"
        config_path: Path = Path(__file__).parent.parent / "assets" / "config.toml"

        # Set up SQL database
        self.engine = create_engine(f"sqlite:///{(db_path).as_posix()}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        # Query vars
        self.base_url: str = "https://api.spoonacular.com/recipes/complexSearch"
        self.api_key = tomlloads((config_path).read_text())["apikey"]

    # Main functions
    def search_recipes(
        self,
        include_ingredients: str,
        exclude_ingredients: str,
        cuisine: str,
        intolerances: str,
        diet:str) -> Response:
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
            "apiKey": self.api_key,
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

        # Build request
        request_url: Request = Request(method="GET", url=self.base_url, params=params).prepare().url

        # Query Spoonacular
        response: Any = json_mapper(jsonloads(reqget(url=request_url, timeout=5).text))

        # Dummy response / debug printing
        # response = json_mapper(self.get_dummy_data())
        #print(response.results)

        return response.results


    def save_recipe(self, recipe: Recipe) -> str:
        """Save a recipe to the database.

        Args:
            recipe (Recipe): Recipe to save.

        Returns:
            str: Success response.

        """
        with self.Session() as session:
            recipe_db_class = recipe_mapper(recipe)
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
            return [recipe_mapper(recipe) for recipe in session.query(RecipeDB).all()]


    def add_ingredient(self, ingredient: Ingredient) -> str:
        """Add an ingredient to the database.

        Args:
            ingredient (Ingredient): Ingredient to add to the database.

        Returns:
            str: Success string.

        """
        with self.Session() as session:
            ingredient_db_class = ingredient_mapper(ingredient)
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
            return [ingredient_mapper(ingr) for ingr in session.query(IngredientDB).all()]


    def get_dummy_data(self) -> dict:
        """Get dummt data for testing.

        Returns:
            dict: Dummy data.

        """
        with Path.open(Path(__file__).parent.parent / "assets" / "cached.json") as f:
            return jsonload(f, strict=False)
