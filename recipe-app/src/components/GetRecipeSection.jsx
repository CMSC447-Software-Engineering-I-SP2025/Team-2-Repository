import { useState } from "react";

export default function GetRecipeSection() {
    const [ingredients, setIngredients] = useState(['asparagus', 'califlower', 'carrots']);
    
    return <>
        <div className="get-recipe-section">
            <div className="get-recipe-guide">Find recipes by their ingredients</div>
            <TextArea ingredients={ingredients} setIngredients={setIngredients}/>
            <IngredientList ingredients={ingredients} setIngredients={setIngredients}/>
            <SubmitButton />
        </div>
    </>
}

function TextArea({ingredients, setIngredients}) {
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

function SubmitButton() {
    return <button type="button" className="submit-button">Get Recipes</button>;
}

// function IngredientLine({name}) {
//     return <li>{name}</li>;
// }

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
            {/* <div>Includes: </div> */}
            {/* <ul>
                {ingredients.map((ingredient) => 
                    {return <IngredientLine key={ingredient} name={ingredient}/>
                })}
            </ul>; */}
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