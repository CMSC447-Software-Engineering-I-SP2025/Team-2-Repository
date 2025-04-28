"""Main file for this project (FastAPI version)."""

# Standard Libraries
from collections.abc import Generator
from json import loads as jsonloads
from pathlib import Path
from typing import Annotated, Any

# Custom Libraries
from data_classes import Recipe, Response, json_mapper
from db_models import (
    Base,
    IngredientDB,
    RecipeDB,
    db_to_ingredient,
    db_to_recipe,
    ingredient_to_db,
    recipe_to_db,
)

# External Libraries
from fastapi import Depends, FastAPI, HTTPException
from requests import Request
from requests import get as reqget
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from tomllib import loads as tomlloads


#
# DATABASE AND FASTAPI INIT
#
class DB:
    """Database connector for the application."""

    def __init__(self) -> None:
        """Initialize the database."""
        self.engine = create_engine(
            f"sqlite:///{(Path(__file__).resolve().parent.parent / 'assets' / 'database.db').as_posix()}",
        )
        Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)
        self.base_url = "https://api.spoonacular.com/recipes/complexSearch"
        self.api_key = tomlloads(
            (Path(__file__).parent.parent / "assets" / "config.toml").read_text(),
        )["apikey"]

db = DB()

def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session.

    Yields:
        SQLAlchemy Session object.

    """
    session = db.DBSession()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

# CORS
# origins = ["http://localhost:5173"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

#
# CORE BUSINESS LOGIC
#

@app.get("/recipes", response_model=dict)
def api_get_recipes(
    includeIngredients: str,
    excludeIngredients: str = "",
    cuisine: str = "",
    intolerances: str = "",
    diet: str = "",
) -> dict:
    """Search for recipes from Spoonacular API.

    Args:
        includeIngredients (str): Comma-separated list of ingredients to include.
        excludeIngredients (str, optional): Comma-separated list of ingredients to exclude.
        cuisine (str, optional): Type of cuisine to filter.
        intolerances (str, optional): Comma-separated list of intolerances.
        diet (str, optional): Type of diet to filter.

    Returns:
        Response: Recipes matching the search criteria.

    """
    params = {
        "includeIngredients": includeIngredients,
        "instructionsRequired": True,
        "addRecipeInformation": True,
        "addRecipeInstructions": True,
        "apiKey": db.api_key,
    }
    if excludeIngredients:
        params["excludeIngredients"] = excludeIngredients
    if cuisine:
        params["cuisine"] = cuisine
    if intolerances:
        params["intolerances"] = intolerances
    if diet:
        params["diet"] = diet

    try:

        return  json_mapper(json_data=jsonloads(reqget(url=Request(method="GET", url=db.base_url, params=params).prepare().url,timeout=5).text), data_class=Response).results


    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/saverecipe", response_model=str)
def api_save_recipe(
    recipe: dict,
    db_session: Annotated[Session, Depends(get_db)],
) -> str:
    """Save a recipe to the database.

    Args:
        recipe (dict): Recipe data to save.
        db_session (Session, optional): SQLAlchemy session dependency.

    Returns:
        str: "200" if successful.

    """
    try:
        recipe_db_class = recipe_to_db(recipe)
        db_session.add(recipe_db_class)
        db_session.commit()
        return "200"
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/deleterecipe", response_model=str)
def api_delete_recipe(
    recipe_id: int,
    db_session: Annotated[Session, Depends(get_db)],
) -> str:
    """Delete a recipe from the database by its ID.

    Args:
        recipe_id (int): ID of the recipe to delete.
        db_session (Session, optional): SQLAlchemy session dependency.

    Returns:
        str: "200" if successful.

    """
    try:
        db_session.query(RecipeDB).filter_by(id=recipe_id).delete()
        db_session.commit()
        return "200"
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/listrecipes", response_model=list[Any])
def api_list_recipes(
    db_session: Annotated[Session, Depends(get_db)],
) -> list[Any]:
    """List all saved recipes from the database.

    Args:
        db_session (Session, optional): SQLAlchemy session dependency.

    Returns:
        list[Any]: List of recipes.

    """
    try:
        return [db_to_recipe(recipe) for recipe in db_session.query(RecipeDB).all()]
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/addingredient", response_model=str)
def api_save_ingredient(
    ingredient: dict,
    db_session: Annotated[Session, Depends(get_db)],
) -> str:
    """Add an ingredient to the pantry.

    Args:
        ingredient (dict): Ingredient data to add.
        db_session (Session, optional): SQLAlchemy session dependency.

    Returns:
        str: "200" if successful.

    """
    try:
        ingredient_db_class = ingredient_to_db(ingredient)
        db_session.add(ingredient_db_class)
        db_session.commit()
        return "200"
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/removeingredient", response_model=str)
def api_delete_ingredient(
    ingredient_id: int,
    db_session: Annotated[Session, Depends(get_db)],
) -> str:
    """Remove an ingredient from the pantry by its ID.

    Args:
        ingredient_id (int): ID of the ingredient to remove.
        db_session (Session, optional): SQLAlchemy session dependency.

    Returns:
        str: "200" if successful.

    """
    try:
        db_session.query(IngredientDB).filter_by(id=ingredient_id).delete()
        db_session.commit()
        return "200"
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/listingredients", response_model=list[Any])
def api_list_ingredients(
    db_session: Annotated[Session, Depends(get_db)],
) -> list[Any]:
    """List all saved ingredients from the pantry.

    Args:
        db_session (Session, optional): SQLAlchemy session dependency.

    Returns:
        list[Any]: List of ingredients.

    """
    try:
        return [db_to_ingredient(ingr) for ingr in db_session.query(IngredientDB).all()]
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


#
# BEGIN PROGRAM EXECUTION
#

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8080, reload=True)

