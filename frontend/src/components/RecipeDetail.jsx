{/*Page to display details about a single recipe*/}

import {useParams} from "react-router-dom";
import { useState, useEffect } from "react";
import NutritionLabel from "./NutritionLabel";

export default function RecipeDetail({saveRecipe, removeRecipe, isLoggedIn, setShowLogin}) {
    //the recipe data must be in states b/c the recipe isn't found until after the page loads
    //storing a single recipe state wasn't working, so we have states for each field
    const {recipeName} = useParams();
    const [title, setTitle] = useState(null);
    const [instructions, setInstructions] = useState(null);
    const [imageURL, setImageURL] = useState('');
    const [ingredients, setIngredients] = useState(null);
    const [favorited, setFavorited] = useState(false);
    const [nutrients, setNutrients] = useState([]);
    const [numServings, setNumServings] = useState(null);
    const [missingIngredients, setMissingIngredients] = useState([]);
    const [scaleBy, setScaleBy] = useState("1");
    const serverBaseURLString = "http://localhost:8080";

    let recipe;
    let recipesArr = [];
    let favorite_icon = favorited ? "../star-solid.svg" : "../star-regular.svg";
    let favorite_alt_text = favorited ? "A favorite recipe button set to favorited." : "A favorite recipe button set to not favorited.";

    function checkIfSaved(recipe) {
        let serverBaseURL = new URL(serverBaseURLString); 
        let listRecipesEndpoint = new URL("listrecipes", serverBaseURL);
        const options = {
            method: "GET",
            credentials: "include"
        };
        fetch(listRecipesEndpoint, options)
        .then(response => response.json())
        .then(data => {
            data.forEach(savedRecipe => {
                if (savedRecipe["id"] == recipe["id"]) setFavorited(true);
            });
        })
        .catch(error => console.log(error));
    }

    function getMissingIngredients(recipe) {
        let serverBaseURL = new URL(serverBaseURLString); 
        let listRecipesEndpoint = new URL("findmissing", serverBaseURL);
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(recipe)
        };
        fetch(listRecipesEndpoint, options)
        .then(response => response.json())
        .then(data => {
            const missing = []
            data.forEach(ingr => {
                missing.push(ingr)
            });
            setMissingIngredients(missing)
        })
        .catch(error => console.log(error));
    }

    useEffect(() => {
        if (sessionStorage && sessionStorage.getItem('recipes')) {
            recipesArr = JSON.parse(sessionStorage.getItem('recipes'));
            recipe = recipesArr.find(sessionRecipe => sessionRecipe.title.toLowerCase() == recipeName.toLowerCase());
            if (recipe) {
                setTitle(recipe['title']);
                const tempIngredients = [];
                const  tempInstructions = recipe['analyzedInstructions'] || recipe['instructions'];
                if(tempInstructions?.length > 0) {
                    setInstructions(tempInstructions[0]['steps']);
                }
                recipe['extendedIngredients']?.forEach(ing => tempIngredients.push(ing)) ;
                setIngredients(tempIngredients);
                setImageURL(recipe['image']);
                setNutrients(recipe['nutrition']['nutrients']);
                setNumServings(recipe['servings']);
                checkIfSaved(recipe);
                getMissingIngredients(recipe);
            }
        }
    }, [isLoggedIn]);


    function handleFavoriteClick() {
        if (isLoggedIn) {
            recipesArr = JSON.parse(sessionStorage.getItem('recipes'));
            recipe = recipesArr.find(sessionRecipe => sessionRecipe.title.toLowerCase() == recipeName.toLowerCase());
            favorited ? removeRecipe(recipe) : saveRecipe(recipe);
            setFavorited(!favorited);
        } else {
            setShowLogin(true);
        }

    }

    return (
        <div className="recipe-detail">
            {title ? ( // page status requires a state check because data loads after page loads
                <>
                   <div className="recipe-title">
                        <h1>{title}</h1>
                   </div>
                   <div className="image-and-save-section">
                        <div className="detail-image-holder">{imageURL ? <img src= {imageURL} alt={recipeName}/>: <div>No Image Provided</div>}</div>
                        <div className="favorite-recipe-element">      
                            <div className="scale">
                                Scale By: 
                                x {scaleBy}
                                <input value={scaleBy} type="range" min="1" max="8" step="1" onChange={e => setScaleBy(e.target.value)}></input>
                            </div>                      
                            {favorited ? "Saved!": "Save Recipe?"}
                            <img className="favorite-button" src={favorite_icon} alt={favorite_alt_text} onClick={() => handleFavoriteClick()}/>
                        </div>
                    </div>

                    {
                        instructions ? 
                        <div className="recipe-detail-text-sections">
                            <div className="ingredients-and-time-area">
                                <div>
                                    <h2>Servings: {numServings * parseInt(scaleBy)}</h2>
                                </div>
                                <div className="recipe-ingredients-display">

                                    <h2>Ingredients</h2>                                
                                    <ul>
                                        {ingredients.map((ing, index) => (
                                            <li key={index}><b>{ing.name}</b> - {Math.round((ing.amount * parseInt(scaleBy))*1000)/1000} <span style={{textTransform:"none"}}>{ing.unit}</span> </li>
                                        ))}
                                    </ul> 
                                </div>
                            </div>
                            <div className="steps-section">
                                <h2>Steps</h2>
                                <ol>
                                    {instructions.map((fullStep, index) => (
                                            <li key={index}>{fullStep.step}</li>
                                    ))}
                                </ol>
                            </div> 
                        </div> :
                        <div>No Instructions Or Ingredients Provided</div>
                    }
                    <div className="extra-details">  
                            {isLoggedIn && 
                                <div className="missing-list"> 
                                    <h2>Missing From Pantry</h2>
                                    <ul>
                                        {missingIngredients.map((item, index) => (
                                            <li key={index}>{item}</li>
                                        ))}                   
                                    </ul>
                                </div>
                            }
                        <NutritionLabel nutrientsRaw={nutrients} servings={numServings}/>
                    </div>
                </>
            ) : (
                <h2>Recipe not found</h2>
            )}
        </div>
    );
}