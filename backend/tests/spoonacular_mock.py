# Mocks a spoonacular request of includeIngredients=sausage
mock_spoonacular_response = {
    "results": [
        {
            "id": 659581,
            "title": "Mock Scotch Eggs",
            "image": "https://img.spoonacular.com/recipes/659581-312x231.jpg",
            "servings": 8,
            "usedIngredientCount": 1,
            "missedIngredientCount": 2,
            "analyzedInstructions": [
                {
                    "name": "",
                    "steps": [
                        {
                            "number": 1,
                            "step": "Wrap sausage around egg",
                            "ingredients": [
                                {"id": 1129, "name": "hard boiled egg", "quantity": None, "image": "hard-boiled-egg.png"},
                                {"id": 18079, "name": "breadcrumbs", "quantity": None, "image": "breadcrumbs.jpg"}
                            ],
                            "equipment": [
                                {
                                    "id": 404727,
                                    "name": "baking sheet",
                                    "image": "https://spoonacular.com/cdn/equipment_100x100/baking-sheet.jpg",
                                    "temperature": None
                                }
                            ],
                            "length": {
                                "number": 20,
                                "unit": "minutes"
                            }
                        }
                    ]
                }
            ],
            "nutrition": {
                "nutrients": [
                    {"name": "Calories", "amount": 296.48, "unit": "kcal", "percentOfDailyNeeds": 14.82},
                    {"name": "Protein", "amount": 16.6, "unit": "g", "percentOfDailyNeeds": 33.19},
                    {"name": "Fat", "amount": 20.47, "unit": "g", "percentOfDailyNeeds": 31.48}
                ]
            }
        }
    ]
}