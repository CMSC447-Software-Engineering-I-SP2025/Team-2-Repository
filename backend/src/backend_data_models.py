"""Data classe for frontend <-> backend interaction."""
from __future__ import annotations

from dataclasses import dataclass
from dacite import Config, from_dict


@dataclass
class Temperature:
    """Temperature dataclass.

    Attributes:
        number (float): The temperature value.
        unit (str): The unit of temperature (e.g., 'C', 'F').

    """

    number: float
    unit: str


@dataclass
class Length:
    """Length dataclass.

    Attributes:
        number (int): The length or duration value.
        unit (str): The unit of length or duration (e.g., 'minutes', 'seconds').

    """

    number: int
    unit: str


@dataclass
class Ingredient:
    """Ingredient dataclass.

    Attributes:
        id (int): Unique identifier for the ingredient.
        name (str): Name of the ingredient.
        image (str): URL or path to an image of the ingredient.

    """

    id: int
    name: str
    quantity: int | None
    unit: str | None
    image: str


@dataclass
class Equipment:
    """Equipment dataclass.

    Attributes:
        id (int): Unique identifier for the equipment.
        name (str): Name of the equipment.
        image (str): URL or path to an image of the equipment.
        temperature (Temperature | None): Optional temperature setting for the equipment.

    """

    id: int
    name: str
    image: str
    temperature: Temperature | None = None


@dataclass
class Step:
    """Step dataclass.

    Represents a single step in a recipe instruction.

    Attributes:
        number (int): The step number in the instruction sequence.
        step (str): Description of the step.
        ingredients (list[Ingredient]): List of ingredients used in this step.
        equipment (list[Equipment]): List of equipment needed for this step.
        length (Length | None): Optional length or duration for the step.

    """

    number: int
    step: str
    ingredients: list[Ingredient]
    equipment: list[Equipment]
    length: Length | None


@dataclass
class Instruction:
    """Instruction dataclass.

    Represents a set of steps under a named instruction group.

    Attributes:
        name (str): Name of the instruction group (e.g., 'Main', 'Sauce').
        steps (list[Step]): List of steps for this instruction group.

    """

    name: str
    steps: list[Step]

@dataclass
class Nutrient:
    """Nutrient dataclass.

    Represents quantity of a single nutrient in a recipe

    Attributes:
        name (str): Name of the nutrient (e.g., 'Calories', 'Vitamin D')
        amount (float): How much of the ingredient is in the recipe.
        unit (str): The measurement unit associated with the amount.
        percentOfDailyNeeds (float): Amount of nutrient in recipe / Recommended daily amount

    """

    name: str
    amount: float
    unit: str
    percentOfDailyNeeds: float



@dataclass
class Nutrition:
    """Nutrient dataclass.

    Represents a collection of a nutritional information about a recipe.
    Omits the properties, flavonoids, and ingredients fields of a Spoonacular Nutrition object.

    Attributes:
        nutrients(list[Nutrient]): A list of nutrient quantity objects

    """

    nutrients: list[Nutrient]

@dataclass
class Recipe:
    """Recipe dataclass.

    Represents a complete recipe with metadata and instructions.

    Attributes:
        id (int): Unique identifier for the recipe.
        image (str): URL or path to an image of the recipe.
        title (str): Title of the recipe.
        servings (int): Number of servings.
        usedIngredientCount (int | None): Number of used ingredients (if applicable).
        missedIngredientCount (int | None): Number of missed ingredients (if applicable).
        analyzedInstructions (list[Instruction] | None): Analyzed instructions for the recipe.
        nutrition (Nutrition | None): Nutritional information about the recipe.

    """

    id: int
    image: str
    title: str
    servings: int
    usedIngredientCount: int | None
    missedIngredientCount: int | None
    analyzedInstructions: list[Instruction] | None
    nutrition: Nutrition | None

@dataclass
class Response:
    """Response dataclass.

    Represents a response containing a list of recipes.

    Attributes:
        results (list[Recipe]): List of recipe objects in the response.

    """

    results: list[Recipe]