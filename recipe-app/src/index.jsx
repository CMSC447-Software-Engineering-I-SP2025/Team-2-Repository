// Start the app

import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";

let csvIngredientNames = [], csvIngredientPairs = [];
const root = createRoot(document.getElementById("root"));
root.render(
        <StrictMode>
            <App ingredientNameList = {csvIngredientNames} ingredientIDNamePairs = {csvIngredientPairs}/>
        </StrictMode>
)