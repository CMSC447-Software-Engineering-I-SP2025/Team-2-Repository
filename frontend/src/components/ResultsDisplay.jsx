import {Link} from 'react-router-dom';

export default function ResultsDisplay ({recipes, favoritedRecipesBitMap, setFavoritedRecipesBitMap, saveRecipe, removeRecipe}) {
    return <div className="results-section">
        <div className="results-grid">
                {recipes.slice(0,15).map((recipe, i) => 
                <ResultsCell recipe={recipe} index={i} favoritedRecipesBitMap={favoritedRecipesBitMap} setFavoritedRecipesBitMap={setFavoritedRecipesBitMap} saveRecipe={saveRecipe} removeRecipe={removeRecipe} key={recipe.title}/>)}
        </div>
    </div>
}

function ResultsCell({recipe, index, favoritedRecipesBitMap, setFavoritedRecipesBitMap, saveRecipe, removeRecipe}) {
    const recipeURL = recipe.image;
    const recipeName = recipe.title;
    const resultLink = `/recipe/${recipeName.toLowerCase()}`; 
    let favorite_icon = favoritedRecipesBitMap[index] ? "../star-solid.svg" : "../star-regular.svg";
    let favorite_alt_text = favoritedRecipesBitMap[index] ? "A favorite recipe button set to favorited." : "A favorite recipe button set to not favorited.";

    function handleFavoriteClick() {
        let copyBitMap = favoritedRecipesBitMap.slice();
        favoritedRecipesBitMap[index] ? removeRecipe(recipe) : saveRecipe(recipe);
        copyBitMap[index] = !copyBitMap[index];
        setFavoritedRecipesBitMap(copyBitMap);
    }

    return <div className="result-cell">
        <div className="result-image-wrapper">
            <a href={resultLink}><img src ={recipeURL} alt={recipeName}/></a>
            <div className="favorite-button-cut-out">
                <img className="favorite-button" src={favorite_icon} alt={favorite_alt_text} onClick={() => handleFavoriteClick()}/>
            </div>
        </div>
        <div className="recipe-name"> 
            {/* <a href={resultLink}>{recipeName}</a> */}
            <Link to={{ pathname: resultLink, state: recipeName }}>{recipeName}</Link>
        </div>
    </div>;
}