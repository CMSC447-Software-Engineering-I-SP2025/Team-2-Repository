# Team-2-Repository

# Overview
This is our recipe app.

# Usage (Windows)
1. Clone the git repo.
2. Download and install [nodeJS](https://nodejs.org/en/download/). 
2. In a terminal in `recipe-app` run `npm install`.
3. To start the frontend, run `npm run dev` to start the dev frontend.
  - Hit `q + Enter`, or run `npx kill-port 5173` to stop the frontend.
5. To start the backend, run `./mvnw clean package`, then run `java -jar .\target\CookbookApp-maker-0.0.1-SNAPSHOT.jar`

# Backend
---
## How to use
- Start RecipeMakerApplication
  - Either use IDE or mvnw wrapper
    - ./mvnw spring-boot:run
- Navigate to `localhost:8080/recipes?includeIngredients=x,y,z?excludeIngredients=x?cuisine=x?intolerances=x?diet=x`
  - excludedIngredients, cuisine, and intolerances are all optional
  - elements passed into cuisine are treated as an OR list
  - elements passed into diet
    - `|` between elements mean OR
    - `,` between elements mean AND
  - Example Query: `http://localhost:8080/recipes?includeIngredients=chicken,sugar&excludeIngredients=&cuisine=American,Korean&diet=paleo`

## Structure
```markdown
recipe_maker/
├── config/                    # Defines configuration beans for dependency injection
│   ├── MapperConfig           # Provides a bean for a modelMapper
│   └── RestTemplateConfig     # Provides a bean for a RestTemplate for HTTP client usage
│
├── controllers/               # Handles incoming HTTP requests from the front-end
│   └── AppController          # Defines API endpoints for core application features
│
├── domain/                    # Plain java objects (POJOs) representing application data
│   ├── dto/                   # Objects that are used purely to send and receive data from front-end
│   └── entities/              # Objects that represent database records
│
├── mappers/                   # Classes that help convert one type of object to another
│   └── GenericMapper          # A reusable mapper that converts between DTOs and Entities
│
├── repositories/              # Interfaces that handle database operations
│   ├── IngredientRepository   # Provides methods to access and manage Ingredient data in the database
│   └── RecipeRepository       # Provides methods to access and manage Recipe data in the database
│
├── services/                  # Coordinates external API calls and handles saving data to the database
│   ├── APIClient              # Uses RestTemplate to fetch data from the Spoonacular API
│   ├── IngredientService      # Manages saving Ingredient data to the database
│   └── RecipeService          # Fetches recipes from Spoonacular via APIClient and saves them to the database
│
├── CookbookApplication        # Starts the entire spring boot app
└── README.md                  # You're here!
```
