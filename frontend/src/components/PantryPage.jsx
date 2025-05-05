import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';

export default function PantryPage({uniqueIngredientNames, ingredientObjs}) {
    // const [ingredients, setIngredients] = useState([
    //     { name: 'Chicken', quantity: "2 Whole lbs" },
    //     { name: 'Rice', quantity: "1 Cup" },
    //     { name: 'Broccoli', quantity: "1 Bunch"},
    //     { name: 'Olive Oil', quantity: "1 Tbsp"},
    // ]);
    const [ingredients, setIngredients] = useState([]);


    const [quickAddGroups, setQuickAddGroups] = useState({});
    const [filteredSuggestions, setFilteredSuggestions] = useState([]);
    const [newIngredient, setNewIngredient] = useState({ id: '', name: '', quantity: ''});
    const [showSuggestions, setShowSuggestions] = useState(false);


    const serverBaseURLString = "http://localhost:8080";
    const serverBaseURL = new URL(serverBaseURLString);

    function getIDNamePairByName(name) {
        return ingredientObjs.find(idNamePair => idNamePair.name == name.toLowerCase());
    }
    function saveIngredient(ingredient) {
        console.log(ingredient);
        let saveIngredientEndpoint = new URL("addingredient", serverBaseURL);
        const options = {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(ingredient)
        };
        fetch(saveIngredientEndpoint, options)
        .catch(error => console.log(error));
    }

    function removeIngredient(ingredient) {
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
            .then(response => response.json())
            .then(data => {
                const tempIngredients = data.map(savedIngredient => ({name: savedIngredient.name, quantity: savedIngredient.quantity}));
                setIngredients(tempIngredients);
            })
            .catch(error => console.log(error));
    }, []);

    // Add ingredient to the list
    const handleQuickAdd = (name) => {
        const idName = getIDNamePairByName(name);
        saveIngredient(idName);
        setIngredients((prev) => [...prev, { name, quantity: "-"}]);
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
        // const capitalizeWords = (str) => {
        //     return str
        //         .split(' ') // Split the string into words
        //         .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()) // Capitalize each word
        //         .join(' '); // Join the words back together
        // };
        
        const ingredientToAdd = getIDNamePairByName(newIngredient.name);
        
        // const ingredientToAdd = {
        //     id: ingredientObjs.find(idNamePair => idNamePair.name == newIngredient.name.toLowerCase()).id,
        //     name: capitalizeWords(newIngredient.name.trim()), // Capitalize each word
        //     quantity: newIngredient.quantity.trim() || "-",
        // };
    
        if (ingredientToAdd.name) {
            saveIngredient(ingredientToAdd);
            setIngredients((prev) => [...prev, ingredientToAdd]);
            setNewIngredient({ id: '', name: '', quantity: '' });
        }
    };

    return (
        <div className="pantry-page">
            <div className="quick-add">
                <h2>Quick Add Ingredients</h2>
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
                    type="text"
                    placeholder="Quantity (optional)"
                    value={newIngredient.quantity}
                    onChange={(e) => setNewIngredient({ ...newIngredient, quantity: e.target.value })}
                />
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
                            <th>Edit Quantity</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {ingredients.map((ingredient, index) => (
                            <tr key={index}>
                                <td style={{textTransform: 'capitalize'}}>{ingredient.name}</td>
                                <td>{ingredient.quantity ? ingredient.quantity : "-"}</td>
                                <td>
                                    <button onClick={() => {
                                        const newQuantity = prompt("Enter new quantity:", ingredient.quantity);
                                        if (newQuantity) {
                                            const updatedIngredients = [...ingredients];
                                            updatedIngredients[index].quantity = newQuantity;
                                            setIngredients(updatedIngredients);
                                        }
                                    }}>
                                        Edit
                                    </button>
                                </td>
                                <td>
                                    <button onClick={() => {
                                        removeIngredient(getIDNamePairByName(ingredient.name));
                                        setIngredients(prev => prev.filter((_, i) => i !== index));
                                    }}>
                                        Remove
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
