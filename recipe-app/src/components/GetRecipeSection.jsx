import { useState } from "react";

export default function GetRecipeSection({pushRecipes}) {
    const [ingredients, setIngredients] = useState(['asparagus', 'califlower', 'carrots']);
    const serverIP = "localhost:8080";

    //creating sample response for testing
    const dataJSON = {
        "recipes": [
            {
                "name": "chicken pot pie",
                "image": "/chicken_pot_pie.jpeg",
                "instructions": [],
                "ingredients": [], 
                "diet": [],
                "intolerances" : [],
                "cuisine": []
            },
            {
                "name": "chicken cacciatore",
                "image": "/chicken_cacciatore.webp",
                "instructions": [],
                "ingredients": [], 
                "diet": [],
                "intolerances" : [],
                "cuisine": []
            },
            {
                "name": "green chili stew",
                "image": "/green-chili-stew.webp",
                "instructions": [],
                "ingredients": [], 
                "diet": [],
                "intolerances" : [],
                "cuisine": []
            },
            {
                "name": "ground beef dish",
                "image": "/ground-beef.jpg",
                "instructions": [],
                "ingredients": [], 
                "diet": [],
                "intolerances" : [],
                "cuisine": []
            },
            {
                "name": "some recipe",
                "image": "https://img.spoonacular.com/recipes/632660-312x231.jpg",
                "instructions": [],
                "ingredients": [], 
                "diet": [],
                "intolerances" : [],
                "cuisine": []
            }
        ]
    };
    const myBlob = new Blob([JSON.stringify(dataJSON)], {type: "application/json"});
    const sampleResponse = new Response(myBlob);

    function handleSubmit() {
        const outgoingJSON = JSON.stringify(
            {includeIngredients:ingredients}, 
            {excludeIngredients:[]}, 
            {diet:[]},
            {intolerances:[]},
            {cuisine: []})
        console.log(outgoingJSON);
        const options = {
            method: "GET",
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            },
            body: outgoingJSON
        }
        // Have to figure out how to start the springboot server in order to test the connection
        // fetch(serverIP, options)
        // .then(response => response.json())
        // .then(data => console.log(data))
        // .catch(error => console.error(error))
        // .then(response => response.recipes.map(recipe => pushRecipe(recipe)));
        const tempArr = [];
        sampleResponse.json().then(response => {
            response.recipes.forEach(recipe => tempArr.push(recipe));
            pushRecipes(tempArr);
        })
    }

    return <>
        <div className="get-recipe-section">
            <div className="get-recipe-guide">Find recipes by their ingredients</div>
            <InputTextArea ingredients={ingredients} setIngredients={setIngredients}/>
            <IngredientList ingredients={ingredients} setIngredients={setIngredients}/>
            <SubmitButton handleSubmit={handleSubmit}/>
        </div>
    </>
}

function InputTextArea({ingredients, setIngredients}) {
    const [inputVal, setInputVal] = useState("");
    //input val is the exact string current on the searchbar. remember to convert to lowercase before doing anything with it.

    function pushIngredient (ingredient) {
        ingredient = ingredient.toLowerCase();
        if(ingredients.indexOf(ingredient) >= 0) return;
        const ingredientArrCopy = ingredients.slice();
        ingredientArrCopy.push(ingredient);
        setIngredients(ingredientArrCopy);
    }

    function keyEvent(key, ingredient) {
        if(key === 'Enter') {
            pushIngredient(ingredient);
        }
    }

    return <label className="textArea">
        <div className="input-prompt">Ingredient:</div>
        <input className="ingredientSearchBar"
            type="text" 
            onChange={(e) => setInputVal(e.target.value)}
            onKeyUp={(e) => keyEvent(e.key, inputVal)}
        />
        <button type="button" className="add-ingredient-button" onClick={() => pushIngredient(inputVal)}>Add</button>
    </label>
}

function SubmitButton({handleSubmit}) {
    return <button type="button" className="submit-button" onClick={handleSubmit}>Get Recipes</button>;
}

function IngredientList({ingredients, setIngredients}) {
    function removeIngredient (ingredient) {
        //error because of key duplicate if duplicate ingredient, make sure to disallow dupes.
        const ingredientArrCopy = ingredients.slice();
        const index = ingredientArrCopy.indexOf(ingredient);
        ingredientArrCopy.splice(index, 1);
        setIngredients(ingredientArrCopy);
    }
    return <>
        <div className="ingredient-list">
            <div className="ingredient-grid">
                {ingredients.map((ingredient) => 
                    {return <FilterBlock key={ingredient} filterName={ingredient} handleClick={() => removeIngredient(ingredient)}  filterType = "contains-ingredient"/>
                })}
            </div>
        </div>
    </>
}

function FilterBlock({filterName, filterType, handleClick}) {
    const classStr = "filter-block " + {filterType}; 
    let croppedName = filterName;
    if(croppedName.length > 17) {
        croppedName = croppedName.slice(0, 17) + "...";
    }
    return <div className={classStr}><div className="filter-text">{croppedName}</div><FilterX handleClick={handleClick}/></div>;
}

function FilterX({handleClick}) {
    return <button className="filter-x" onClick={handleClick}>&#10006;</button>;
}