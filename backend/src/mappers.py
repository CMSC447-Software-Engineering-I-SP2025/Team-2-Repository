"""Mappers between dataclass types."""
from __future__ import annotations

import json
from typing import Any

from backend_data_models import Ingredient, Recipe
from dacite import Config, from_dict
from db_data_models import IngredientDB, RecipeDB, Response


def recipe_mapper(input_recipe: Recipe | RecipeDB) -> Recipe | RecipeDB:
    """Convert between Recipe dataclass/dict and RecipeDB SQLAlchemy model."""
    # Recipe -> RecipeDB
    if isinstance(input_recipe, Recipe):  # Recipe dict -> RecipeDB
        return RecipeDB(
            id=input_recipe.get("recipe_id", input_recipe.get("id")),
            title=input_recipe["title"],
            image=input_recipe["image"],
            used_ingredient_count=input_recipe["used_ingredient_count"],
            missed_ingredient_count=input_recipe["missed_ingredient_count"],
            analyzed_instructions=json.dumps(
                [{k: v for k, v in instr.items() if k != "repr"}
                 for instr in input_recipe.get("instructions", []) or []],
            ),
        )

    # RecipeDB -> Recipe
    return {
        "id": input_recipe.id,
        "title": input_recipe.title,
        "image": input_recipe.image,
        "used_ingredient_count": input_recipe.used_ingredient_count,
        "missed_ingredient_count": input_recipe.missed_ingredient_count,
        "instructions": [
            dict(instr) for instr in json.loads(input_recipe.analyzed_instructions)
        ],
    }

    error = f"Unsupported type: {type(input_recipe)}"
    raise TypeError(error)


def ingredient_mapper(input_ingredient: Ingredient | IngredientDB) -> Ingredient | IngredientDB:
    """Convert between Ingredient dataclass/dict and IngredientDB SQLAlchemy model."""
    # Ingredient -> IngredientDB
    if isinstance(input_ingredient, Ingredient):
        return IngredientDB(
            id=input_ingredient["id"],
            name=input_ingredient["name"],
            localized_name=input_ingredient.get("localized_name"),
            image=input_ingredient.get("image"),
        )

    # IngredientDB -> Ingredient
    return {
        "id": input_ingredient.id,
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
