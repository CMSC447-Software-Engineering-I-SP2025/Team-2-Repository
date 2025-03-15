To run the app:
1. Download nodeJS to get access to npm, a package manager (we don't actually use node in the app). https://nodejs.org/en/download/
2. In the recipe-app directory, execute 'npm install' to configure the environment. This looks through the package.json for any specified dependencies and installs them automatically. This will create a large node_modules folders which should not be pushed to github since that would be redundant. 
3. Then, execute 'npm run dev' to start the development server. This executes a script in package.json that starts up a vite server. The terminal will tell you which local host port to access in your browser. Hitting 'q' + 'Enter' in the terminal shuts down the server. "npx kill-port 5173" is also useful for ending the process if the vite menu is no longer focused in the terminal. Running on port 5173 is important because that is explicitly what has been given permission to interface with our backend.

json response example
const inboundJSON = 
{
    "id": 716429,
    "title": "Pasta with Garlic, Scallions, Cauliflower & Breadcrumbs",
    "image": "https://img.spoonacular.com/recipes/716429-312x231.jpg",
    "ingredients": ["apple", "milk", "carrot"],
    "diet": ["vegetarian", "ketogenic"],
    "intolerances": ["gluten"],
    "cuisine": ["italian"],
    "type": ["main course"]
}