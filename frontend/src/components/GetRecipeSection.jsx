import { AdditionalFiltersAccordion } from "./AdditionalFiltersAccordion";
import { useState, useRef, useEffect } from "react";
import clsx from 'clsx'

export default function GetRecipeSection({ingredientNameList, setRecipes, setFavoritedRecipesBitMap, isLoggedIn}) {

    const cuisineList = [
        "African", "Asian", "American", "British", "Cajun", "Caribbean", "Chinese", 
        "Eastern European", "European", "French", "German", "Greek", "Indian", "Irish", 
        "Italian", "Japanese", "Jewish", "Korean", "Latin American", "Mediterranean", 
        "Mexican", "Middle Eastern", "Nordic", "Southern", "Spanish", "Thai",
        "Vietnamese"
    ];
    const dietsList = [
        "Vegetarian", "Vegan", "Lacto-Vegetarian", "Ovo-Vegetarian", 
        "Pescetarian", "Gluten Free", "Ketogenic", "Paleo", "Primal",
        "Low FODMAP", "Whole30"
    ];
    const intoleranceList = [
        "Dairy", "Egg", "Gluten", "Grain", "Peanut", "Seafood", "Sesame", 
        "Shellfish", "Soy", "Sulfite", "Tree Nut", "Wheat"
    ];
    const constFilterLists = new Map([["cuisine", cuisineList], ["diet", dietsList], ["intolerances", intoleranceList]]);
    
    //The state of each filter stored in "filter name" => "filter options list" mapping
    //True for an option means the user has toggled that option. The order of lists and options are the same as in the constant lists above.
    const [selectedFiltersBitMaps, setSelectedFiltersBitMaps] = useState(new Map((Array.from(constFilterLists).map(nameToListMapping => [nameToListMapping[0], new Array(nameToListMapping[1].length).fill(false)]))));
    
    function updateFilterBitMap (filterTypeName, filterOptionName) {
        //find position of a filter option then invert its truthiness
        const optionIndex = constFilterLists.get(filterTypeName).indexOf(filterOptionName);
        let tempFilterLists = new Map(selectedFiltersBitMaps);
        tempFilterLists.get(filterTypeName)[optionIndex] = !tempFilterLists.get(filterTypeName)[optionIndex];
        setSelectedFiltersBitMaps(tempFilterLists);
    }
    const [ingredients, setIngredients] = useState([]);

    //Represents whether an ingredient on the ingredient list is to be included or excluded. True represents included, false represents excluded.
    const [ingredientsIncludeBitMap, setIngredientsIncludeBitMap] = useState([]);
    const [includeToggle, setIncludeToggle] = useState(true); //True if toggle currently set to include chosen ingredients.
    function checkIfSaved(recipes) {
        const recipeIDs = recipes.map(recipe => recipe["id"]);
        const favoritesCopy = new Array(recipes.length).fill(false);
        const serverBaseURLString = "http://localhost:8080";
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
                favoritesCopy[recipeIDs.indexOf(savedRecipe["id"])] = true;
            });
            setFavoritedRecipesBitMap(favoritesCopy);
        })
        .catch(error => console.log(error));
    }

    const serverBaseURLString = "http://localhost:8080";
    let serverBaseURL = new URL(serverBaseURLString);

    function handleSubmit() {
        let recipeEndpoint = new URL("recipes", serverBaseURL);

        // if (ingredients.length > 0) 
        const includeIngredients = [];
        const excludeIngrendients = [];
        ingredients.forEach((ingredient, i) => ingredientsIncludeBitMap[i] == true ? 
                            includeIngredients.push(ingredient) : excludeIngrendients.push(ingredient)
        )
        recipeEndpoint.searchParams.append("includeIngredients", includeIngredients.join());
        recipeEndpoint.searchParams.append("excludeIngredients", excludeIngrendients.join());
        selectedFiltersBitMaps.forEach((bitMap, filterType) => {
            const selectedOptions = [];
            bitMap.forEach((optionIsSelected, i) => { 
                if (optionIsSelected) selectedOptions.push(constFilterLists.get(filterType)[i]);
            });
            if(selectedOptions.length > 0) {
                recipeEndpoint.searchParams.append(filterType, selectedOptions.join());
            }
        });

        const options = {
            method: "GET",
        };
        const tempArr = [];
        fetch(recipeEndpoint, options)
        .then(response => response.json())
        .then(data => {
            data.forEach(recipe => tempArr.push(recipe));
            setRecipes(tempArr);
            sessionStorage.setItem("recipes", JSON.stringify(tempArr));
            if(isLoggedIn) checkIfSaved(tempArr);
        })
        .catch(error => console.log(error));
    }

    return <div className="get-recipe-section">
        <div className = "additional-filters-side-panel">
            <AdditionalFiltersAccordion constFilterLists={constFilterLists} updateFilterBitMap={updateFilterBitMap}/>
        </div>
        <div className="get-recipe-main">
            <div className="get-recipe-guide">Find recipes by their ingredients</div>
            <InputTextArea ingredients={ingredients} setIngredients={setIngredients} ingredientNameList={ingredientNameList} includeToggle={includeToggle} 
                        setIncludeToggle={setIncludeToggle} ingredientsIncludeBitMap={ingredientsIncludeBitMap} setIngredientsIncludeBitMap={setIngredientsIncludeBitMap} handleSubmit={handleSubmit}/>
            <IngredientList ingredients={ingredients} setIngredients={setIngredients} ingredientsIncludeBitMap={ingredientsIncludeBitMap}/>
            <SubmitButton handleSubmit={handleSubmit}/>
        </div>
    </div>
}

