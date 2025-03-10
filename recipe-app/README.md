To run the app:
In the recipe-app directory, execute 'npm install' to configure the environment. This will create a large node_modules folders which should not be pushed to github. 
Then, execute 'npm run dev' to start the development server. The terminal will tell you which local host port to access in your browser. Hitting 'q' + 'Enter' in the terminal shuts down the server.

The following examples show how search request data will be transmitted to the backend and how the backend will respond.

outgoing json format example
const outboundJSON =
{
    "includeIngredients": ["apple", "milk", "carrot"],
    "excludeIngredients": ["sugar", "coconut milk", "cilantro"],
    "diet": ["vegetarian", "ketogenic"],
    "intolerances": ["gluten"],
    "cuisine": ["italian"],
    "type": ["main course"]
}

incoming json example
const inboundJSON = 
{
    "ingredients": ["apple", "milk", "carrot"],
    "diet": ["vegetarian", "ketogenic"],
    "intolerances": ["gluten"],
    "cuisine": ["italian"],
    "type": ["main course"]
}