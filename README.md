# Team-2-Repository
This is a recipe finder application that uses the Spoonacular API.

### Running the Frontend
1. Download [nodeJS](https://nodejs.org/en/download/)
2. In `/frontend` run `npm install`, then run `npm run dev`.
3. For sunsequent runs, go to `/frontend` and run `num run dev`.
4. To stop the server do one of the following:
    - Hit `Q + Enter`
    - Hit `Ctrl + C`
    - In another terminal, run `npx kill-port 5173`

### Running the Backend
1. Run `.\backend\.venv\Scripts\activate`
2. Run `python .\backend\src\server.py`
3. Go to `http://localhost:5173/`

## Project Structure
### Files
```markdown
.
├── frontend
│   └── react-js - ReactJS frontend.
├── backend
│   ├── assets
│   │   ├── cached.json - Cached JSON response for testing.
│   │   └── config.toml - Backend config info.
│   └── src - Source code
│       ├── server.py - Routes for the backend
│       ├── client.py - Main business logic. Interacts with Spoonacular / database.
│       ├── data_classes.py - Data objects / mapper for Frontend <-> Backend stuff
│       └── db_models.py - Data objects / mappers for Backend <-> Database stuff
└── README.md - This file.
```
### Interactions
| Interaction Type                                   | Program Path                                              |
| -------------------------------------------------- | --------------------------------------------------------- |
| Query Spoonacular.                                 | User -> Frontend -> server.py -> client.py -> Spoonacular |
| Save /delete / list recipe(s) / ingredient(s).<br> | User -> Frontend -> server.py -> client.py -> Database    |