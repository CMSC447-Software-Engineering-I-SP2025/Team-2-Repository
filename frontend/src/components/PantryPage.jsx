import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';

export default function PantryPage({uniqueIngredientNames, ingredientObjs}) {
    // const [ingredients, setIngredients] = useState([
    //     { name: 'Chicken', quantity: "2 Whole lbs" },
    //     { name: 'Rice', quantity: "1 Cup" },
    //     { name: 'Broccoli', quantity: "1 Bunch"},
    //     { name: 'Olive Oil', quantity: "1 Tbsp"},
    // ]);
    const commonVolumeUnits = ["cup", "tsp", "tbsp", "L", "mL", "qt", "pt", "gal", "fl oz"]
    const commonWeightUnits = ["kg", "g", "mg", "lb", "oz"]
    const [ingredients, setIngredients] = useState([]);
    const [quickAddGroups, setQuickAddGroups] = useState({});
    const [filteredSuggestions, setFilteredSuggestions] = useState([]);
    const [newIngredient, setNewIngredient] = useState({ id: '', name: '', quantity: '', unit: '-- unit --'});
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [loggedIn, setLoggedIn] = useState(false);

    //bit maps representing whether table ingredient at that row index is currently being edited
    const [isEditingQuantity, setIsEditingQuantity] = useState([]); 
    const [isEditingUnit, setIsEditingUnit] = useState([]);

    const serverBaseURLString = "http://localhost:8080";
    const serverBaseURL = new URL(serverBaseURLString);

    function getIngredientByName(name) {
        return ingredientObjs.find(ing => ing.name == name.toLowerCase());
    }
    function saveIngredient(ingredient) {
        const processedIngredient = {... ingredient}
        if(!ingredient.id) {
            processedIngredient.id = getIngredientByName(ingredient.name).id;
        }
        if(isNaN(ingredient.quantity)) {
            ingredient.quantity = '-';
        }
        if(processedIngredient.quantity) {
            //renaming before sending off because of different naming conventions
            const tempAmount = ingredient.quantity;
            processedIngredient.amount = tempAmount;
            delete processedIngredient.quantity;
        }

        let saveIngredientEndpoint = new URL("addingredient", serverBaseURL);
        const options = {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(processedIngredient)
        };
        fetch(saveIngredientEndpoint, options)
        .catch(error => console.log(error));
    }

    function removeIngredient(ingredient, index) {
        setIngredients(prev => prev.filter((_, i) => i !== index));
        const tempEditQuantity = isEditingQuantity.slice();
        tempEditQuantity.splice(index, 1);
        setIsEditingQuantity(tempEditQuantity);
        const tempEditUnit = isEditingUnit.slice();
        tempEditUnit.splice(index, 1);
        setIsEditingUnit(tempEditUnit);

        let removeIngredientEndpoint = new URL("removeingredient", serverBaseURL);
        const options = {
            method: "DELETE",
            credentials: "include",
            body: ingredient.id
        };
        fetch(removeIngredientEndpoint, options)
        .catch(error => console.log(error));
    }

    // Fetch and parse CSV data. Fetch saved ingredients.
    useEffect(() => {
        fetch("/ingredient_list_by_category.csv")
            .then(res => res.text())
            .then(csvText => {
                Papa.parse(csvText, {
                    header: true,
                    skipEmptyLines: true, // Avoid empty rows in the CSV
                    complete: function(results) {
                        const categorizedData = results.data.reduce((acc, row) => {
                            const category = row["Category"];
                            const ingredient = row["Ingredient"];
                            if (category && ingredient) {
                                if (!acc[category]) {
                                    acc[category] = [];
                                }
                                acc[category].push(ingredient);
                            }
                            return acc;
                        }, {});

                        // Set the data in state
                        setQuickAddGroups(categorizedData);
                    },
                    error: (error) => console.error("Error parsing CSV:", error), // Handle errors gracefully
                });
            })
            .catch((err) => console.error("Error fetching CSV file:", err)); // Handle fetch errors

            //Fetching the list of saved ingredients.
            const serverBaseURLString = "http://localhost:8080";
            let serverBaseURL = new URL(serverBaseURLString); 
            let listIngredientsEndpoint = new URL("listingredients", serverBaseURL);
            const options = {
                method: "GET",
                credentials: "include"
            };
            fetch(listIngredientsEndpoint, options)
            .then(response => {
                if(response.status == 401) {
                    setLoggedIn(false);
                    throw new Error(`401 - Not authenticated`);
                }
                setLoggedIn(true);
                return response.json();
            })
            .then(data => {
                const tempIngredients = data.map(savedIngredient => ({name: savedIngredient.name, quantity: savedIngredient.amount, unit: savedIngredient.unit}));
                setIngredients(tempIngredients);
                const prefilledArray = new Array(tempIngredients.length);
                prefilledArray.fill(false);
                setIsEditingQuantity(prefilledArray)
                setIsEditingUnit(prefilledArray)
                setLoggedIn(true);
            })
            .catch(error => console.log(error));
    }, []);

    // Add ingredient to the list
    const handleQuickAdd = (name) => {
        if (!ingredients.find(ing => ing.name == name)) {
            const ingredient = getIngredientByName(name);
            saveIngredient(ingredient);
            setIngredients((prev) => [...prev, { name, quantity: "-"}]);
            setIsEditingQuantity([...isEditingQuantity, false]);
            setIsEditingUnit([...isEditingUnit, false]);
        }
    };

    // Filter suggestions based on input
    useEffect(() => {
        const input = newIngredient.name.toLowerCase();
        if (input) {
            const matches = Object.values(uniqueIngredientNames) //id, name
                .filter(item => item.toLowerCase().includes(input))
            setFilteredSuggestions(matches);
            setShowSuggestions(true);
        } else {
            setFilteredSuggestions([]);
            setShowSuggestions(false);
        }
    }, [newIngredient.name]);

    // Add new ingredient with validation (now allowing for missing quantity)
    const handleAddIngredient = () => {

        if (ingredients.find(ing => ing.name == newIngredient.name)) {
            return;
        }

        if(parseFloat(newIngredient.quantity) <= 0) {
            return;
        }
    
        const ingredientToAdd = getIngredientByName(newIngredient.name)
        ingredientToAdd.quantity = newIngredient.quantity.trim() || "-";
        if (!["-- unit --", "n/a"].includes(newIngredient.unit)) {
            ingredientToAdd.unit = newIngredient.unit
        } else {
            ingredientToAdd.unit = "-"
        }
    
        if (ingredientToAdd.name) {
            saveIngredient(ingredientToAdd);
            setIngredients((prev) => [...prev, ingredientToAdd]);
            setIsEditingQuantity([...isEditingQuantity, false]);
            setIsEditingUnit([...isEditingUnit, false]);
            setNewIngredient({ id: '', name: '', quantity: '', unit: '-- unit --' });
        }
    };

    return (
        loggedIn ?
        <div className="pantry-page">
            <div className="quick-add">
                <h2>Add Ingredients</h2>
                <input
                    type="text"
                    placeholder="Ingredient Name"
                    value={newIngredient.name}
                    onChange={(e) => setNewIngredient({ ...newIngredient, name: e.target.value })}
                    onFocus={() => setShowSuggestions(true)}
                />
                {showSuggestions && filteredSuggestions.length > 0 && (
                    <ul className="suggestions-list">
                        {filteredSuggestions.map((suggestion, index) => (
                            <li
                                key={index}
                                onMouseDown={() => {
                                    setNewIngredient({ ...newIngredient, name: suggestion });
                                    setShowSuggestions(false);
                                }}
                            >
                                {suggestion}
                            </li>
                        ))}
                    </ul>
                )}
                <input
                    style={{width: "8rem"}}
                    type="number"
                    step="any"
                    min="0"
                    max="10000"
                    placeholder="Quantity (optional)"
                    value={newIngredient.quantity}
                    onChange={(e) => setNewIngredient({ ...newIngredient, quantity: e.target.value })}
                />
                <select
                    value={newIngredient.unit}
                    onChange={(e) => setNewIngredient({ ...newIngredient, unit: e.target.value })}
                >
                    <option disabled defaultValue> -- unit -- </option>
                    <option>n/a</option>
                    <optgroup label="volume">
                        {commonVolumeUnits.map(unit => <option key={unit}>{unit}</option>)}
                    </optgroup>
                    <optgroup label="weight">
                        {commonWeightUnits.map(unit => <option key={unit}>{unit}</option>)}
                    </optgroup>
                </select>

                <button onClick={handleAddIngredient}>Add Ingredient</button>

                {/* Display categorized quick-add buttons */}
                {Object.entries(quickAddGroups).map(([category, items]) => (
                    <div key={category} className="category-container">
                        <h3>{category}</h3>
                        <div className="button-container">
                            {items.map((item, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => handleQuickAdd(item)}
                                    className="quick-add-button"
                                >
                                    {item}
                                </button>
                            ))}
                        </div>
                    </div>
                ))}

            </div>

            <div className="ingredient-list">
                <h2>My Pantry</h2>
                <table style={{ width: '100%', marginTop: '1rem', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr>
                            <th>Ingredient</th>
                            <th>Quantity</th>
                            <th>Unit</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {ingredients.map((ingredient, index) => (
                            <tr key={index}>
                                <td style={{textTransform: 'capitalize'}}>{ingredient.name}</td>
                                <td className='measurement-column'>{ingredient.quantity ? ingredient.quantity : "-"}</td>
                                <td className='measurement-column'>{ingredient.unit ? ingredient.unit : "-"}</td>
                                <td>
                                    <div className='add-spacing-to-children'>
                                        {isEditingQuantity[index]
                                        ?   <input
                                                style={{width: "4rem"}}
                                                type="number"
                                                step="any"
                                                min="0"
                                                max="10000"
                                                placeholder="Quantity"
                                                defaultValue={ingredients[index].quantity}
                                                onKeyDown={(e) => {
                                                    if(e.key == "Enter") {
                                                        const newQuantity = parseFloat(e.target.value);
                                                        if (newQuantity == 0) {
                                                            removeIngredient(getIngredientByName(ingredient.name), index);
                                                        } else if (newQuantity > 0) {
                                                            const ingrsCopy = ingredients.slice();
                                                            ingrsCopy[index].quantity = newQuantity;
                                                            saveIngredient(ingrsCopy[index]);
                                                            setIngredients(ingrsCopy);

                                                            const updatedEditingQuantity = isEditingQuantity.slice();
                                                            updatedEditingQuantity[index] = false;
                                                            setIsEditingQuantity(updatedEditingQuantity);
                                                        }
                                                    } 
                                                }}   
                                            />
                                        :   <button onClick={() => {
                                                const updatedEditingQuantity = [...isEditingQuantity];
                                                updatedEditingQuantity[index] = true;
                                                setIsEditingQuantity(updatedEditingQuantity);
                                            }}>
                                                Edit Quantity
                                            </button>
                                        }
                                        {isEditingUnit[index]
                                        ?   <>
                                                <select defaultValue={ingredients[index].unit == '-' ? 'n/a' : ingredients[index].unit}>
                                                    {/* <option defaultValue value={ingredients[index].unit}> {ingredients[index].unit} </option> */}
                                                    <option value={'-'}>n/a</option>
                                                    <optgroup label="volume">
                                                        {commonVolumeUnits.map(unit => <option key={unit} value={unit}>{unit}</option>)}
                                                    </optgroup>
                                                    <optgroup label="weight">
                                                        {commonWeightUnits.map(unit => <option key={unit} value={unit}>{unit}</option>)}
                                                    </optgroup>
                                                </select>
                                            </>
                                        :   <button onClick={() => {
                                                const updatedEditingUnit = [...isEditingUnit];
                                                updatedEditingUnit[index] = true;
                                                setIsEditingUnit(updatedEditingUnit);
                                            }}>
                                                Edit Unit
                                            </button>
                                        }

                                        {(isEditingQuantity[index] || isEditingUnit[index]) &&
                                            <input 
                                                type="submit"
                                                value="Update"
                                                onClick={(e) => {
                                                    const ingrsCopy = ingredients.slice();
                                                    if(isEditingQuantity[index]) {
                                                        ingrsCopy[index].quantity = parseFloat(e.target.previousSibling.previousSibling.value);
                                                        console.log(ingrsCopy[index].quantity);
                                                        if (ingrsCopy[index].quantity == 0) {
                                                            removeIngredient(getIngredientByName(ingredient.name), index);
                                                            return;
                                                        } else if (ingrsCopy[index].quantity < 0) {
                                                            return;
                                                        }
                                                    }
                                                    if(isEditingUnit[index]) {
                                                        ingrsCopy[index].unit = e.target.previousSibling.value;
                                                    }
                                                    saveIngredient(ingrsCopy[index]);
                                                    setIngredients(ingrsCopy);
                                                    const updatedEditingQuantity = isEditingQuantity.slice();
                                                    const updatedEditingUnit = isEditingUnit.slice();
                                                    updatedEditingQuantity[index] = false;
                                                    updatedEditingUnit[index] = false;
                                                    setIsEditingQuantity(updatedEditingQuantity);  
                                                    setIsEditingUnit(updatedEditingUnit);                                                      
                                                }}
                                            />
                                        }
                                        <button onClick={() => {
                                            removeIngredient(getIngredientByName(ingredient.name), index);
                                        }}>
                                            Remove
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
        :
        <h1 style={{textAlign: 'center'}}>Not Logged In</h1>
    );
}
