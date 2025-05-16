export default function NutritionLabel ({nutrientsRaw, servings}) {
    let nutrients = {};
    const nutrientNameList = ["Calories", "Fat", "Saturated Fat", "Trans Fat", "Cholesterol", "Sodium", "Carbohydrates", 
                            "Fiber", "Sugar", "Protein", "Vitamin D", "Calcium", "Iron", "Potassium"];
    nutrientNameList.forEach(name => {
        nutrients[name] = nutrientsRaw.find(nutrient => nutrient.name == name);
        if(nutrients[name]) {
            nutrients[name].amount = Math.round(nutrients[name].amount);
            nutrients[name].percentOfDailyNeeds = Math.round(nutrients[name].percentOfDailyNeeds);
        } else {
            nutrients[name] = {};
            nutrients[name].amount = 0;
            nutrients[name].percentOfDailyNeeds = 0;
            if (["Fat", "Saturated Fat", "Trans Fat", "Carbohydrates", "Fiber", "Sugar", "Protein"].includes(name)) {
                nutrients[name].unit = "g";
            } else {
                nutrients[name].unit = "mg";
            }
        }
    });

    function DisplayQuantity (nutrientName) {
        return nutrients[nutrientName]["amount"] + nutrients[nutrientName]["unit"];
    }
    
    return <>   
        <section id="spoonacular-nutrition-label">
            <div>
                <h1>
                    <b>Nutrition Facts</b>
                </h1>
                <hr />
                <div>
                    {servings + ((servings == 1) ? " Serving": " Servings")} Per Recipe
                </div>
            </div>
            <b>Amount Per Serving</b>
            <table>
            <tbody>
                <tr id="calorie-summary">
                    <td colSpan="2">
                        <b>Calories</b>
                    </td>
                    <td>
                        <b>{nutrients["Calories"]["amount"]}</b>
                    </td>
                </tr>
                <tr className="separator">
                    <td className="small" colSpan="3">
                        <b>% Daily Value*</b>
                    </td>
                </tr>
                <tr>
                    <td colSpan="2">
                        <b>Total Fat</b> {DisplayQuantity("Fat")}
                    </td>
                    <td>
                        <b>{nutrients["Fat"]["percentOfDailyNeeds"]}%</b>
                    </td>
                </tr>
                <tr>
                    <td className="empty"></td>
                    <td>Saturated Fat {DisplayQuantity("Saturated Fat")}</td>
                    <td>
                        <b>{nutrients["Saturated Fat"]["percentOfDailyNeeds"]}%</b>
                    </td>
                </tr>
                <tr>
                    <td className="empty"></td>
                    <td>
                        <i>Trans</i> Fat {DisplayQuantity("Trans Fat")}
                    </td>
                    <td></td>
                </tr>
                <tr>
                    <td colSpan="2">
                        <b>Cholesterol</b> {DisplayQuantity("Cholesterol")}
                    </td>
                    <td>
                        <b>{nutrients["Cholesterol"]["percentOfDailyNeeds"]}%</b>
                    </td>
                </tr>
                <tr>
                    <td colSpan="2">
                        <b>Sodium</b> {DisplayQuantity("Sodium")}
                    </td>
                    <td>
                        <b>{nutrients["Sodium"]["percentOfDailyNeeds"]}%</b>
                    </td>
                </tr>
                <tr>
                    <td colSpan="2">
                        <b>Total Carbohydrate</b> {DisplayQuantity("Carbohydrates")}
                    </td>
                    <td>
                        <b>{nutrients["Carbohydrates"]["percentOfDailyNeeds"]}%</b>
                    </td>
                </tr>
                <tr>
                    <td className="empty"></td>
                    <td>Dietary Fiber {DisplayQuantity("Fiber")}</td>
                    <td>
                        <b>{nutrients["Fiber"]["percentOfDailyNeeds"]}%</b>
                    </td>
                </tr>
                <tr>
                    <td className="empty"></td>
                    <td>Total Sugars {DisplayQuantity("Sugar")}</td>
                    <td></td>
                </tr>
                <tr>
                    <td colSpan="2">
                        <b>Protein</b> {DisplayQuantity("Protein")}
                    </td>
                    <td>
                        <b>{nutrients["Protein"]["percentOfDailyNeeds"]}%</b>
                    </td>
                </tr>
            </tbody>    
            </table>
        <div className="separator"></div>
            <table>
            <tbody>
                <tr>
                    <td>Vitamin D {DisplayQuantity("Vitamin D")}</td>
                    <td> {nutrients["Vitamin D"]["percentOfDailyNeeds"]}% </td>
                </tr>
                <tr>
                    <td>Calcium {DisplayQuantity("Calcium")} </td>
                    <td> {nutrients["Calcium"]["percentOfDailyNeeds"]}% </td>
                </tr>
                <tr>
                    <td>Iron {DisplayQuantity("Iron")}</td>
                    <td> {nutrients["Iron"]["percentOfDailyNeeds"]}% </td>
                </tr>
                <tr>
                    <td>Potassium {DisplayQuantity("Potassium")}</td>
                    <td> {nutrients["Potassium"]["percentOfDailyNeeds"]}% </td>
                </tr>
                <tr className="separator">
                            <td className="small" colSpan="2">*The % Daily Value tells you how much a nutrient in a serving of food contributes to a daily diet. 2,000 calories a day is used for general nutrition advice.</td>
                </tr>
            </tbody>
            </table>
        </section>
        {/* <section id="spoonacular-nutrition-ingredient-list">
            <b>Ingredients:</b>
            pepper, brown sugar, carrots, celery, herbs, garlic, grapeseed oil, lemon juice, lentils, onion, red wine vinegar, salt, tomatoes, and water
        </section> */}
    </>
}
