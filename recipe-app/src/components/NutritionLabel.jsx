// Calories
// Total Fat
// Saturated Fat
// Trans Fat
// Cholestoral
// Sodium
// Total Carbohydrates
// Dietary Fiber
// Total Sugars
// Protein
// Vitamin D
// Calcium
// Iron
// Potassium

export default function NutritionLabel ({nutrition}) {
    let nutrients = {};
    const nutrientNameList = ["Calories", "Fat", "Saturated Fat", "Cholestoral", "Sodium", "Carbohydrates", 
                            "Fiber", "Sugar", "Protein", "Vitamin D", "Calcium", "Iron", "Potassium"];
    nutrientNameList.forEach(name => nutrients[name] = nutrition.find(nutrient => nutrient.name == name));
    
    return <>   
        <section id="spoonacular-nutrition-label">
            <div>
                <h1>
                    <b>Nutrition Facts</b>
                </h1>
            </div>
            <b>Amount Per Serving</b>
            <table>
            <tbody>
                <tr id="calorie-summary">
                    <td colSpan="2">
                        <b>Calories</b>
                    </td>
                    <td>
                        <b>396</b>
                    </td>
                </tr>
                <tr className="separator">
                    <td className="small" colSpan="3">
                        <b>% Daily Value*</b>
                    </td>
                </tr>
                <tr>
                    <td colSpan="2">
                        <b>Total Fat</b> 4g
                    </td>
                    <td>
                        <b>5%</b>
                    </td>
                </tr>
                <tr>
                    <td className="empty"></td>
                    <td>Saturated Fat 0.42g</td>
                    <td>
                        <b>2%</b>
                    </td>
                </tr>
                <tr>
                    <td className="empty"></td>
                    <td>
                        <i>Trans</i> Fat 0g
                    </td>
                    <td></td>
                </tr>
                <tr>
                    <td colSpan="2">
                        <b>Cholesterol</b> 0mg
                    </td>
                    <td>
                        <b>0%</b>
                    </td>
                </tr>
                <tr>
                    <td colSpan="2">
                        <b>Sodium</b> 232mg
                    </td>
                    <td>
                        <b>10%</b>
                    </td>
                </tr>
                <tr>
                    <td colSpan="2">
                        <b>Total Carbohydrate</b> 66g
                    </td>
                    <td>
                        <b>24%</b>
                    </td>
                </tr>
                <tr>
                    <td className="empty"></td>
                    <td>Dietary Fiber 31g</td>
                    <td>
                        <b>111%</b>
                    </td>
                </tr>
                <tr>
                    <td className="empty"></td>
                    <td>Total Sugars 7g</td>
                    <td></td>
                </tr>
                <tr>
                    <td colSpan="2">
                        <b>Protein</b> 26g
                    </td>
                    <td>
                        <b>51%</b>
                    </td>
                </tr>
            </tbody>    
            </table>
        <div className="separator"></div>
            <table>
            <tbody>
                <tr>
                    <td>Vitamin D 0mcg</td>
                    <td> 0% </td>
                </tr>
                <tr>
                    <td>Calcium 89mg </td>
                    <td> 7% </td>
                </tr>
                <tr>
                    <td>Iron 8mg</td>
                    <td> 45% </td>
                </tr>
                <tr>
                    <td>Potassium 1131mg</td>
                    <td> 24% </td>
                </tr>
                <tr className="separator">
                            <td className="small" colSpan="2">*The % Daily Value tells you how much a nutrient in a serving of food contributes to a daily diet. 2,000 calories a day is used for general nutrition advice.</td>
                </tr>
            </tbody>
            </table>
        </section>
        <section id="spoonacular-nutrition-ingredient-list">
            <b>Ingredients:</b>
            pepper, brown sugar, carrots, celery, herbs, garlic, grapeseed oil, lemon juice, lentils, onion, red wine vinegar, salt, tomatoes, and water
        </section>
    </>
}