function InputTextArea({ingredients, setIngredients, ingredientNameList, includeToggle, setIncludeToggle, ingredientsIncludeBitMap, setIngredientsIncludeBitMap, handleSubmit}) {
    const [inputVal, setInputVal] = useState(""); //current text on the searchbar
    const [dropdownIndex, setDropdownIndex] = useState(-1); //specifies which dropdown recipe is highlighted
    const highlightedRef = useRef(null);
    const matchingIngredients = ingredientNameList.filter(name => name.includes(inputVal.toLowerCase()));
    const exactMatchPos = matchingIngredients.indexOf(inputVal.toLowerCase());
    if (exactMatchPos > 0)  {
        matchingIngredients.splice(exactMatchPos, 1);
        matchingIngredients.unshift(inputVal.toLowerCase());
    }

    function pushIngredient (ingredient) {
        ingredient = ingredient.toLowerCase();
        if(ingredients.indexOf(ingredient) >= 0) return;
        const ingredientArrCopy = ingredients.slice();
        ingredientArrCopy.push(ingredient);
        setIngredients(ingredientArrCopy);
        const includeMapCopy = ingredientsIncludeBitMap.slice();
        includeMapCopy.push(includeToggle);
        setIngredientsIncludeBitMap(includeMapCopy);
        setInputVal(""); // clear input field after adding
    }

    function keyUpEvent(e, ingredient) {
        const key = e.key;
        if(key === 'Enter') {
            if (ingredient.length == 0) {
                handleSubmit();
            } else if (dropdownIndex >= 0 && matchingIngredients.length > 0) {
                pushIngredient(matchingIngredients[dropdownIndex]);
            } else {
                pushIngredient(ingredient);
            }
        } 
    }

    function keyDownEvent(e) {
        function scrollDropdownBy (px) {
            highlightedRef?.current?.parentElement.scrollBy({ top: px, behavior: 'instant'})
        }
        function scrollDownToHighlighted (scrollingDown) {
            const highlightedObj = highlightedRef?.current;
            const sibling = scrollingDown ? highlightedObj?.nextElementSibling : highlightedObj?.previousElementSibling;
            sibling?.scrollIntoView({ behavior: "smooth", block: "nearest"});
        }

        const key = e.key;
        const scrollPx = 29;
        if (key === 'ArrowDown') {
            if(e.repeat) {
                scrollDropdownBy(scrollPx);
            } else {
                scrollDownToHighlighted(true);
            }
            setDropdownIndex(Math.min(matchingIngredients.length - 1, dropdownIndex + 1));
        } else if (key === 'ArrowUp') {
            setDropdownIndex(Math.max(-1, dropdownIndex - 1));
            if(e.repeat) {
                scrollDropdownBy(-1 * scrollPx);
            } else {
                scrollDownToHighlighted(false);
            }
        }
    }

    return <label className="textArea">
        <select onChange={e => setIncludeToggle(e.target.value)}>
            <option value={true}>Include</option>
            <option value={false}>Exclude</option>
        </select>
        <div className="input-prompt">Ingredient:</div>
        <div className="text-with-dropdown" >
            <input className="ingredientSearchBar"
                type="text" 
                name = "Ingredient Search Bar"
                value={inputVal} // control input
                onChange={e => {setInputVal(e.target.value); setDropdownIndex(-1);}}
                onKeyUp={e => keyUpEvent(e, inputVal)}
                onKeyDown={e => keyDownEvent(e)}
                autoComplete="off" // disable browser autocomplete
            />
            <AutocompleteDropdown currentText={inputVal} matchingIngredients={matchingIngredients} pushIngredient={pushIngredient} dropdownIndex={dropdownIndex} highlightedRef={highlightedRef}/>
        </div>
        <button type="button" className="add-ingredient-button" onClick={() => pushIngredient(inputVal)}>Add</button>
    </label>
}

