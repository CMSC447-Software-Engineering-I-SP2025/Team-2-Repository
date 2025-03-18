import GetRecipeSection from "./components/GetRecipeSection";
import Header from "./components/Header";
import {useState, useEffect} from "react";
import ResultsDisplay from "./components/ResultsDisplay";
import Papa from 'papaparse';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import RecipeDetail from "./components/RecipeDetail";

export default function App({ingredientNameList}) {
    const [recipes, setRecipes] = useState([]);

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
                                <GetRecipeSection ingredientNameList = {ingredientNameList} setRecipes = {setRecipes}/>
                                <ResultsDisplay recipes={recipes}/>
                            </>
                        } />

                        {/* Recipe Detail Page */}
                        <Route path="/recipe/:recipeName" element={<RecipeDetail />} />
                        
                    </Routes>
                </main>
        </Router>
    );
}

