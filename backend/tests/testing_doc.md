# TODO
- Test User Routes
  - Login
  - Logout
  - LoginStatus
  - My-Account

- Test Authorized Routes (All require database usage)
  - save_recipe
  - delete_recipe
  - list_recipes
    - from database
  - save_ingredient
  - delete_ingredient
  - list_ingredients

- Generate test coverage report
- See if still need unit tests (testing models themselves)
## Test Cases
- Test both successful and unsuccessful


# Usage
`pytest -v -s`

Need to update pip by installing from requirements.txt

Coverage report
add in `--cov`

Can parameterize tests if necessary