"""Database data models."""
from sqlalchemy import JSON, Column, ForeignKey, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Classes
class UserDB(Base):
    """Table to hold users."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)


class IngredientDB(Base):
    """Ingredient DB table."""

    __tablename__ = "ingredients"

    ingr_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=True)
    unit = Column(String(100), nullable=True)
    image = Column(String(255))

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "ingr_id"),
    )

class RecipeDB(Base):
    """Recipe DB table."""


    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    image = Column(String(255))
    servings = Column(Integer, nullable=True)
    analyzed_instructions = Column(JSON)  # Stores list of Instruction dataclasses as JSON
    nutrition = Column(JSON) # Stores list of Nutrient dataclasses as JSON

    # Relationship (if you want direct access)
    # ingredients = relationship("IngredientDB", secondary="recipe_ingredients")
    ingredients = Column(JSON)

# Association table for many-to-many relationship
class RecipeIngredientDB(Base):
    """Association table for a many-to-many relationships.

    Args:
        Base (_type_): Base DB class.

    """

    __tablename__ = "recipe_ingredients"
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingr_id"), primary_key=True)
