export default function ResultsDisplay ({recipes}) {
    console.log(recipes[1]);
    const images = ["/chicken_pot_pie.jpeg", "/chicken_cacciatore.webp", "/green-chili-stew.webp", "/ground-beef.jpg", "https://img.spoonacular.com/recipes/632660-312x231.jpg"];
    
    return <div className="results-section">
        {/* <div>Results</div> */}
        <div className="results-grid">
                {recipes.slice(0,15).map((recipe) => 
                <ResultsCell recipeURL={recipe.image} recipeName={recipe.name} key={recipe.image}/>)}
        </div>
    </div>
}

function ResultsCell({recipeURL, recipeName}) {
    return <div className="result-cell"><img src={recipeURL}/><div>{recipeName}</div></div>;
}
