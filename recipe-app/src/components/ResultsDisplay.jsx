import { Link } from "react-router-dom";

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
    const resultLink = `/recipe/${recipeName.replace(/\s+/g, "-").toLowerCase()}`;
    return <div className="result-cell"><a href={resultLink}> <img src ={recipeURL} alt={recipeName}/> </a><div> <a href={resultLink}> {recipeName} </a></div></div>;
}