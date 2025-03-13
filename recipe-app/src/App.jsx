import GetRecipeSection from "./components/GetRecipeSection";
import Header from "./components/Header";
import ResultsDisplay from "./components/ResultsDisplay";
import React from "react";
import { useState } from "react";

export default function App() {
    const [recipes, setRecipes] = useState([]);
    return <>
        <Header />
        <main>
            <GetRecipeSection setRecipes={setRecipes}/>
            <ResultsDisplay recipes={recipes}/>
        </main>
    </>
}

