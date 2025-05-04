"""Data models for frontend <-> backend interaction."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Temperature:
    """Temperature for a step."""

    number: float
    unit: str

@dataclass
class Length:
    """Length of an action in a step."""

    number: int
    unit: str

@dataclass
class Ingredient:
    """Ingredient used in a step or held by the user."""

    id: int
    name: str
    localized_name: str | None
    image: str

@dataclass
class Equipment:
    """Represents a piece of equipment used in instruction."""

    id: int
    name: str
    localized_name: str
    image: str
    temperature: Temperature | None = None

@dataclass
class Step:
    """A single step in a recipe's instructions."""

    number: int
    step: str
    ingredients: list[Ingredient]
    equipment: list[Equipment]
    length: Length | None

@dataclass
class Instruction:
    """A recipe's analyzed instructions."""

    name: str
    steps: list[Step]

@dataclass
class Recipe:
    """A single recipe."""

    id: int
    image: str
    title: str
    used_ingredient_count: int | None
    missed_ingredient_count: int | None
    instructions: list[Instruction] | None

@dataclass
class Response:
    """Represents responses from spoonacular."""

    results: list[Recipe]



