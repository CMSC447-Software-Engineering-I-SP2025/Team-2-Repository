export default function ResultsDisplay () {
    const images = ["/chicken_pot_pie.jpeg", "/chicken_cacciatore.webp", "/green-chili-stew.webp", "/ground-beef.jpg", "https://img.spoonacular.com/recipes/632660-312x231.jpg"];

    return <div className="results-section">
        {/* <div>Results</div> */}
        <div id="results-grid">
            {images.slice(0,9).map((image) => <ResultsCell recipeURL={image} key={image}/>)}
        </div>
    </div>
}

function ResultsCell({recipeURL}) {
    return <div ><img src={recipeURL} /></div>;
}
