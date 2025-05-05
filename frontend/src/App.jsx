// Required imports
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import {useState, useEffect} from "react";
import Papa from 'papaparse';

// importing components
import GetRecipeSection from "./components/GetRecipeSection";
import Header from "./components/Header";
import ResultsDisplay from "./components/ResultsDisplay";
import RecipeDetail from "./components/RecipeDetail";
import PantryPage from "./components/PantryPage";
import UserRecipesPage from "./components/UserRecipesPage";
import LoginRegisterModal from "./components/LoginRegisterModal";
import CategoryPage from "./components/CategoryPage";
import Footer from "./components/Footer";
import HomePage from "./components/HomePage";

//import AuthContext from "./context/AuthContext";


export default function App({ingredientNameList, ingredientIDNamePairs}) {
    const serverBaseURLString = "http://localhost:8080";
    let serverBaseURL = new URL(serverBaseURLString);


    function saveRecipe(recipe) {
        let saveRecipeEndpoint = new URL("saverecipe", serverBaseURL);
        const options = {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(recipe)
        };
        fetch(saveRecipeEndpoint, options)
        .catch(error => console.log(error));
    }

    function removeRecipe(recipe) {
        let removeRecipeEndpoint = new URL("deleterecipe", serverBaseURL);
        const options = {
            method: "DELETE",
            credentials: "include",
            body: recipe["id"]
        };
        fetch(removeRecipeEndpoint, options)
        .catch(error => console.log(error));
    }

    // Checks in with backend whether user is logged in. The frontend cannot check the user's session cookie, but the backend automatically receives it.
    async function queryLoginStatus() {
        let loginStatusEndpoint = new URL("loginstatus", serverBaseURL);
        const options = {
            method: "GET",
            credentials: "include"
        }
        fetch(loginStatusEndpoint, options)
        .then(response => response.text())
        .then(status => status == 'Logged In')
        .then(status => setIsLoggedIn(status))
        .catch(error => console.log(error));

    }

    const [recipes, setRecipes] = useState([]);
    const [favoritedRecipesBitMap, setFavoritedRecipesBitMap] = useState([]);

    useEffect(() => {
        //Fetching the top spoonacular ingredients from a csv
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

        queryLoginStatus();
    }, [])

    const [showLoginModal, setShowLoginModal] = useState(false);
    const toggleLoginModal = () => setShowLoginModal(prev => !prev);
    // Last known status of whether user is logged in. Only check this for low risk actions that don't interact with backend. 
    // Otherwise, the status should be re-checked by querying backend since this value could be tampered with or session could have expired.
    const [isLoggedIn, setIsLoggedIn] = useState(false); 
    // const [userName, setUserName] = useState(); //only used to display user's name

    return ( 
        <Router>
            <div className="page-wrapper">
                <Header onLoginIconClick={toggleLoginModal} isLoggedIn={isLoggedIn}/>
                    <main>
                        <Routes>

                            {/* Homepage */}
                            <Route path="/" element={<HomePage />} />
                            
                            {/* Search Page */}
                            <Route path="/search" element={
                                <>
                                    <GetRecipeSection ingredientNameList={ingredientNameList} setRecipes={setRecipes} setFavoritedRecipesBitMap={setFavoritedRecipesBitMap} isLoggedIn={isLoggedIn}/>
                                    <ResultsDisplay recipes={recipes} favoritedRecipesBitMap={favoritedRecipesBitMap} setFavoritedRecipesBitMap={setFavoritedRecipesBitMap} saveRecipe={saveRecipe} removeRecipe={removeRecipe}/>
                                </>
                            } />

                            {/* Recipe Detail Page */}
                            <Route path="/recipe/:recipeName" element={<RecipeDetail  saveRecipe={saveRecipe} removeRecipe={removeRecipe}/>} />
                            
                            {/* Pantry Page */}
                            <Route path="/pantry" element={<PantryPage uniqueIngredientNames={ingredientNameList} ingredientObjs={ingredientIDNamePairs}/>} />
        
                            {/* Saved Recipes Page */}
                            <Route path="/saved-recipes" element={<UserRecipesPage saveRecipe={saveRecipe} removeRecipe={removeRecipe}/>} />

                            {/* Category/Subcategory Page */}
                            <Route path="/:category" element={<CategoryPage />} />
                            <Route path="/:category/:subcategory" element={<CategoryPage />} />

                            {/* 404 Page */}
                            <Route path="*" element={<h1>404 Not Found</h1>} />

                        </Routes>

                    </main>
                <Footer />
                <LoginRegisterModal show={showLoginModal} onClose={() => setShowLoginModal(false)} isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn}/>
            </div>
        </Router>
    );
};