import GetRecipeSection from "./components/GetRecipeSection";
import Header from "./components/Header";
import ResultsDisplay from "./components/ResultsDisplay";
import React from "react";
import { useState } from "react";

export default function App() {
    const [recipes, setRecipes] = useState([]);
    function pushRecipes (recipesToAdd) {
        const recipeArrCopy = recipes.slice();
        recipeArrCopy.push(... recipesToAdd);
        setRecipes(recipeArrCopy);
    }

    return <>
        
        <Header />
        <main>
            <GetRecipeSection pushRecipes={pushRecipes}/>
            <ResultsDisplay recipes={recipes}/>
        </main>
    </>
}

