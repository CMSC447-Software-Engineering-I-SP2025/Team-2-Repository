# Overview
This is our recipe app.

# Usage (Windows)

### Frontend
1. Clone the git repo.
2. Download and install [nodeJS](https://nodejs.org/en/download/). 
2. In a terminal in `recipe-app` run `npm install`.
3. To start the frontend, run `npm run dev` to start the dev frontend.
  - Hit `q + Enter`, or run `npx kill-port 5173` to stop the frontend.
5. To start the backend, run `./mvnw clean package`, then run `java -jar .\target\CookbookApp-maker-0.0.1-SNAPSHOT.jar`

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
│       ├── server.py - Routes for the backend
│       ├── client.py - Main business logic. Interacts with Spoonacular / database.
│       ├── backend_data_models.py - Data objects / mapper for Frontend <-> Backend stuff
└── README.md - This file.
```
### Interactions
| Interaction Type                                   | Program Path                                              |
| -------------------------------------------------- | --------------------------------------------------------- |
| Query Spoonacular.                                 | User -> Frontend -> server.py -> client.py -> Spoonacular |
| Save /delete / list recipe(s) / ingredient(s).<br> | User -> Frontend -> server.py -> client.py -> Database    |