function SubmitButton({handleSubmit}) {
    return <button type="button" className="submit-button" onClick={handleSubmit}>Get Recipes</button>;
}

function IngredientList({ingredients, setIngredients, ingredientsIncludeBitMap}) {
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
                {ingredients.map(
                    (ingredient, i) => 
                    <IngredientFilterBlock key={ingredient} ingredientName={ingredient} handleClick={() => removeIngredient(ingredient)}  
                                             filterType={ingredientsIncludeBitMap[i] == true ? "includes-ingredient" : "excludes-ingredient"}/>
                )}
            </div>
        </div>
    </>
}

function IngredientFilterBlock({ingredientName,  handleClick, filterType}) {
    const classStr = "ingredient-filter-block " + filterType; 
    let croppedName = ingredientName;
    if(croppedName.length > 17) {
        croppedName = croppedName.slice(0, 17) + "...";
    }
    return <div className={classStr}><div className="ingredient-filter-text">{croppedName}</div><IngredientFilterX handleClick={handleClick}/></div>;
}

function IngredientFilterX({handleClick}) {
    return <button className="ingredient-filter-x" onClick={handleClick}>&#10006;</button>;
}

function AutocompleteDropdown ({currentText, pushIngredient, matchingIngredients, dropdownIndex, highlightedRef}) { 
        if(currentText.length < 3) return <></>
        
        return <ul className="input-text-dropdown">
             {
             matchingIngredients.length > 0 ? 
             matchingIngredients.map((ingredientName, i) => 
             <DropdownItem ingredientName={ingredientName} key={ingredientName} pushIngredient={pushIngredient} 
                           dropdownIndex={dropdownIndex} i={i} highlightedRef={highlightedRef}/>) :
             <DropdownItem ingredientName={"No ingredient found"} pushIngredient={()=>null} i={-1}/>}
        </ul>
}

function DropdownItem ({ingredientName, pushIngredient, dropdownIndex, i, highlightedRef}) {
    const cls = clsx('dropdown-item', {'highlighted': dropdownIndex == i}, {'no-match': !highlightedRef});
    if(dropdownIndex == i) {
        return <li className={cls} onClick={()=>pushIngredient(ingredientName)} ref={highlightedRef}>{ingredientName}</li>
    } else {
        return <li className={cls} onClick={()=>pushIngredient(ingredientName)}>{ingredientName}</li>
    }
}