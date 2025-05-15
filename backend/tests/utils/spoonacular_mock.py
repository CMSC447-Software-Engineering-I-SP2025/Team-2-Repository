# Real spoonacular request from includeIngredient = potatoes.
# Replaced None, false, and true with python compliant ones
from backend.src.backend_data_models import Recipe, Instruction, Step, Ingredient, Nutrient, Nutrition

mock_raw_spoonacular_recipe = {
  "results": [
    {
      "id": 641122,
      "image": "https://img.spoonacular.com/recipes/641122-312x231.jpg",
      "imageType": "jpg",
      "title": "Curry Leaves Potato Chips",
      "readyInMinutes": 45,
      "servings": 3,
      "sourceUrl": "https://www.foodista.com/recipe/S6M8SF2T/curry-leaves-potato-chips",
      "vegetarian": True,
      "vegan": True,
      "glutenFree": True,
      "dairyFree": True,
      "veryHealthy": False,
      "cheap": False,
      "veryPopular": False,
      "sustainable": False,
      "lowFodmap": True,
      "weightWatcherSmartPoints": 5,
      "gaps": "no",
      "preparationMinutes": None,
      "cookingMinutes": None,
      "aggregateLikes": 4,
      "healthScore": 18,
      "creditsText": "Foodista.com – The Cooking Encyclopedia Everyone Can Edit",
      "license": "CC BY 3.0",
      "sourceName": "Foodista",
      "pricePerServing": 54.5,
      "extendedIngredients": [
        {
          "id": 10011355,
          "aisle": "Produce",
          "image": "red-potatoes.jpg",
          "consistency": "SOLID",
          "name": "potatoes - remove skin",
          "nameClean": "potatoes - remove skin",
          "original": "3 potatoes - remove skin, sliced thinly and soaked in ice water for 10-15 minutes.",
          "originalName": "potatoes - remove skin, sliced thinly and soaked in ice water for 10-15 minutes",
          "amount": 3,
          "unit": "",
          "meta": [
            "sliced",
            "for 10-15 minutes."
          ],
          "measures": {
            "us": {
              "amount": 3,
              "unitShort": "",
              "unitLong": ""
            },
            "metric": {
              "amount": 3,
              "unitShort": "",
              "unitLong": ""
            }
          }
        },
        {
          "id": 2009,
          "aisle": "Spices and Seasonings",
          "image": "chili-powder.jpg",
          "consistency": "SOLID",
          "name": "chili powder",
          "nameClean": "chili powder",
          "original": "1 tsp plain chili powder",
          "originalName": "plain chili powder",
          "amount": 1,
          "unit": "tsp",
          "meta": [
            "plain"
          ],
          "measures": {
            "us": {
              "amount": 1,
              "unitShort": "tsp",
              "unitLong": "teaspoon"
            },
            "metric": {
              "amount": 1,
              "unitShort": "tsp",
              "unitLong": "teaspoon"
            }
          }
        },
        {
          "id": 93604,
          "aisle": "Ethnic Foods",
          "image": "curry-leaves.jpg",
          "consistency": "SOLID",
          "name": "curry leaves",
          "nameClean": "curry leaves",
          "original": "3-4 sprigs curry leaves",
          "originalName": "curry leaves",
          "amount": 3,
          "unit": "sprigs",
          "meta": [],
          "measures": {
            "us": {
              "amount": 3,
              "unitShort": "sprigs",
              "unitLong": "sprigs"
            },
            "metric": {
              "amount": 3,
              "unitShort": "sprigs",
              "unitLong": "sprigs"
            }
          }
        },
        {
          "id": 2047,
          "aisle": "Spices and Seasonings",
          "image": "salt.jpg",
          "consistency": "SOLID",
          "name": "salt",
          "nameClean": "salt",
          "original": "Salt for taste",
          "originalName": "Salt for taste",
          "amount": 3,
          "unit": "servings",
          "meta": [
            "for taste"
          ],
          "measures": {
            "us": {
              "amount": 3,
              "unitShort": "servings",
              "unitLong": "servings"
            },
            "metric": {
              "amount": 3,
              "unitShort": "servings",
              "unitLong": "servings"
            }
          }
        },
        {
          "id": 4582,
          "aisle": "Oil, Vinegar, Salad Dressing",
          "image": "vegetable-oil.jpg",
          "consistency": "LIQUID",
          "name": "oil",
          "nameClean": "oil",
          "original": "Oil for frying",
          "originalName": "Oil for frying",
          "amount": 3,
          "unit": "servings",
          "meta": [
            "for frying"
          ],
          "measures": {
            "us": {
              "amount": 3,
              "unitShort": "servings",
              "unitLong": "servings"
            },
            "metric": {
              "amount": 3,
              "unitShort": "servings",
              "unitLong": "servings"
            }
          }
        }
      ],
      "nutrition": {
        "nutrients": [
          {
            "name": "Calories",
            "amount": 177.47,
            "unit": "kcal",
            "percentOfDailyNeeds": 8.87
          },
          {
            "name": "Fat",
            "amount": 3.24,
            "unit": "g",
            "percentOfDailyNeeds": 4.98
          },
          {
            "name": "Saturated Fat",
            "amount": 0.3,
            "unit": "g",
            "percentOfDailyNeeds": 1.89
          },
          {
            "name": "Carbohydrates",
            "amount": 34.5,
            "unit": "g",
            "percentOfDailyNeeds": 11.5
          },
          {
            "name": "Net Carbohydrates",
            "amount": 30.5,
            "unit": "g",
            "percentOfDailyNeeds": 11.09
          },
          {
            "name": "Sugar",
            "amount": 2.81,
            "unit": "g",
            "percentOfDailyNeeds": 3.12
          },
          {
            "name": "Cholesterol",
            "amount": 0,
            "unit": "mg",
            "percentOfDailyNeeds": 0
          },
          {
            "name": "Sodium",
            "amount": 246.89,
            "unit": "mg",
            "percentOfDailyNeeds": 10.73
          },
          {
            "name": "Alcohol",
            "amount": 0,
            "unit": "g",
            "percentOfDailyNeeds": 100
          },
          {
            "name": "Alcohol %",
            "amount": 0,
            "unit": "%",
            "percentOfDailyNeeds": 100
          },
          {
            "name": "Protein",
            "amount": 4.21,
            "unit": "g",
            "percentOfDailyNeeds": 8.42
          },
          {
            "name": "Vitamin B3",
            "amount": 25.55,
            "unit": "mg",
            "percentOfDailyNeeds": 127.76
          },
          {
            "name": "Vitamin C",
            "amount": 58.32,
            "unit": "mg",
            "percentOfDailyNeeds": 70.7
          },
          {
            "name": "Folate",
            "amount": 273.59,
            "unit": "µg",
            "percentOfDailyNeeds": 68.4
          },
          {
            "name": "Potassium",
            "amount": 986.74,
            "unit": "mg",
            "percentOfDailyNeeds": 28.19
          },
          {
            "name": "Vitamin B6",
            "amount": 0.38,
            "unit": "mg",
            "percentOfDailyNeeds": 19.05
          },
          {
            "name": "Fiber",
            "amount": 4,
            "unit": "g",
            "percentOfDailyNeeds": 15.99
          },
          {
            "name": "Manganese",
            "amount": 0.32,
            "unit": "mg",
            "percentOfDailyNeeds": 15.88
          },
          {
            "name": "Copper",
            "amount": 0.3,
            "unit": "mg",
            "percentOfDailyNeeds": 14.78
          },
          {
            "name": "Phosphorus",
            "amount": 133.2,
            "unit": "mg",
            "percentOfDailyNeeds": 13.32
          },
          {
            "name": "Magnesium",
            "amount": 48.65,
            "unit": "mg",
            "percentOfDailyNeeds": 12.16
          },
          {
            "name": "Vitamin B1",
            "amount": 0.18,
            "unit": "mg",
            "percentOfDailyNeeds": 11.71
          },
          {
            "name": "Iron",
            "amount": 1.72,
            "unit": "mg",
            "percentOfDailyNeeds": 9.56
          },
          {
            "name": "Vitamin K",
            "amount": 9.12,
            "unit": "µg",
            "percentOfDailyNeeds": 8.69
          },
          {
            "name": "Vitamin A",
            "amount": 357.36,
            "unit": "IU",
            "percentOfDailyNeeds": 7.15
          },
          {
            "name": "Vitamin B5",
            "amount": 0.6,
            "unit": "mg",
            "percentOfDailyNeeds": 6.02
          },
          {
            "name": "Vitamin E",
            "amount": 0.85,
            "unit": "mg",
            "percentOfDailyNeeds": 5.7
          },
          {
            "name": "Zinc",
            "amount": 0.74,
            "unit": "mg",
            "percentOfDailyNeeds": 4.96
          },
          {
            "name": "Vitamin B2",
            "amount": 0.08,
            "unit": "mg",
            "percentOfDailyNeeds": 4.51
          },
          {
            "name": "Calcium",
            "amount": 32.69,
            "unit": "mg",
            "percentOfDailyNeeds": 3.27
          },
          {
            "name": "Selenium",
            "amount": 1.25,
            "unit": "µg",
            "percentOfDailyNeeds": 1.78
          }
        ],
        "properties": [
          {
            "name": "Glycemic Index",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Glycemic Load",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Inflammation Score",
            "amount": -7,
            "unit": ""
          },
          {
            "name": "Nutrition Score",
            "amount": 18.339999893437263,
            "unit": "%"
          }
        ],
        "flavonoids": [
          {
            "name": "Cyanidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Petunidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Delphinidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Malvidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Pelargonidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Peonidin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Catechin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Epigallocatechin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Epicatechin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Epicatechin 3-gallate",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Epigallocatechin 3-gallate",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Theaflavin",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Thearubigins",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Eriodictyol",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Hesperetin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Naringenin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Apigenin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Luteolin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Isorhamnetin",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Kaempferol",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Myricetin",
            "amount": 0,
            "unit": "mg"
          },
          {
            "name": "Quercetin",
            "amount": 1.38,
            "unit": "mg"
          },
          {
            "name": "Theaflavin-3,3'-digallate",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Theaflavin-3'-gallate",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Theaflavin-3-gallate",
            "amount": 0,
            "unit": ""
          },
          {
            "name": "Gallocatechin",
            "amount": 0,
            "unit": "mg"
          }
        ],
        "ingredients": [
          {
            "id": 10011355,
            "name": "potatoes - remove skin",
            "amount": 1,
            "unit": "",
            "nutrients": [
              {
                "name": "Folic Acid",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Net Carbohydrates",
                "amount": 30.25,
                "unit": "g",
                "percentOfDailyNeeds": 11.09
              },
              {
                "name": "Vitamin K",
                "amount": 6.18,
                "unit": "µg",
                "percentOfDailyNeeds": 8.69
              },
              {
                "name": "Vitamin B12",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Calcium",
                "amount": 21.3,
                "unit": "mg",
                "percentOfDailyNeeds": 3.27
              },
              {
                "name": "Phosphorus",
                "amount": 129.93,
                "unit": "mg",
                "percentOfDailyNeeds": 13.32
              },
              {
                "name": "Manganese",
                "amount": 0.3,
                "unit": "mg",
                "percentOfDailyNeeds": 15.88
              },
              {
                "name": "Poly Unsaturated Fat",
                "amount": 0.13,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Sugar",
                "amount": 2.75,
                "unit": "g",
                "percentOfDailyNeeds": 3.12
              },
              {
                "name": "Sodium",
                "amount": 38.34,
                "unit": "mg",
                "percentOfDailyNeeds": 10.73
              },
              {
                "name": "Vitamin B6",
                "amount": 0.36,
                "unit": "mg",
                "percentOfDailyNeeds": 19.05
              },
              {
                "name": "Calories",
                "amount": 149.1,
                "unit": "kcal",
                "percentOfDailyNeeds": 8.87
              },
              {
                "name": "Magnesium",
                "amount": 46.86,
                "unit": "mg",
                "percentOfDailyNeeds": 12.16
              },
              {
                "name": "Lycopene",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Cholesterol",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fat",
                "amount": 0.3,
                "unit": "g",
                "percentOfDailyNeeds": 4.98
              },
              {
                "name": "Selenium",
                "amount": 1.06,
                "unit": "µg",
                "percentOfDailyNeeds": 1.78
              },
              {
                "name": "Vitamin B5",
                "amount": 0.59,
                "unit": "mg",
                "percentOfDailyNeeds": 6.02
              },
              {
                "name": "Vitamin D",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Iron",
                "amount": 1.55,
                "unit": "mg",
                "percentOfDailyNeeds": 9.56
              },
              {
                "name": "Vitamin A",
                "amount": 14.91,
                "unit": "IU",
                "percentOfDailyNeeds": 7.15
              },
              {
                "name": "Alcohol",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 100
              },
              {
                "name": "Folate",
                "amount": 38.34,
                "unit": "µg",
                "percentOfDailyNeeds": 68.4
              },
              {
                "name": "Mono Unsaturated Fat",
                "amount": 0.01,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Vitamin E",
                "amount": 0.02,
                "unit": "mg",
                "percentOfDailyNeeds": 5.7
              },
              {
                "name": "Copper",
                "amount": 0.29,
                "unit": "mg",
                "percentOfDailyNeeds": 14.78
              },
              {
                "name": "Choline",
                "amount": 34.93,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Caffeine",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fiber",
                "amount": 3.62,
                "unit": "g",
                "percentOfDailyNeeds": 15.99
              },
              {
                "name": "Vitamin B2",
                "amount": 0.07,
                "unit": "mg",
                "percentOfDailyNeeds": 4.51
              },
              {
                "name": "Vitamin B3",
                "amount": 2.45,
                "unit": "mg",
                "percentOfDailyNeeds": 127.76
              },
              {
                "name": "Protein",
                "amount": 4.03,
                "unit": "g",
                "percentOfDailyNeeds": 8.42
              },
              {
                "name": "Vitamin C",
                "amount": 18.32,
                "unit": "mg",
                "percentOfDailyNeeds": 70.7
              },
              {
                "name": "Saturated Fat",
                "amount": 0.07,
                "unit": "g",
                "percentOfDailyNeeds": 1.89
              },
              {
                "name": "Vitamin B1",
                "amount": 0.17,
                "unit": "mg",
                "percentOfDailyNeeds": 11.71
              },
              {
                "name": "Carbohydrates",
                "amount": 33.87,
                "unit": "g",
                "percentOfDailyNeeds": 11.5
              },
              {
                "name": "Potassium",
                "amount": 969.15,
                "unit": "mg",
                "percentOfDailyNeeds": 28.19
              },
              {
                "name": "Zinc",
                "amount": 0.7,
                "unit": "mg",
                "percentOfDailyNeeds": 4.96
              }
            ]
          },
          {
            "id": 2009,
            "name": "chili powder",
            "amount": 0.33,
            "unit": "tsp",
            "nutrients": [
              {
                "name": "Folic Acid",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Net Carbohydrates",
                "amount": 0.13,
                "unit": "g",
                "percentOfDailyNeeds": 11.09
              },
              {
                "name": "Trans Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 110.6
              },
              {
                "name": "Vitamin K",
                "amount": 0.95,
                "unit": "µg",
                "percentOfDailyNeeds": 8.69
              },
              {
                "name": "Vitamin B12",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Calcium",
                "amount": 2.97,
                "unit": "mg",
                "percentOfDailyNeeds": 3.27
              },
              {
                "name": "Phosphorus",
                "amount": 2.7,
                "unit": "mg",
                "percentOfDailyNeeds": 13.32
              },
              {
                "name": "Manganese",
                "amount": 0.02,
                "unit": "mg",
                "percentOfDailyNeeds": 15.88
              },
              {
                "name": "Poly Unsaturated Fat",
                "amount": 0.07,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Sugar",
                "amount": 0.06,
                "unit": "g",
                "percentOfDailyNeeds": 3.12
              },
              {
                "name": "Sodium",
                "amount": 14.76,
                "unit": "mg",
                "percentOfDailyNeeds": 10.73
              },
              {
                "name": "Vitamin B6",
                "amount": 0.02,
                "unit": "mg",
                "percentOfDailyNeeds": 19.05
              },
              {
                "name": "Calories",
                "amount": 2.54,
                "unit": "kcal",
                "percentOfDailyNeeds": 8.87
              },
              {
                "name": "Magnesium",
                "amount": 1.34,
                "unit": "mg",
                "percentOfDailyNeeds": 12.16
              },
              {
                "name": "Lycopene",
                "amount": 0.19,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Cholesterol",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fat",
                "amount": 0.13,
                "unit": "g",
                "percentOfDailyNeeds": 4.98
              },
              {
                "name": "Selenium",
                "amount": 0.18,
                "unit": "µg",
                "percentOfDailyNeeds": 1.78
              },
              {
                "name": "Vitamin B5",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 6.02
              },
              {
                "name": "Vitamin D",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Iron",
                "amount": 0.16,
                "unit": "mg",
                "percentOfDailyNeeds": 9.56
              },
              {
                "name": "Vitamin A",
                "amount": 266.85,
                "unit": "IU",
                "percentOfDailyNeeds": 7.15
              },
              {
                "name": "Alcohol",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 100
              },
              {
                "name": "Folate",
                "amount": 0.25,
                "unit": "µg",
                "percentOfDailyNeeds": 68.4
              },
              {
                "name": "Mono Unsaturated Fat",
                "amount": 0.03,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Vitamin E",
                "amount": 0.34,
                "unit": "mg",
                "percentOfDailyNeeds": 5.7
              },
              {
                "name": "Copper",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 14.78
              },
              {
                "name": "Choline",
                "amount": 0.6,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Caffeine",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fiber",
                "amount": 0.31,
                "unit": "g",
                "percentOfDailyNeeds": 15.99
              },
              {
                "name": "Vitamin B2",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 4.51
              },
              {
                "name": "Vitamin B3",
                "amount": 0.1,
                "unit": "mg",
                "percentOfDailyNeeds": 127.76
              },
              {
                "name": "Protein",
                "amount": 0.12,
                "unit": "g",
                "percentOfDailyNeeds": 8.42
              },
              {
                "name": "Vitamin C",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 70.7
              },
              {
                "name": "Saturated Fat",
                "amount": 0.02,
                "unit": "g",
                "percentOfDailyNeeds": 1.89
              },
              {
                "name": "Vitamin B1",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 11.71
              },
              {
                "name": "Carbohydrates",
                "amount": 0.45,
                "unit": "g",
                "percentOfDailyNeeds": 11.5
              },
              {
                "name": "Potassium",
                "amount": 17.55,
                "unit": "mg",
                "percentOfDailyNeeds": 28.19
              },
              {
                "name": "Zinc",
                "amount": 0.04,
                "unit": "mg",
                "percentOfDailyNeeds": 4.96
              }
            ]
          },
          {
            "id": 93604,
            "name": "curry leaves",
            "amount": 1,
            "unit": "sprigs",
            "nutrients": [
              {
                "name": "Net Carbohydrates",
                "amount": 0.12,
                "unit": "g",
                "percentOfDailyNeeds": 11.09
              },
              {
                "name": "Trans Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 110.6
              },
              {
                "name": "Vitamin K",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 8.69
              },
              {
                "name": "Vitamin B12",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Calcium",
                "amount": 8.3,
                "unit": "mg",
                "percentOfDailyNeeds": 3.27
              },
              {
                "name": "Phosphorus",
                "amount": 0.57,
                "unit": "mg",
                "percentOfDailyNeeds": 13.32
              },
              {
                "name": "Manganese",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 15.88
              },
              {
                "name": "Poly Unsaturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fluoride",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Sugar",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 3.12
              },
              {
                "name": "Sodium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 10.73
              },
              {
                "name": "Vitamin B6",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 19.05
              },
              {
                "name": "Calories",
                "amount": 1.08,
                "unit": "kcal",
                "percentOfDailyNeeds": 8.87
              },
              {
                "name": "Magnesium",
                "amount": 0.44,
                "unit": "mg",
                "percentOfDailyNeeds": 12.16
              },
              {
                "name": "Cholesterol",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fat",
                "amount": 0.01,
                "unit": "g",
                "percentOfDailyNeeds": 4.98
              },
              {
                "name": "Selenium",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 1.78
              },
              {
                "name": "Vitamin B5",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 6.02
              },
              {
                "name": "Vitamin D",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Iron",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 9.56
              },
              {
                "name": "Vitamin A",
                "amount": 75.6,
                "unit": "IU",
                "percentOfDailyNeeds": 7.15
              },
              {
                "name": "Alcohol",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 100
              },
              {
                "name": "Folate",
                "amount": 235,
                "unit": "µg",
                "percentOfDailyNeeds": 68.4
              },
              {
                "name": "Mono Unsaturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Vitamin E",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 5.7
              },
              {
                "name": "Copper",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 14.78
              },
              {
                "name": "Caffeine",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fiber",
                "amount": 0.06,
                "unit": "g",
                "percentOfDailyNeeds": 15.99
              },
              {
                "name": "Vitamin B2",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.51
              },
              {
                "name": "Vitamin B3",
                "amount": 23,
                "unit": "mg",
                "percentOfDailyNeeds": 127.76
              },
              {
                "name": "Protein",
                "amount": 0.06,
                "unit": "g",
                "percentOfDailyNeeds": 8.42
              },
              {
                "name": "Vitamin C",
                "amount": 40,
                "unit": "mg",
                "percentOfDailyNeeds": 70.7
              },
              {
                "name": "Saturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 1.89
              },
              {
                "name": "Vitamin B1",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 11.71
              },
              {
                "name": "Carbohydrates",
                "amount": 0.19,
                "unit": "g",
                "percentOfDailyNeeds": 11.5
              },
              {
                "name": "Potassium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 28.19
              },
              {
                "name": "Zinc",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.96
              }
            ]
          },
          {
            "id": 2047,
            "name": "salt",
            "amount": 1,
            "unit": "servings",
            "nutrients": [
              {
                "name": "Folic Acid",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Net Carbohydrates",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 11.09
              },
              {
                "name": "Vitamin K",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 8.69
              },
              {
                "name": "Vitamin B12",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Calcium",
                "amount": 0.12,
                "unit": "mg",
                "percentOfDailyNeeds": 3.27
              },
              {
                "name": "Phosphorus",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 13.32
              },
              {
                "name": "Manganese",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 15.88
              },
              {
                "name": "Poly Unsaturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fluoride",
                "amount": 0.01,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Sugar",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 3.12
              },
              {
                "name": "Sodium",
                "amount": 193.79,
                "unit": "mg",
                "percentOfDailyNeeds": 10.73
              },
              {
                "name": "Vitamin B6",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 19.05
              },
              {
                "name": "Calories",
                "amount": 0,
                "unit": "kcal",
                "percentOfDailyNeeds": 8.87
              },
              {
                "name": "Magnesium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 12.16
              },
              {
                "name": "Lycopene",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Cholesterol",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 4.98
              },
              {
                "name": "Selenium",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 1.78
              },
              {
                "name": "Vitamin B5",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 6.02
              },
              {
                "name": "Vitamin D",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Iron",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 9.56
              },
              {
                "name": "Vitamin A",
                "amount": 0,
                "unit": "IU",
                "percentOfDailyNeeds": 7.15
              },
              {
                "name": "Alcohol",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 100
              },
              {
                "name": "Folate",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 68.4
              },
              {
                "name": "Mono Unsaturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Vitamin E",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 5.7
              },
              {
                "name": "Copper",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 14.78
              },
              {
                "name": "Choline",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Caffeine",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fiber",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 15.99
              },
              {
                "name": "Vitamin B2",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.51
              },
              {
                "name": "Vitamin B3",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 127.76
              },
              {
                "name": "Protein",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 8.42
              },
              {
                "name": "Vitamin C",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 70.7
              },
              {
                "name": "Saturated Fat",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 1.89
              },
              {
                "name": "Vitamin B1",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 11.71
              },
              {
                "name": "Carbohydrates",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 11.5
              },
              {
                "name": "Potassium",
                "amount": 0.04,
                "unit": "mg",
                "percentOfDailyNeeds": 28.19
              },
              {
                "name": "Zinc",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.96
              }
            ]
          },
          {
            "id": 4582,
            "name": "oil",
            "amount": 1,
            "unit": "servings",
            "nutrients": [
              {
                "name": "Folic Acid",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Net Carbohydrates",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 11.09
              },
              {
                "name": "Trans Fat",
                "amount": 0.06,
                "unit": "g",
                "percentOfDailyNeeds": 110.6
              },
              {
                "name": "Vitamin K",
                "amount": 9.98,
                "unit": "µg",
                "percentOfDailyNeeds": 8.69
              },
              {
                "name": "Vitamin B12",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Calcium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 3.27
              },
              {
                "name": "Phosphorus",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 13.32
              },
              {
                "name": "Manganese",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 15.88
              },
              {
                "name": "Poly Unsaturated Fat",
                "amount": 3.93,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Sugar",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 3.12
              },
              {
                "name": "Sodium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 10.73
              },
              {
                "name": "Vitamin B6",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 19.05
              },
              {
                "name": "Calories",
                "amount": 123.76,
                "unit": "kcal",
                "percentOfDailyNeeds": 8.87
              },
              {
                "name": "Magnesium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 12.16
              },
              {
                "name": "Lycopene",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Cholesterol",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fat",
                "amount": 14,
                "unit": "g",
                "percentOfDailyNeeds": 4.98
              },
              {
                "name": "Selenium",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 1.78
              },
              {
                "name": "Vitamin B5",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 6.02
              },
              {
                "name": "Vitamin D",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Iron",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 9.56
              },
              {
                "name": "Vitamin A",
                "amount": 0,
                "unit": "IU",
                "percentOfDailyNeeds": 7.15
              },
              {
                "name": "Alcohol",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 100
              },
              {
                "name": "Folate",
                "amount": 0,
                "unit": "µg",
                "percentOfDailyNeeds": 68.4
              },
              {
                "name": "Mono Unsaturated Fat",
                "amount": 8.86,
                "unit": "g",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Vitamin E",
                "amount": 2.45,
                "unit": "mg",
                "percentOfDailyNeeds": 5.7
              },
              {
                "name": "Copper",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 14.78
              },
              {
                "name": "Choline",
                "amount": 0.03,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Caffeine",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 0
              },
              {
                "name": "Fiber",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 15.99
              },
              {
                "name": "Vitamin B2",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.51
              },
              {
                "name": "Vitamin B3",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 127.76
              },
              {
                "name": "Protein",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 8.42
              },
              {
                "name": "Vitamin C",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 70.7
              },
              {
                "name": "Saturated Fat",
                "amount": 1.03,
                "unit": "g",
                "percentOfDailyNeeds": 1.89
              },
              {
                "name": "Vitamin B1",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 11.71
              },
              {
                "name": "Carbohydrates",
                "amount": 0,
                "unit": "g",
                "percentOfDailyNeeds": 11.5
              },
              {
                "name": "Potassium",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 28.19
              },
              {
                "name": "Zinc",
                "amount": 0,
                "unit": "mg",
                "percentOfDailyNeeds": 4.96
              }
            ]
          }
        ],
        "caloricBreakdown": {
          "percentProtein": 9.15,
          "percentFat": 15.83,
          "percentCarbs": 75.02
        },
        "weightPerServing": {
          "amount": 229,
          "unit": "g"
        }
      },
      "summary": "Curry Leaves Potato Chips requires approximately <b>45 minutes</b> from start to finish. This recipe serves 3 and costs 55 cents per serving. One portion of this dish contains around <b>4g of protein</b>, <b>3g of fat</b>, and a total of <b>177 calories</b>. 4 people were glad they tried this recipe. If you have oil, chili powder, salt, and a few other ingredients on hand, you can make it. It is brought to you by Foodista. Not a lot of people really liked this side dish. This recipe is typical of American cuisine. It is a good option if you're following a <b>gluten free, dairy free, lacto ovo vegetarian, and fodmap friendly</b> diet. All things considered, we decided this recipe <b>deserves a spoonacular score of 92%</b>. This score is outstanding. Users who liked this recipe also liked <a href=\"https://spoonacular.com/recipes/chicken-stir-fry-with-potato-cashews-and-curry-leaves-202216\">Chicken Stir Fry with Potato, Cashews, and Curry Leaves</a>, <a href=\"https://spoonacular.com/recipes/yam-leaves-stir-fried-sweet-potato-leaves-960798\">Yam Leaves, Stir-Fried Sweet Potato Leaves</a>, and <a href=\"https://spoonacular.com/recipes/curry-leaves-chutney-how-to-make-curry-leaves-chutney-487613\">curry leaves chutney , how to make curry leaves chutney</a>.",
      "cuisines": [
        "American"
      ],
      "dishTypes": [
        "side dish"
      ],
      "diets": [
        "gluten free",
        "dairy free",
        "lacto ovo vegetarian",
        "fodmap friendly",
        "whole 30",
        "vegan"
      ],
      "occasions": [],
      "analyzedInstructions": [
        {
          "name": "",
          "steps": [
            {
              "number": 1,
              "step": "Wipe/pat dry potatoes.",
              "ingredients": [
                {
                  "id": 11352,
                  "name": "potato",
                  "localizedName": "potato",
                  "image": "potatoes-yukon-gold.png"
                }
              ],
              "equipment": []
            },
            {
              "number": 2,
              "step": "Mix in chili powder and salt.",
              "ingredients": [
                {
                  "id": 2009,
                  "name": "chili powder",
                  "localizedName": "chili powder",
                  "image": "chili-powder.jpg"
                },
                {
                  "id": 2047,
                  "name": "salt",
                  "localizedName": "salt",
                  "image": "salt.jpg"
                }
              ],
              "equipment": []
            },
            {
              "number": 3,
              "step": "Heat oil and fry in batches till crunchy and crispy.",
              "ingredients": [
                {
                  "id": 4582,
                  "name": "cooking oil",
                  "localizedName": "cooking oil",
                  "image": "vegetable-oil.jpg"
                }
              ],
              "equipment": []
            },
            {
              "number": 4,
              "step": "Remove and keep aside.",
              "ingredients": [],
              "equipment": []
            },
            {
              "number": 5,
              "step": "In the same oil, fry curry leaves till crispy too.",
              "ingredients": [
                {
                  "id": 93604,
                  "name": "curry leaves",
                  "localizedName": "curry leaves",
                  "image": "curry-leaves.jpg"
                },
                {
                  "id": 4582,
                  "name": "cooking oil",
                  "localizedName": "cooking oil",
                  "image": "vegetable-oil.jpg"
                }
              ],
              "equipment": []
            },
            {
              "number": 6,
              "step": "Scoop out and add over chips.",
              "ingredients": [
                {
                  "id": 11408,
                  "name": "french fries",
                  "localizedName": "french fries",
                  "image": "french-fries-isolated.jpg"
                }
              ],
              "equipment": []
            },
            {
              "number": 7,
              "step": "Crush and toss the leaves with the chips.",
              "ingredients": [
                {
                  "id": 11408,
                  "name": "french fries",
                  "localizedName": "french fries",
                  "image": "french-fries-isolated.jpg"
                }
              ],
              "equipment": []
            }
          ]
        }
      ],
      "spoonacularScore": 70.99125671386719,
      "spoonacularSourceUrl": "https://spoonacular.com/curry-leaves-potato-chips-641122",
      "usedIngredientCount": 1,
      "missedIngredientCount": 2,
      "likes": 0,
      "missedIngredients": [
        {
          "id": 2009,
          "amount": 1,
          "unit": "tsp",
          "unitLong": "teaspoon",
          "unitShort": "tsp",
          "aisle": "Spices and Seasonings",
          "name": "chili powder",
          "original": "1 tsp plain chili powder",
          "originalName": "plain chili powder",
          "meta": [
            "plain"
          ],
          "extendedName": "plain chili powder",
          "image": "https://img.spoonacular.com/ingredients_100x100/chili-powder.jpg"
        },
        {
          "id": 93604,
          "amount": 3,
          "unit": "sprigs",
          "unitLong": "sprigs",
          "unitShort": "sprigs",
          "aisle": "Ethnic Foods",
          "name": "curry leaves",
          "original": "3-4 sprigs curry leaves",
          "originalName": "curry leaves",
          "meta": [],
          "image": "https://img.spoonacular.com/ingredients_100x100/curry-leaves.jpg"
        }
      ],
      "usedIngredients": [
        {
          "id": 10011355,
          "amount": 3,
          "unit": "",
          "unitLong": "",
          "unitShort": "",
          "aisle": "Produce",
          "name": "potatoes - remove skin",
          "original": "3 potatoes - remove skin, sliced thinly and soaked in ice water for 10-15 minutes.",
          "originalName": "potatoes - remove skin, sliced thinly and soaked in ice water for 10-15 minutes",
          "meta": [
            "sliced",
            "for 10-15 minutes."
          ],
          "image": "https://img.spoonacular.com/ingredients_100x100/red-potatoes.jpg"
        }
      ],
      "unusedIngredients": []
    }
  ],
  "offset": 0,
  "number": 1,
  "totalResults": 243
}

