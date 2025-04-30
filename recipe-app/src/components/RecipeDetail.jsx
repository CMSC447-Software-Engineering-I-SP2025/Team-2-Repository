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


    let numServings = 2;
    let nutrientsRaw = [
        {
          "name": "Calories",
          "amount": 538.7,
          "unit": "kcal",
          "percentOfDailyNeeds": 26.94
        },
        {
          "name": "Fat",
          "amount": 14.62,
          "unit": "g",
          "percentOfDailyNeeds": 22.49
        },
        {
          "name": "Saturated Fat",
          "amount": 1.97,
          "unit": "g",
          "percentOfDailyNeeds": 12.29
        },
        {
          "name": "Carbohydrates",
          "amount": 84.48,
          "unit": "g",
          "percentOfDailyNeeds": 28.16
        },
        {
          "name": "Net Carbohydrates",
          "amount": 69.7,
          "unit": "g",
          "percentOfDailyNeeds": 25.35
        },
        {
          "name": "Sugar",
          "amount": 17.87,
          "unit": "g",
          "percentOfDailyNeeds": 19.85
        },
        {
          "name": "Cholesterol",
          "amount": 0,
          "unit": "mg",
          "percentOfDailyNeeds": 0
        },
        {
          "name": "Sodium",
          "amount": 221.29,
          "unit": "mg",
          "percentOfDailyNeeds": 9.62
        },
        {
          "name": "Alcohol",
          "amount": 0,
          "unit": "g",
          "percentOfDailyNeeds": 100
        },
        {
          "name": "Alcohol %",
          "amount": 0,
          "unit": "%",
          "percentOfDailyNeeds": 100
        },
        {
          "name": "Protein",
          "amount": 20.86,
          "unit": "g",
          "percentOfDailyNeeds": 41.72
        },
        {
          "name": "Manganese",
          "amount": 2.57,
          "unit": "mg",
          "percentOfDailyNeeds": 128.69
        },
        {
          "name": "Folate",
          "amount": 394.21,
          "unit": "µg",
          "percentOfDailyNeeds": 98.55
        },
        {
          "name": "Fiber",
          "amount": 14.78,
          "unit": "g",
          "percentOfDailyNeeds": 59.11
        },
        {
          "name": "Copper",
          "amount": 1.06,
          "unit": "mg",
          "percentOfDailyNeeds": 52.75
        },
        {
          "name": "Magnesium",
          "amount": 210.24,
          "unit": "mg",
          "percentOfDailyNeeds": 52.56
        },
        {
          "name": "Phosphorus",
          "amount": 520.59,
          "unit": "mg",
          "percentOfDailyNeeds": 52.06
        },
        {
          "name": "Iron",
          "amount": 7.49,
          "unit": "mg",
          "percentOfDailyNeeds": 41.62
        },
        {
          "name": "Vitamin B1",
          "amount": 0.53,
          "unit": "mg",
          "percentOfDailyNeeds": 35.46
        },
        {
          "name": "Potassium",
          "amount": 1149.58,
          "unit": "mg",
          "percentOfDailyNeeds": 32.85
        },
        {
          "name": "Vitamin B6",
          "amount": 0.61,
          "unit": "mg",
          "percentOfDailyNeeds": 30.66
        },
        {
          "name": "Zinc",
          "amount": 4.11,
          "unit": "mg",
          "percentOfDailyNeeds": 27.38
        },
        {
          "name": "Vitamin B2",
          "amount": 0.34,
          "unit": "mg",
          "percentOfDailyNeeds": 20.08
        },
        {
          "name": "Vitamin E",
          "amount": 2.55,
          "unit": "mg",
          "percentOfDailyNeeds": 17.01
        },
        {
          "name": "Selenium",
          "amount": 10.92,
          "unit": "µg",
          "percentOfDailyNeeds": 15.6
        },
        {
          "name": "Vitamin B5",
          "amount": 1.51,
          "unit": "mg",
          "percentOfDailyNeeds": 15.07
        },
        {
          "name": "Vitamin K",
          "amount": 15.16,
          "unit": "µg",
          "percentOfDailyNeeds": 14.44
        },
        {
          "name": "Vitamin C",
          "amount": 10.76,
          "unit": "mg",
          "percentOfDailyNeeds": 13.04
        },
        {
          "name": "Vitamin B3",
          "amount": 2.6,
          "unit": "mg",
          "percentOfDailyNeeds": 13.02
        },
        {
          "name": "Calcium",
          "amount": 103.04,
          "unit": "mg",
          "percentOfDailyNeeds": 10.3
        },
        {
          "name": "Vitamin A",
          "amount": 385.89,
          "unit": "IU",
          "percentOfDailyNeeds": 7.72
        }
      ];

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

        
        //The label gives the nutrition by serving, so we may want to also return serving size or number of servings per recipe in regular get recipe requests
        const apiKey = "";
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
                // getNutritionFacts(recipe['id']);
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
                    {/* <div dangerouslySetInnerHTML={widget}></div> */}
                    <NutritionLabel nutrientsRaw={nutrientsRaw} servings={numServings}/>
                </>
            ) : (
                <h2>Recipe not found</h2>
            )}
        </div>
    );
}