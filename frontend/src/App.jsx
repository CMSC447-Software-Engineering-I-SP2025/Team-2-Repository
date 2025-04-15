// Required imports
import GetRecipeSection from "./components/GetRecipeSection";
import Header from "./components/Header";
import {useState, useEffect} from "react";
import ResultsDisplay from "./components/ResultsDisplay";
import Papa from 'papaparse';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import RecipeDetail from "./components/RecipeDetail";
import PantryPage from "./components/PantryPage";
import UserRecipesPage from "./components/UserRecipesPage";

import Footer from "./components/Footer";
import HomePage from "./components/HomePage";

export default function App({ingredientNameList, ingredientIDNamePairs}) {
    function saveRecipe(recipe) {
        const serverBaseURLString = "http://localhost:8080";
        let serverBaseURL = new URL(serverBaseURLString);
        let saveRecipeEndpoint = new URL("saverecipe", serverBaseURL);
        const options = {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(recipe)
        };
        fetch(saveRecipeEndpoint, options)
        .catch(error => console.log(error));
    }

    function removeRecipe(recipe) {
        const serverBaseURLString = "http://localhost:8080";
        let serverBaseURL = new URL(serverBaseURLString); 
        let removeRecipeEndpoint = new URL("deleterecipe", serverBaseURL);
        const options = {
            method: "DELETE",
            body: recipe["id"]
        };
        fetch(removeRecipeEndpoint, options)
        .catch(error => console.log(error));
    }

    const [recipes, setRecipes] = useState([]);
    const [favoritedRecipesBitMap, setFavoritedRecipesBitMap] = useState([]);

    useEffect(() => {
        const ingredientCSV = "/top-1k-ingredients.csv";
        const options = {
            "content-type": "text/csv;charset=UTF-8"
        }
        fetch(ingredientCSV, options)
        .then(response => response.text())
        .then(text => Papa.parse(text))
        .then(obj => {ingredientIDNamePairs.length=0; 
                      ingredientIDNamePairs.push(... obj.data.map(pair => ({id: pair[1], name: pair[0]})));
                      return obj.data.map(nameIDPair => nameIDPair[0].toLowerCase())})
        .then(names => [... new Set(names)])
        .then(uniqueNames => {ingredientNameList.length = 0; return ingredientNameList.push(... uniqueNames)})
    }, [])

    return ( 
        <Router>
            <Header />
                <main>
                    <Routes>

                        {/* Homepage */}
                        <Route path="/" element={<HomePage />} />
                        
                        {/* Search Page */}
                        <Route path="/search" element={
                            <>
                                <GetRecipeSection ingredientNameList={ingredientNameList} setRecipes={setRecipes} setFavoritedRecipesBitMap={setFavoritedRecipesBitMap}/>
                                <ResultsDisplay recipes={recipes} favoritedRecipesBitMap={favoritedRecipesBitMap} setFavoritedRecipesBitMap={setFavoritedRecipesBitMap} saveRecipe={saveRecipe} removeRecipe={removeRecipe}/>
                            </>
                        } />

                        {/* Recipe Detail Page */}
                        <Route path="/recipe/:recipeName" element={<RecipeDetail  saveRecipe={saveRecipe} removeRecipe={removeRecipe}/>} />
                        
                        {/* Pantry Page */}
                        <Route path="/pantry" element={<PantryPage uniqueIngredientNames={ingredientNameList} ingredientObjs={ingredientIDNamePairs}/>} />
    
                        {/* Saved Recipes Page */}
                        <Route path="/saved-recipes" element={<UserRecipesPage saveRecipe={saveRecipe} removeRecipe={removeRecipe}/>} />

                        {/* 404 Page */}
                        <Route path="*" element={<h1>404 Not Found</h1>} />

                    </Routes>

                </main>
            <Footer />
        </Router>
    );
}

