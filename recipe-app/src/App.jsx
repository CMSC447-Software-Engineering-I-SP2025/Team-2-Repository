// Required imports
import GetRecipeSection from "./components/GetRecipeSection";
import Header from "./components/Header";
import {useState, useEffect} from "react";
import ResultsDisplay from "./components/ResultsDisplay";
import Papa from 'papaparse';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import RecipeDetail from "./components/RecipeDetail";

export default function App({ingredientNameList}) {
    function saveRecipe(recipe) {
        const serverBaseURLString = "http://localhost:8080";
        let serverBaseURL = new URL(serverBaseURLString);
        let saveRecipeEndpoint = new URL("saverecipe", serverBaseURL);
        const options = {
            method: "POST",
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
        .then(obj => obj.data.map(nameIDPair => nameIDPair[0].toLowerCase()))
        .then(names => [... new Set(names)])
        .then(uniqueNames => {ingredientNameList.length = 0; return ingredientNameList.push(... uniqueNames)})
    }, [])

    return ( 
        <Router>
            <Header />
                <main>
                    <Routes>
                        {/* Homepage */}
                        <Route path="/" element={
                            <>
                                <GetRecipeSection ingredientNameList={ingredientNameList} setRecipes={setRecipes} setFavoritedRecipesBitMap={setFavoritedRecipesBitMap}/>
                                <ResultsDisplay recipes={recipes} favoritedRecipesBitMap={favoritedRecipesBitMap} setFavoritedRecipesBitMap={setFavoritedRecipesBitMap} saveRecipe={saveRecipe} removeRecipe={removeRecipe}/>
                            </>
                        } />

                        {/* Recipe Detail Page */}
                        <Route path="/recipe/:recipeName" element={<RecipeDetail  saveRecipe={saveRecipe} removeRecipe={removeRecipe}/>} />
                        
                    </Routes>
                </main>
        </Router>
    );
}

