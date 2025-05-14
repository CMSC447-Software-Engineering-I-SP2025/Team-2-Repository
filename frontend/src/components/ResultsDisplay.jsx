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
    // Ensure `favoritedRecipesBitMap` is valid
    const isFavorited = (favoritedRecipesBitMap && favoritedRecipesBitMap[index]) || false;
    const favorite_icon = isFavorited ? "../star-solid.svg" : "../star-regular.svg";
    const favorite_alt_text = isFavorited
        ? "A favorite recipe button set to favorited."
        : "A favorite recipe button set to not favorited.";

    function handleFavoriteClick() {
        let copyBitMap = favoritedRecipesBitMap.slice();
        if (isFavorited) {
            removeRecipe(recipe);
        } else {
            saveRecipe(recipe);
        }
        copyBitMap[index] = !isFavorited;
        setFavoritedRecipesBitMap(copyBitMap);
    }

    const recipeURL = recipe.image;
    const recipeName = recipe.title;
    const resultLink = `/recipe/${recipeName.toLowerCase()}`; 

    return (
        <div className="result-cell">
            <div className="result-image-wrapper">
                <a href={resultLink}><img src={recipeURL} alt={recipeName}/></a>
                <div className="favorite-button-cut-out">
                    <img className="favorite-button" src={favorite_icon} alt={favorite_alt_text} onClick={handleFavoriteClick}/>
                </div>
            </div>
            <div className="recipe-name">
                <Link to={{ pathname: resultLink, state: recipeName }}>{recipeName}</Link>
            </div>
        </div>
    );
}
