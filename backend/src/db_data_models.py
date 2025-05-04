"""Database data models."""
from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Classes
class UserDB(Base):
    """User table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_path = Column(String(200), nullable=False)
    password_reset_hash = Column(String(200), nullable=False)


class IngredientDB(Base):
    """Ingredient DB table."""

    __tablename__ = "ingredients"

    ingr_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    localized_name = Column(String(100))
    image = Column(String(255))

class RecipeDB(Base):
    """Recipe DB table."""

    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    image = Column(String(255))
    used_ingredient_count = Column(Integer)
    missed_ingredient_count = Column(Integer)
    analyzed_instructions = Column(JSON)  # Stores list of Instruction dataclasses as JSON

    # Relationship (if you want direct access)
    ingredients = relationship("IngredientDB", secondary="recipe_ingredients")

# # Association table for many-to-many relationship
# class RecipeIngredientDB(Base):
#     """Association table for a many-to-many relationships.

#     Args:
#         Base (_type_): Base DB class.

#     """

#     __tablename__ = "recipe_ingredients"
#     recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
#     ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
