import { useEffect, useState } from "react";
import ResultsDisplay from "./ResultsDisplay";

export default function UserRecipesPage ({saveRecipe, removeRecipe}) {
    const [savedRecipes, setSavedRecipes] = useState([]);
    const [favoritedRecipesBitMap, setFavoritedRecipesBitMap] = useState([]);

    useEffect(() => {
        // const recipeIDs = recipes.map(recipe => recipe["id"]);
        // const favoritesCopy = new Array(recipes.length).fill(false);
        const serverBaseURLString = "http://localhost:8080";
        let serverBaseURL = new URL(serverBaseURLString); 
        let listRecipesEndpoint = new URL("listrecipes", serverBaseURL);
        const options = {method: "GET"};

        fetch(listRecipesEndpoint, options)
        .then(response => response.json())
        .then(data => {
            const savedRecipesTemp = [];
            data.forEach(savedRecipe => {
                //favoritesCopy[recipeIDs.indexOf(savedRecipe["id"])] = true;
                savedRecipesTemp.push(savedRecipe);
            });
            setSavedRecipes(savedRecipesTemp);
            sessionStorage.setItem("recipes", JSON.stringify(savedRecipesTemp));
            const favoritesBitArrayTemp = new Array(savedRecipesTemp.length);
            favoritesBitArrayTemp.fill(true);
            console.log(favoritesBitArrayTemp);
            setFavoritedRecipesBitMap(favoritesBitArrayTemp);
        })
        .catch(error => console.log(error));
    }, []);

    return <>
        <h1 style={{textAlign: "center"}}>Saved Recipes</h1>
        {savedRecipes.length > 0 ? 
            <ResultsDisplay recipes={savedRecipes} favoritedRecipesBitMap={favoritedRecipesBitMap} setFavoritedRecipesBitMap={setFavoritedRecipesBitMap} saveRecipe={saveRecipe} removeRecipe={removeRecipe} />
            : <div style={{textAlign: "center", color: " #A52A2A"}}> No recipes saved yet. Time to start your culinary adventure! </div>
        }
    </>
}