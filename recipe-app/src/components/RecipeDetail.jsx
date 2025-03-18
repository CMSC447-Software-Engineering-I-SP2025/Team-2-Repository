import {useParams} from "react-router-dom";

export default function RecipeDetail() {
    const {recipeName} = useParams();

    // dummy data for the time being
    const recipesData = {
        "chicken-pot-pie": {
            ingredients: ["Chicken", "Pie crust", "Vegetables", "Cream"],
            steps: ["Preheat oven to 375°F", "Mix ingredients", "Bake for 30 min"],
            image: "/chicken_pot_pie.jpeg",
        },
        "chicken-cacciatore": {
            ingredients: ["Chicken", "Tomato sauce", "Garlic", "Onions"],
            steps: ["Sauté chicken", "Add sauce", "Simmer for 40 min"],
            image: "/chicken_cacciatore.webp",
        },
    };

    const recipe = recipesData[recipeName];

    return (
        <div className="recipe-detail">
            {recipe ? (
                <>
                    <h1>{recipeName.replace(/-/g, " ").toUpperCase()}</h1>
                    <img src={recipe.image} alt={recipeName} />
                    <h2>Ingredients</h2>
                    <ul>
                        {recipe.ingredients.map((item, index) => (
                            <li key={index}>{item}</li>
                        ))}
                    </ul>
                    <h2>Steps</h2>
                    <ol>
                        {recipe.steps.map((step, index) => (
                            <li key={index}>{step}</li>
                        ))}
                    </ol>
                </>
            ) : (
                <h2>Recipe not found</h2>
            )}
        </div>
    );
}