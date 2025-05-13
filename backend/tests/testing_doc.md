`WARNING: ` Running tests will nuke the database (wipe it)
Need to update pip by installing from requirements.txt

# TODO


- See if still need unit tests (testing models themselves)
- FInish CI/CD so upon commit tests get ran
---

# Covered
- All authentication endpoints have been covered by tests
  - /register
  - /login
  - /logout
  - /loginstatus
  - /my-account
  - /recipes
    - Get query from spoonacular
- Test Authorized Routes (All require database usage)
  - save_recipe
  - delete_recipe
  - list_recipes
    - from database
  - save_ingredient
  - delete_ingredient
  - list_ingredients


# Usage
`pytest -v -s`

For generating a coverage report
` pytest -v -s --cov=backend/src --cov-report=term-missing`

# How it works
- I made a new tests folder
  - All tests are there
  - conftest.py
    - Essentially set-up/teardown before each test
  - query_api_test.py
    - Unauthenticated spoonacular query testing
  - authenticated_api_test.py
    - All authenticated recipe routes (save recipe, delete recipe, save ingredient, etc.)
  - user_routes_test.py
    - All authenticated routes related to user login/logout
