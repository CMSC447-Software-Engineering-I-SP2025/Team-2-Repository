// Display results from a recipe search in a grid

export default function ResultsDisplay ({recipes}) {    
    return <div className="results-section">
        <div className="results-grid">
                {recipes.slice(0,15).map((recipe) => 
                <ResultsCell recipeURL={recipe.image} recipeName={recipe.title} key={recipe.title}/>)}
        </div>
    </div>
}

function ResultsCell({recipeURL, recipeName}) {
    //had to remove the hypen formatting because it messed with recipes with hyphens -SL
    const resultLink = `/recipe/${recipeName.toLowerCase()}`; 

    return <div className="result-cell"><a href={resultLink}> <img src ={recipeURL} alt={recipeName}/> </a><div> <a href={resultLink}> {recipeName} </a></div></div>;
}