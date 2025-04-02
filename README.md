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
- Navigate to `localhost:8080/recipes?ingredients=x,y,z`
  - make sure you have commas and reference Spoonacular on how to type ingredients
  - example `localhost:8080/recipes?apples,flour,sugar`
