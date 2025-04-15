from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import json


Base = declarative_base()

# Classes
class IngredientDB(Base):
    """SQLAlchemy model for ingredients table"""
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    localized_name = Column(String(100))
    image = Column(String(255))

class RecipeDB(Base):
    """SQLAlchemy model for recipes table"""
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    image = Column(String(255))
    used_ingredient_count = Column(Integer)
    missed_ingredient_count = Column(Integer)
    analyzed_instructions = Column(JSON)  # Stores list of Instruction dataclasses as JSON
    
    # Relationship (if you want direct access)
    ingredients = relationship("IngredientDB", secondary="recipe_ingredients")

# Association table for many-to-many relationship
class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'
    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), primary_key=True)


def recipe_to_db(recipe: dict) -> RecipeDB:
    return RecipeDB(
        id=recipe['id'],
        title=recipe['title'],
        image=recipe['image'],
        used_ingredient_count=recipe['usedIngredientCount'],
        missed_ingredient_count=recipe['missedIngredientCount'],
        analyzed_instructions=json.dumps(
            [{k: v for k, v in instr.items() if k != 'repr'} 
             for instr in recipe['analyzedInstructions'] or []]
            if recipe['analyzedInstructions'] is not None 
            else []
        )
    )

def db_to_recipe(recipe_db: dict) -> dict:
    """Convert SQLAlchemy model to Recipe dictionary"""
    return {
        'id': recipe_db.id,
        'title': recipe_db.title,
        'image': recipe_db.image,
        'usedIngredientCount': recipe_db.used_ingredient_count,
        'missedIngredientCount': recipe_db.missed_ingredient_count,
        'analyzedInstructions': [
            dict(instr) for instr in json.loads(recipe_db.analyzed_instructions)
        ]
    }


def ingredient_to_db(ingredient: dict) -> IngredientDB:
    """Convert Recipe to SQLAlchemy model."""
    return IngredientDB(
        id=ingredient['id'],
        name=ingredient['name'],
        localized_name=ingredient.get('localizedName', None),
        image=ingredient.get('image', None),
    )


def db_to_ingredient(ingredient_db: IngredientDB) -> dict:
    return {
        'id': ingredient_db.id,
        'name': ingredient_db.name,
        'localizedName': ingredient_db.localized_name, 
        'image': ingredient_db.image,
    }