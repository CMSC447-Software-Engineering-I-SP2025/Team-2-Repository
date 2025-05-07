import { useEffect, useState } from "react";
import ResultsDisplay from "./ResultsDisplay";

export default function UserRecipesPage ({saveRecipe, removeRecipe}) {
    const [savedRecipes, setSavedRecipes] = useState([]);
    const [favoritedRecipesBitMap, setFavoritedRecipesBitMap] = useState([]);
    const [loggedIn, setLoggedIn] = useState(false);

    useEffect(() => {
        // const recipeIDs = recipes.map(recipe => recipe["id"]);
        // const favoritesCopy = new Array(recipes.length).fill(false);
        const serverBaseURLString = "http://localhost:8080";
        let serverBaseURL = new URL(serverBaseURLString); 
        let listRecipesEndpoint = new URL("listrecipes", serverBaseURL);
        const options = {
            method: "GET",
            credentials: "include"
        };

        fetch(listRecipesEndpoint, options)
        .then(response => {
            if(response.status == 401) {
                setLoggedIn(false);
                throw new Error(`401 - Not authenticated`);
            }
            setLoggedIn(true);
            return response.json();
        }).then(data => {
            const savedRecipesTemp = [];
            data.forEach(savedRecipe => {
                //favoritesCopy[recipeIDs.indexOf(savedRecipe["id"])] = true;
                savedRecipesTemp.push(savedRecipe);
            });
            setSavedRecipes(savedRecipesTemp);
            sessionStorage.setItem("recipes", JSON.stringify(savedRecipesTemp));
            const favoritesBitArrayTemp = new Array(savedRecipesTemp.length);
            favoritesBitArrayTemp.fill(true);
            setFavoritedRecipesBitMap(favoritesBitArrayTemp);
        })
        .catch(error => console.log(error));

    }, []);

    return <>
        {loggedIn ?
            <><h1 style={{textAlign: "center"}}>Saved Recipes</h1>
            {savedRecipes.length > 0 ? 
                <ResultsDisplay recipes={savedRecipes} favoritedRecipesBitMap={favoritedRecipesBitMap} setFavoritedRecipesBitMap={setFavoritedRecipesBitMap} saveRecipe={saveRecipe} removeRecipe={removeRecipe} />
                : <div style={{textAlign: "center", color: " #A52A2A"}}> No recipes saved yet. Time to start your culinary adventure! </div>
            }</>
        : <h3 style={{textAlign: "center"}}>Not logged in</h3>
        }
    </>
}