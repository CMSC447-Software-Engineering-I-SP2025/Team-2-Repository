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
1. `cd /Team-2-Repository`
2. `python -m venv .venv`
3. `.\.venv\Scripts\activate`
4. `python -m pip install -r requirements.txt`
5. `python .\backend\src\server.py`

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
│       ├── server.py - Core business logic.
│       ├── data_classes.py - Data objects / mappers for Frontend <-> Backend data transfer.
│       └── db_models.py - Data objects / mappers for Backend <-> Database data transfer.
└── README.md - This file.
```
### Interactions
| Interaction Type                                   | Program Path                                              |
| -------------------------------------------------- | --------------------------------------------------------- |
| Query Spoonacular.                                 | User -> Frontend -> server.py -> client.py -> Spoonacular |
| Save /delete / list recipe(s) / ingredient(s).<br> | User -> Frontend -> server.py -> client.py -> Database    |