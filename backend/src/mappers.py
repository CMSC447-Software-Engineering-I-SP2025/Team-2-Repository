"""Mappers between dataclass types."""
from __future__ import annotations

import json
from typing import Any

from backend_data_models import Ingredient, Recipe, Response
from dacite import Config, from_dict
from db_data_models import IngredientDB, RecipeDB


def recipe_mapper(input_recipe: Recipe | RecipeDB) -> Recipe | RecipeDB:
    """Convert between Recipe dataclass/dict and RecipeDB SQLAlchemy model."""
    # Recipe -> RecipeDB
    if isinstance(input_recipe, Recipe):  # Recipe dict -> RecipeDB
        return RecipeDB(
            recipe_id=input_recipe.get("id"),
            title=input_recipe["title"],
            image=input_recipe["image"],
            servings=input_recipe["servings"],
            used_ingredient_count=input_recipe["used_ingredient_count"],
            missed_ingredient_count=input_recipe["missed_ingredient_count"],
            analyzed_instructions=json.dumps(
                [{k: v for k, v in instr.items() if k != "repr"}
                 for instr in input_recipe.get("instructions", []) or []],
            ),
            nutrition= json.dumps(
                {"nutrients": [{k: v for k, v in nutr.items()}
                for nutr in input_recipe.get("nutrition").get("nutrients", []) or []]},
            )
        )

    # RecipeDB -> Recipe
    return {
        "id": input_recipe.recipe_id,
        "title": input_recipe.title,
        "image": input_recipe.image,
        "servings": input_recipe.servings,
        "used_ingredient_count": input_recipe.used_ingredient_count,
        "missed_ingredient_count": input_recipe.missed_ingredient_count,
        "instructions": [
            dict(instr) for instr in json.loads(input_recipe.analyzed_instructions)
        ],
        "nutrition": {"nutrients": [dict(nutr) for nutr in json.loads(input_recipe.nutrition)["nutrients"]]}
    }

    error = f"Unsupported type: {type(input_recipe)}"
    raise TypeError(error)


def ingredient_mapper(input_ingredient: Ingredient | IngredientDB) -> Ingredient | IngredientDB:
    """Convert between Ingredient dataclass/dict and IngredientDB SQLAlchemy model."""
    # Ingredient -> IngredientDB
    if isinstance(input_ingredient, Ingredient):
        return IngredientDB(
            ingr_id=input_ingredient["id"],
            name=input_ingredient["name"],
            localized_name=input_ingredient.get("localized_name"),
            image=input_ingredient.get("image"),
        )

    # IngredientDB -> Ingredient
    return {
        "id": input_ingredient.ingr_id,
        "name": input_ingredient.name,
        "localized_name": input_ingredient.localized_name,
        "image": input_ingredient.image,
    }


def response_mapper(json_data: Any) -> Any:
    """Map JSON response data to a Response object.

    Args:
        json_data (Any)): JSON response data.

    Returns:
        Any: _description_

    """
    return from_dict(
        data_class=Response,
        data=json_data,
        config=Config(check_types=False, cast=[], strict=False),
    )


def recipe_to_db(recipe: Recipe) -> RecipeDB:
    """Convert a recipe backend object to a recipe database object.

    Args:
        recipe (dict): A recipe backend object.

    Returns:
        RecipeDB: A recipe database object.

    """
    return RecipeDB(
        recipe_id=recipe["id"],
        title=recipe["title"],
        image=recipe["image"],
        servings=recipe["servings"],
        used_ingredient_count=recipe["usedIngredientCount"],
        missed_ingredient_count=recipe["missedIngredientCount"],
        analyzed_instructions=json.dumps(
            [{k: v for k, v in instr.items() if k != "repr"}
             for instr in recipe["analyzedInstructions"] or []]
            if recipe["analyzedInstructions"] is not None
            else [],
        ),
        nutrition=json.dumps(
            {"nutrients": [{k: v for k, v in nutr.items()}
            for nutr in recipe["nutrition"]["nutrients"] or []]}
            if recipe["nutrition"] is not None
            else [],
        )
    )


def db_to_recipe(recipe_db: dict) -> dict:
    """Convert SQLAlchemy model to Recipe dictionary."""
    return {
        "id": recipe_db.recipe_id,
        "title": recipe_db.title,
        "image": recipe_db.image,
        "servings": recipe_db.servings,
        "usedIngredientCount": recipe_db.used_ingredient_count,
        "missedIngredientCount": recipe_db.missed_ingredient_count,
        "analyzedInstructions": [
            dict(instr) for instr in json.loads(recipe_db.analyzed_instructions)
        ],
        "nutrition": {"nutrients": [dict(nutr) for nutr in json.loads(recipe_db.nutrition)["nutrients"]]}
        
    }


def ingredient_to_db(ingredient: dict) -> IngredientDB:
    """Convert Recipe to SQLAlchemy model."""
    return IngredientDB(
        ingr_id=ingredient["id"],
        name=ingredient["name"],
        image=ingredient.get("image"),
    )


def db_to_ingredient(ingredient_db: IngredientDB) -> dict:
    """Convert a database ingredient object into a backend ingredient object.

    Args:
        ingredient_db (IngredientDB): Ingredient database object.

    Returns:
        dict: Ingredient backend object.

    """
    return {
        "id": ingredient_db.ingr_id,
        "name": ingredient_db.name,
        "image": ingredient_db.image,
    }
