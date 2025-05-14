"""Mappers between dataclass types."""
from __future__ import annotations

import json

from backend_data_models import Ingredient, Recipe, Response
from dacite import Config, from_dict
from db_data_models import IngredientDB, RecipeDB


def recipe_mapper(input_recipe: Recipe | RecipeDB) -> Recipe | RecipeDB:
    """Convert between Recipe dataclass/dict and RecipeDB SQLAlchemy model."""
    # print(input_recipe)
    # Recipe -> RecipeDB
    if isinstance(input_recipe, (dict, Recipe)):  # Recipe dict -> RecipeDB

        # Assign values to variables first
        recipe_id = input_recipe.get("id")
        title = input_recipe["title"]
        image = input_recipe["image"]
        servings = input_recipe["servings"]
        analyzed_instructions = json.dumps([
            {k: v for k, v in instr.items() if k != "repr"}
            for instr in input_recipe.get("analyzedInstructions", []) or []
        ])
        nutrition = json.dumps({
            "nutrients": [
                dict(nutr.items())
                for nutr in (input_recipe.get("nutrition", {}).get("nutrients", []) or [])
            ]
        })
        ingredients = input_recipe.get("ingredients")

        print(analyzed_instructions)
        input()

        # Pass variables into RecipeDB
        return RecipeDB(
            recipe_id=recipe_id,
            title=title,
            image=image,
            servings=servings,
            analyzed_instructions=analyzed_instructions,
            nutrition=nutrition,
            ingredients=ingredients,
        )

        # return RecipeDB(
        #     recipe_id=input_recipe.get("id"),
        #     title=input_recipe["title"],
        #     image=input_recipe["image"],
        #     servings=input_recipe["servings"],
        #     analyzed_instructions=json.dumps(
        #         [{k: v for k, v in instr.items() if k != "repr"}
        #          for instr in input_recipe.get("analyzedInstructions", []) or []],
        #     ),
        #     #{"nutrients": [{k: v for k, v in nutr.items()}
        #     nutrition = json.dumps({"nutrients": [dict(nutr.items()) for nutr in input_recipe.get("nutrition", []).get("nutrients", []) or []]},
        #     ),
        #     ingredients=input_recipe.get("ingredients"),
        # )

    # RecipeDB -> Recipe
    return {
        "id": input_recipe.recipe_id,
        "title": input_recipe.title,
        "image": input_recipe.image,
        "servings": input_recipe.servings,
        "instructions": [
            dict(instr) for instr in json.loads(input_recipe.analyzed_instructions)
        ],
        "nutrition": {"nutrients": [dict(nutr) for nutr in json.loads(input_recipe.nutrition)["nutrients"]]},
        "ingredients": list(input_recipe.ingredients),
    }

    error = f"Unsupported type: {type(input_recipe)}"
    raise TypeError(error)


def ingredient_mapper(input_ingredient: Ingredient | IngredientDB) -> Ingredient | IngredientDB:
    """Convert between Ingredient dataclass/dict and IngredientDB SQLAlchemy model."""
    # Ingredient -> IngredientDB
    if isinstance(input_ingredient, (dict, Ingredient)):
        return IngredientDB(
            ingr_id=input_ingredient["id"],
            name=input_ingredient["name"],
            quantity=input_ingredient.get("quantity"),
            unit=input_ingredient.get("unit"),
            image=input_ingredient.get("image"),
        )

    # IngredientDB -> Ingredient
    return {
        "id": input_ingredient.ingr_id,
        "name": input_ingredient.name,
        "quantity": input_ingredient.quantity,
        "unit": input_ingredient.unit,
        "image": input_ingredient.image,
    }


def response_mapper(json_data: dict) -> Response:
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


# Old deprecated mappers

# def recipe_to_db(recipe: Recipe) -> RecipeDB:
#     """Convert a recipe backend object to a recipe database object.

#     Args:
#         recipe (dict): A recipe backend object.

#     Returns:
#         RecipeDB: A recipe database object.

#     """
#     return RecipeDB(
#         recipe_id=recipe["id"],
#         title=recipe["title"],
#         image=recipe["image"],
#         servings=recipe["servings"],
#         used_ingredient_count=recipe["usedIngredientCount"],
#         missed_ingredient_count=recipe["missedIngredientCount"],
#         analyzed_instructions=json.dumps(
#             [{k: v for k, v in instr.items() if k != "repr"}
#              for instr in recipe["analyzedInstructions"] or []]
#             if recipe["analyzedInstructions"] is not None
#             else [],
#         ),
#         nutrition=json.dumps(
#             {"nutrients": [{k: v for k, v in nutr.items()}
#             for nutr in recipe["nutrition"]["nutrients"] or []]}
#             if recipe["nutrition"] is not None
#             else [],
#         )
#     )


# def db_to_recipe(recipe_db: dict) -> dict:
#     """Convert SQLAlchemy model to Recipe dictionary."""
#     return {
#         "id": recipe_db.recipe_id,
#         "title": recipe_db.title,
#         "image": recipe_db.image,
#         "servings": recipe_db.servings,
#         "usedIngredientCount": recipe_db.used_ingredient_count,
#         "missedIngredientCount": recipe_db.missed_ingredient_count,
#         "analyzedInstructions": [
#             dict(instr) for instr in json.loads(recipe_db.analyzed_instructions)
#         ],
#         "nutrition": {"nutrients": [dict(nutr) for nutr in json.loads(recipe_db.nutrition)["nutrients"]]}
#     }


# def ingredient_to_db(ingredient: dict) -> IngredientDB:
#     """Convert Recipe to SQLAlchemy model."""
#     return IngredientDB(
#         ingr_id=ingredient["id"],
#         name=ingredient["name"],
#         image=ingredient.get("image"),
#     )


# def db_to_ingredient(ingredient_db: IngredientDB) -> dict:
#     """Convert a database ingredient object into a backend ingredient object.

#     Args:
#         ingredient_db (IngredientDB): Ingredient database object.

#     Returns:
#         dict: Ingredient backend object.

#     """
#     return {
#         "id": ingredient_db.ingr_id,
#         "name": ingredient_db.name,
#         "image": ingredient_db.image,
#     }