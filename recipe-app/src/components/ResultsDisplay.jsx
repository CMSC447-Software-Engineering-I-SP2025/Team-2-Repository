export default function ResultsDisplay ({recipes}) {    
    return <div className="results-section">
        {/* <div>Results</div> */}
        <div className="results-grid">
                {recipes.slice(0,15).map((recipe) => 
                <ResultsCell recipeURL={recipe.image} recipeName={recipe.title} key={recipe.title}/>)}
        </div>
    </div>
}

function ResultsCell({recipeURL, recipeName}) {
    return <div className="result-cell"><img src={recipeURL}/><div>{recipeName}</div></div>;
}
