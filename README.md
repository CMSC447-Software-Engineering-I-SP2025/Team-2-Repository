# Team-2-Repository
This is a recipe finder application that uses the Spoonacular API.


# Frontend
## Usage
1. Download [nodeJS](https://nodejs.org/en/download/)
2. In `/frontend` run `npm install`, then run `npm run dev`.
3. For sunsequent runs, go to `/frontend` and run `num run dev`.
4. To stop the server do one of the following:
    - Hit `Q + Enter`
    - Hit `Ctrl + C`
    - In another terminal, run `npx kill-port 5173`

# Backend
## Usage
1. Run `.\backend\.venv\Scripts\activate`
2. Run `python .\backend\src\server.py`
3. Go to `http://localhost:5173/`

# Structure
```markdown

```


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
