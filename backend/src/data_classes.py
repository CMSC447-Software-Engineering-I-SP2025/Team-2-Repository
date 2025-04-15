from typing import Optional
from dataclasses import dataclass
from dacite import from_dict, Config

@dataclass
class Temperature:
    number: float
    unit: str

@dataclass
class Length:
    number: int
    unit: str

@dataclass
class Ingredient:
    id: int
    name: str
    localizedName: Optional[str]
    image: str

@dataclass
class Equipment:
    id: int
    name: str
    localizedName: str
    image: str
    temperature: Optional[Temperature] = None

@dataclass
class Step:
    number: int
    step: str
    ingredients: list[Ingredient]
    equipment: list[Equipment]
    length: Optional[Length]

@dataclass
class Instruction:
    name: str
    steps: list[Step]

@dataclass
class Recipe:
    id: int
    image: str
    title: str
    usedIngredientCount: Optional[int]
    missedIngredientCount: Optional[int]
    analyzedInstructions: Optional[list[Instruction]]

@dataclass
class Response:
    results: list[Recipe]


def json_mapper(json_data, data_class):

    return from_dict(
    data_class=data_class,
    data=json_data,
    config=Config(check_types=False, cast=[], strict=False)
    )