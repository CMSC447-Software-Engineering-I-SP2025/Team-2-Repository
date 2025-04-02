import { useState, useRef } from "react";
import clsx from 'clsx'

export default function GetRecipeSection({ingredientNameList, setRecipes}) {
    const [ingredients, setIngredients] = useState([]);
    const serverIP = "http://localhost:8080";

    function handleSubmit() {
        let requestInfo = "/recipes?";
        if (ingredients.length > 0) requestInfo += ("ingredients=" + ingredients.join());
        
        const requestURL = serverIP + requestInfo;
        const options = {
            method: "GET"
        }

        const tempArr = [];
        fetch(requestURL, options)
        .then(response => response.json())
        .then(data => {
            data.forEach(recipe => tempArr.push(recipe));
            setRecipes(tempArr);
            sessionStorage.setItem("recipes", JSON.stringify(tempArr));
        })
        .catch(error => console.log(error))
    }

    return <>
        <div className="get-recipe-section">
            <div className="get-recipe-guide">Find recipes by their ingredients</div>
            <InputTextArea ingredients={ingredients} setIngredients={setIngredients} ingredientNameList={ingredientNameList}/>
            <IngredientList ingredients={ingredients} setIngredients={setIngredients}/>
            <AdditionalFiltersAccordion />
            <SubmitButton handleSubmit={handleSubmit}/>
        </div>
    </>
}

function InputTextArea({ingredients, setIngredients, ingredientNameList}) {
    const [inputVal, setInputVal] = useState(""); //current text on the searchbar
    const [dropdownIndex, setDropdownIndex] = useState(-1); //specifies which dropdown recipe is highlighted
    const matchingIngredients = ingredientNameList.filter(name => name.includes(inputVal.toLowerCase()));
    const highlightedRef = useRef(null);

    function pushIngredient (ingredient) {
        ingredient = ingredient.toLowerCase();
        if(ingredients.indexOf(ingredient) >= 0) return;
        const ingredientArrCopy = ingredients.slice();
        ingredientArrCopy.push(ingredient);
        setIngredients(ingredientArrCopy);
    }

    function keyUpEvent(e, ingredient) {
        const key = e.key;
        if(key === 'Enter') {
            if (dropdownIndex >= 0 && matchingIngredients.length > 0) {
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
            console.log(highlightedRef.current);
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

    /*
    function handleKeyInput
    */

    return <label className="textArea">
        <div className="input-prompt">Ingredient:</div>
        <div className="text-with-dropdown" >
            <input className="ingredientSearchBar"
                type="text" 
                name = "Ingredient Search Bar"
                onChange={e => {setInputVal(e.target.value); setDropdownIndex(-1);}}
                onKeyUp={e => keyUpEvent(e, inputVal)}
                onKeyDown={e => keyDownEvent(e)}
            />
            <AutocompleteDropdown currentText={inputVal} matchingIngredients={matchingIngredients} pushIngredient={pushIngredient} dropdownIndex={dropdownIndex} highlightedRef={highlightedRef}/>
        </div>
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
                    {return <IngredientFilterBlock key={ingredient} ingredientName={ingredient} handleClick={() => removeIngredient(ingredient)}  filterType = "contains-ingredient"/>
                })}
            </div>
        </div>
    </>
}

function IngredientFilterBlock({ingredientName, filterType, handleClick}) {
    const classStr = "ingredient-filter-block " + {filterType}; 
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
        let i = 0;
        
        return <ul className="input-text-dropdown">
             {
             matchingIngredients.length > 0 ? 
             matchingIngredients.map(ingredientName => 
             <DropdownItem ingredientName={ingredientName} key={ingredientName} pushIngredient={pushIngredient} 
                           dropdownIndex={dropdownIndex} i={i++} highlightedRef={highlightedRef}/>) :
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

function AdditionalFiltersAccordion () {
    const cuisineList = [
        "Asian", "British", "Cajun", "Caribbean", "Chinese", "Eastern European",
        "European", "French", "German", "Greek", "Indian", "Irish", "Italian",
        "Japanese", "Jewish", "Korean", "Latin American", "Mediterranean", 
        "Mexican", "Middle Eastern", "Nordic", "Southern", "Spanish", "Thai",
        "Vietnamese" 
    ]
    const dietsList = [
        "Vegetarian", "Vegan", "Lacto-Vegetarian", "Ovo-Vegetarian", 
        "Pescetarian", "Gluten Free", "Ketogenic", "Paleo", "Primal",
        "Low FODMAP", "Whole30"
    ]
    const intoleranceList = [
        "Dairy", "Egg", "Gluten", "Grain", "Peanut", "Seafood", "Sesame", 
        "Shellfish", "Soy", "Sulfite", "Tree Nut", "Wheat"
    ]
    const filterLists = [["Cuisine", cuisineList], ["Diet", dietsList], ["Intolerance", intoleranceList]]

    //true means block is invisible [cusineFilterIsInvisible, dietFilterIsInvisible, intolerancesFilterIsInvisible]
    const [invisibleBlocks, setInvisibleBlocks] = useState([true, true, true]);
    function toggleVisibility(pos) {
        const arrCopy = invisibleBlocks.slice()
        arrCopy[pos] = !arrCopy[pos]
        setInvisibleBlocks(arrCopy)
    }
    return <div className="additional-filters">
        {
            filterLists.map((list, i) => 
            <AdditionalFilter invisible={invisibleBlocks[i]} toggleVisibility={() => toggleVisibility(i)}  filterOptions={list} key={list[0] + "-list"}/>)
        }
    </div>
}

function AdditionalFilter ({invisible, toggleVisibility, filterOptions}) {
    const cls = clsx('invisible-wrapper', {'invisible': invisible});
    const name = filterOptions[0]
    const list = filterOptions[1]
    return <div className="filter">
            <div className="filter-name" onClick={toggleVisibility}><div>{name}</div> <div>{invisible?<img src="angle-down-svgrepo-com.svg" alt="expand item icon"/>:<img src="angle-up-svgrepo-com.svg" alt="condense item icon"/>}</div></div>
            <div className={cls}>
                <div className="invisible-block">
                    {list.map(option => 
                        <Checkbox labelName={option} key={option} />
                    )}
                </div>
            </div>
    </div>
}

function Checkbox({labelName}) {
    return <div className="filter-item">
        <input  type="checkbox" id={labelName} name={labelName} />
        <label htmlFor={labelName}>{labelName}</label>
    </div>
}