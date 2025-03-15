import GetRecipeSection from "./components/GetRecipeSection";
import Header from "./components/Header";
import React, { useEffect } from "react";
import ResultsDisplay from "./components/ResultsDisplay";
import Papa from 'papaparse';

export default function App() {
    let ingredientNameList = [];
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

    return <>
        <main>
            <Header />
            <GetRecipeSection ingredientNameList = {ingredientNameList}/>
            <ResultsDisplay />
        </main>
    </>
}