mock_formatted_spoonacular_recipe = {
  "analyzedInstructions": [
    {
      "name": "",
      "steps": [
        {
          "equipment": [],
          "ingredients": [
            {
              "id": 11352,
              "image": "potatoes-yukon-gold.png",
              "name": "potato",
              "quantity": None,
              "unit": None
            }
          ],
          "length": None,
          "number": 1,
          "step": "Wipe/pat dry potatoes."
        },
        {
          "equipment": [],
          "ingredients": [
            {
              "id": 2009,
              "image": "chili-powder.jpg",
              "name": "chili powder",
              "quantity": None,
              "unit": None
            },
            {
              "id": 2047,
              "image": "salt.jpg",
              "name": "salt",
              "quantity": None,
              "unit": None
            }
          ],
          "length": None,
          "number": 2,
          "step": "Mix in chili powder and salt."
        },
        {
          "equipment": [],
          "ingredients": [
            {
              "id": 4582,
              "image": "vegetable-oil.jpg",
              "name": "cooking oil",
              "quantity": None,
              "unit": None
            }
          ],
          "length": None,
          "number": 3,
          "step": "Heat oil and fry in batches till crunchy and crispy."
        },
        {
          "equipment": [],
          "ingredients": [],
          "length": None,
          "number": 4,
          "step": "Remove and keep aside."
        },
        {
          "equipment": [],
          "ingredients": [
            {
              "id": 93604,
              "image": "curry-leaves.jpg",
              "name": "curry leaves",
              "quantity": None,
              "unit": None
            },
            {
              "id": 4582,
              "image": "vegetable-oil.jpg",
              "name": "cooking oil",
              "quantity": None,
              "unit": None
            }
          ],
          "length": None,
          "number": 5,
          "step": "In the same oil, fry curry leaves till crispy too."
        },
        {
          "equipment": [],
          "ingredients": [
            {
              "id": 11408,
              "image": "french-fries-isolated.jpg",
              "name": "french fries",
              "quantity": None,
              "unit": None
            }
          ],
          "length": None,
          "number": 6,
          "step": "Scoop out and add over chips."
        },
        {
          "equipment": [],
          "ingredients": [
            {
              "id": 11408,
              "image": "french-fries-isolated.jpg",
              "name": "french fries",
              "quantity": None,
              "unit": None
            }
          ],
          "length": None,
          "number": 7,
          "step": "Crush and toss the leaves with the chips."
        }
      ]
    }
  ],
  "id": 641122,
  "image": "https://img.spoonacular.com/recipes/641122-312x231.jpg",
  "missedIngredientCount": 2,
  "nutrition": {
    "nutrients": [
      { "amount": 177.47, "name": "Calories", "percentOfDailyNeeds": 8.87, "unit": "kcal" },
      { "amount": 3.24, "name": "Fat", "percentOfDailyNeeds": 4.98, "unit": "g" },
      { "amount": 0.3, "name": "Saturated Fat", "percentOfDailyNeeds": 1.89, "unit": "g" },
      { "amount": 34.5, "name": "Carbohydrates", "percentOfDailyNeeds": 11.5, "unit": "g" },
      { "amount": 30.5, "name": "Net Carbohydrates", "percentOfDailyNeeds": 11.09, "unit": "g" },
      { "amount": 2.81, "name": "Sugar", "percentOfDailyNeeds": 3.12, "unit": "g" },
      { "amount": 0, "name": "Cholesterol", "percentOfDailyNeeds": 0, "unit": "mg" },
      { "amount": 246.89, "name": "Sodium", "percentOfDailyNeeds": 10.73, "unit": "mg" },
      { "amount": 0, "name": "Alcohol", "percentOfDailyNeeds": 100, "unit": "g" },
      { "amount": 0, "name": "Alcohol %", "percentOfDailyNeeds": 100, "unit": "%" },
      { "amount": 4.21, "name": "Protein", "percentOfDailyNeeds": 8.42, "unit": "g" },
      { "amount": 25.55, "name": "Vitamin B3", "percentOfDailyNeeds": 127.76, "unit": "mg" },
      { "amount": 58.32, "name": "Vitamin C", "percentOfDailyNeeds": 70.7, "unit": "mg" },
      { "amount": 273.59, "name": "Folate", "percentOfDailyNeeds": 68.4, "unit": "µg" },
      { "amount": 986.74, "name": "Potassium", "percentOfDailyNeeds": 28.19, "unit": "mg" },
      { "amount": 0.38, "name": "Vitamin B6", "percentOfDailyNeeds": 19.05, "unit": "mg" },
      { "amount": 4, "name": "Fiber", "percentOfDailyNeeds": 15.99, "unit": "g" },
      { "amount": 0.32, "name": "Manganese", "percentOfDailyNeeds": 15.88, "unit": "mg" },
      { "amount": 0.3, "name": "Copper", "percentOfDailyNeeds": 14.78, "unit": "mg" },
      { "amount": 133.2, "name": "Phosphorus", "percentOfDailyNeeds": 13.32, "unit": "mg" },
      { "amount": 48.65, "name": "Magnesium", "percentOfDailyNeeds": 12.16, "unit": "mg" },
      { "amount": 0.18, "name": "Vitamin B1", "percentOfDailyNeeds": 11.71, "unit": "mg" },
      { "amount": 1.72, "name": "Iron", "percentOfDailyNeeds": 9.56, "unit": "mg" },
      { "amount": 9.12, "name": "Vitamin K", "percentOfDailyNeeds": 8.69, "unit": "µg" },
      { "amount": 357.36, "name": "Vitamin A", "percentOfDailyNeeds": 7.15, "unit": "IU" },
      { "amount": 0.6, "name": "Vitamin B5", "percentOfDailyNeeds": 6.02, "unit": "mg" },
      { "amount": 0.85, "name": "Vitamin E", "percentOfDailyNeeds": 5.7, "unit": "mg" },
      { "amount": 0.74, "name": "Zinc", "percentOfDailyNeeds": 4.96, "unit": "mg" },
      { "amount": 0.08, "name": "Vitamin B2", "percentOfDailyNeeds": 4.51, "unit": "mg" },
      { "amount": 32.69, "name": "Calcium", "percentOfDailyNeeds": 3.27, "unit": "mg" },
      { "amount": 1.25, "name": "Selenium", "percentOfDailyNeeds": 1.78, "unit": "µg" }
    ]
  },
  "servings": 3,
  "title": "Curry Leaves Potato Chips",
  "usedIngredientCount": 1
}

mock_spoonacular_ingredient = {
    "id": 18079, "name": "breadcrumbs", "image": "breadcrumbs.jpg"
}