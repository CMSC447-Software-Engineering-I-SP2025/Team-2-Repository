import {useParams} from "react-router-dom";
import { useState, useEffect } from "react";

export default function RecipeDetail() {
    //the recipe data must be in states b/c the recipe isn't found until after the page loads
    //storing a single recipe state wasn't working, so we have states for each field
    const {recipeName} = useParams();
    const [title, setTitle] = useState(null);
    const [instructions, setInstructions] = useState([]);
    const [imageURL, setImageURL] = useState('');
    let recipesArr = [], recipe;

    useEffect(() => {
        if (sessionStorage && sessionStorage.getItem('recipes')) {
            recipesArr = JSON.parse(sessionStorage.getItem('recipes'));
            recipe = recipesArr.find(recipe => recipe.title.toLowerCase() == recipeName.toLowerCase());
            recipeName.toLowerCase()
            console.log(recipesArr.length);
            console.log(recipesArr[1].title.toLowerCase());
            console.log(recipe);
            console.log(recipe.title);
            setTitle(recipe['title']);
            setInstructions(recipe['analyzedInstructions'][0]['steps'])
            setImageURL(recipe['image']);
        }
    }, []);

    return (
        <div className="recipe-detail">
            {title ? ( //page status requires a state check because data loads after page loads
                <>
                   <h1>{title}</h1>
                   {imageURL ? <img src= {imageURL} alt={recipeName}/>: null}  
                    {/* <h2>Ingredients</h2>
                    <ul>
                        {recipe.ingredients.map((item, index) => (
                            <li key={index}>{item}</li>
                        ))}
                    </ul> */}
                    <h2>Steps</h2>
                    <ol>
                        {instructions.map((fullStep, index) => (
                                <li key={index}>{fullStep.step}</li>
                        ))}
                    </ol>
                </>
            ) : (
                <h2>Recipe not found</h2>
            )}
        </div>
    );
}