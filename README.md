# Team-2-Repository

# Frontend
---
# How to use
1. Download nodeJS to get access to npm, a package manager (we don't actually use node in the app). https://nodejs.org/en/download/
2. In the recipe-app directory, execute 'npm install' to configure the environment. This looks through the package.json for any specified dependencies and installs them automatically. This will create a large node_modules folders which should not be pushed to github since that would be redundant. 
3. Then, execute 'npm run dev' to start the development server. This executes a script in package.json that starts up a vite server. The terminal will tell you which local host port to access in your browser. Hitting 'q' + 'Enter' in the terminal shuts down the server. "npx kill-port 5173" is also useful for ending the process if the vite menu is no longer focused in the terminal. Running on port 5173 is important because that is explicitly what has been given permission to interface with our backend.
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