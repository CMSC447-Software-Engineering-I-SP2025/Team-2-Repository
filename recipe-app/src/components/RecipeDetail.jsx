{/*Page to display details about a single recipe*/}

import {useParams} from "react-router-dom";
import { useState, useEffect } from "react";
import NutritionLabel from "./NutritionLabel";

export default function RecipeDetail({saveRecipe, removeRecipe}) {
    //the recipe data must be in states b/c the recipe isn't found until after the page loads
    //storing a single recipe state wasn't working, so we have states for each field
    const {recipeName} = useParams();
    const [title, setTitle] = useState(null);
    const [instructions, setInstructions] = useState(null);
    const [imageURL, setImageURL] = useState('');
    const [ingredients, setIngredients] = useState(null);
    const [favorited, setFavorited] = useState(false);
    const [widgetHTML, setWidgetHTML] = useState("");
    let widget = {__html: widgetHTML}
    const serverBaseURLString = "http://localhost:8080";

    // let widget = document.createElement('html');
    // widget.innerHTML = widgetHTML;

    // let widget = "";
    let recipe;
    let recipesArr = [];
    let favorite_icon = favorited ? "../star-solid.svg" : "../star-regular.svg";
    let favorite_alt_text = favorited ? "A favorite recipe button set to favorited." : "A favorite recipe button set to not favorited.";

    function checkIfSaved(recipe) {
        let serverBaseURL = new URL(serverBaseURLString); 
        let listRecipesEndpoint = new URL("listrecipes", serverBaseURL);
        const options = {method: "GET"};
        fetch(listRecipesEndpoint, options)
        .then(response => response.json())
        .then(data => {
            data.forEach(savedRecipe => {
                if (savedRecipe["id"] == recipe["id"]) setFavorited(true);
            });
        })
        .catch(error => console.log(error));
    }

    function getNutritionFacts(recipeID) {
        //Backend: Make an endpoint for that takes an recipe id parameter and forms a request to spoonacular nutrition label endpoint
        //Front end will send a GET request with a recipeID url parameter. Pass along the html string that spoonacular returns back to us.
        //Frontend request: GET http://localhost:8080/nutritionLabel?recipeID={id}
        //Spoonacular request: GET https://api.spoonacular.com/recipes/{id}/nutritionLabel?apiKey={key}
        
        //The label gives the nutrition by serving, so we may want to also return serving size or number of servings per recipe in regular get recipe requests
        apiKey = "";
        let spoonacularWidgetEndpoint = "https://api.spoonacular.com/recipes/" + recipeID + "/nutritionLabel?apiKey="  + apiKey;
        //let spoonacularWidgetEndpoint = "https://api.spoonacular.com/recipes/" + recipeID + "/nutritionLabel?showIngredients=true&apiKey=" + apiKey;
        
        const options = {method: "GET"};
        fetch(spoonacularWidgetEndpoint, options)
        .then(response => response.text())
        .then(html => {
            setWidgetHTML(html);
            console.log(widgetHTML);
        })
        .catch(error => console.log(error));


        // let serverBaseURL = new URL(serverBaseURLString); 
        // let getNutritionLabelEndpoint = new URL("nutritionLabel", serverBaseURL);
        // recipeEndpoint.searchParams.append("recipeID", recipeID);
        // const options = {method: "GET"};
        // fetch(getNutritionLabelEndpoint, options)
        // .then(response => response.text())
        // .then(html => {
        //     setWidgetHTML(html);
        //     console.log(widgetHTML);
        // })
        // .catch(error => console.log(error));
    }

    useEffect(() => {
        //console.log("state: " + state);
        if (sessionStorage && sessionStorage.getItem('recipes')) {
            recipesArr = JSON.parse(sessionStorage.getItem('recipes'));
            recipe = recipesArr.find(sessionRecipe => sessionRecipe.title.toLowerCase() == recipeName.toLowerCase());
            if (recipe) {
                console.log(recipe);
                setTitle(recipe['title']);
                const tempIngredients = [];
                if(recipe['analyzedInstructions']?.length > 0) {
                    setInstructions(recipe['analyzedInstructions'][0]['steps']);
                    recipe['analyzedInstructions'][0]['steps'].forEach( stepInfo => {
                        tempIngredients.push(... stepInfo['ingredients']
                                            .filter(info => info['id'] > 0)
                                            .map(ingredientInfo => ingredientInfo['name']));
                    });
                    console.log(tempIngredients);
                    setIngredients([... new Set(tempIngredients)]);
                }
                setImageURL(recipe['image']);

                checkIfSaved(recipe);
                getNutritionFacts(recipe['id']);
            }
        }
    }, []);


    function handleFavoriteClick() {
        recipesArr = JSON.parse(sessionStorage.getItem('recipes'));
        recipe = recipesArr.find(sessionRecipe => sessionRecipe.title.toLowerCase() == recipeName.toLowerCase());
        favorited ? removeRecipe(recipe) : saveRecipe(recipe);
        setFavorited(!favorited);
    }

    return (
        <div className="recipe-detail">
            {title ? ( // page status requires a state check because data loads after page loads
                <>
                   <div className="recipe-title">
                        <h1>{title}</h1>
                   </div>
                   <div className="image-and-save-section">
                        <div>{imageURL ? <img src= {imageURL} alt={recipeName}/>: <div>No Image Provided</div>}</div>
                        <div className="favorite-recipe-element">
                            {favorited ? "Saved!": "Save Recipe?"}
                            <img className="favorite-button" src={favorite_icon} alt={favorite_alt_text} onClick={() => handleFavoriteClick()}/>
                        </div>
                    </div>

                    {
                        instructions ? 
                        <div className="recipe-detail-text-sections">
                            <div className="ingredients-and-time-area">
                            <div className="recipe-ingredients-display">
                                <h2>Ingredients</h2>
                                <ul>
                                    {ingredients.map((item, index) => (
                                        <li key={index}>{item}</li>
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
                    <div dangerouslySetInnerHTML={widget}></div>
                    {/* <NutritionLabel /> */}
                </>
            ) : (
                <h2>Recipe not found</h2>
            )}
        </div>
    );
}