import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ResultsDisplay from "./ResultsDisplay";
import { CATEGORY_STRUCTURE } from "./categoryData";

// Cook Time
import under10 from "../category-caches/cook-time/under-10.json";
import under30 from "../category-caches/cook-time/under-30.json";

// Cuisine
import american from "../category-caches/cuisines/american.json";
import chinese from "../category-caches/cuisines/chinese.json";
import indian from "../category-caches/cuisines/indian.json";
import japanese from "../category-caches/cuisines/japanese.json";
import korean from "../category-caches/cuisines/korean.json";
import mexican from "../category-caches/cuisines/mexican.json";

// Diets
import dairyFree from "../category-caches/diets/dairy-free.json";
import glutenFree from "../category-caches/diets/gluten-free.json";
import ketogenic from "../category-caches/diets/ketogenic.json";
import paleo from "../category-caches/diets/paleo.json";
import vegan from "../category-caches/diets/vegan.json";
import vegetarian from "../category-caches/diets/vegetarian.json";

// Dish Type
import appetizer from "../category-caches/dish-type/appetizer.json";
import breakfast from "../category-caches/dish-type/breakfast.json";
import dessert from "../category-caches/dish-type/dessert.json";
import drink from "../category-caches/dish-type/drink.json";
import fingerFood from "../category-caches/dish-type/finger-food.json";
import lunch from "../category-caches/dish-type/lunch.json";

// Season
import autumn from "../category-caches/season/autumn.json";
import spring from "../category-caches/season/spring.json";
import summer from "../category-caches/season/summer.json";
import winter from "../category-caches/season/winter.json";

function normalize(str) {
  return str.toLowerCase().replace(/\s+/g, '-');
}

const RECIPE_CACHE = {
  "cook-time": {
    "under-10-mins": under10,
    "under-30-mins": under30
  },
  cuisines: {
    american,
    chinese,
    indian,
    japanese,
    korean,
    mexican
  },
  diets: {
    "dairy-free": dairyFree,
    "gluten-free": glutenFree,
    ketogenic,
    paleo,
    vegan,
    vegetarian
  },
  "dish-type": {
    appetizer,
    breakfast,
    dessert,
    drink,
    "finger-food": fingerFood,
    lunch
  },
  season: {
    autumn,
    spring,
    summer,
    winter
  }
};

export default function CategoryPage({ saveRecipe, removeRecipe, isLoggedIn, setShowLogin }) {
  const { category, subcategory } = useParams();
  const [recipes, setRecipes] = useState([]);
  const [recipesBySubcategory, setRecipesBySubcategory] = useState({});
  const [favoritedRecipesBitMap, setFavoritedRecipesBitMap] = useState([]);
  const [loading, setLoading] = useState(true);

  function checkIfSaved(recipes) {
    const recipeIDs = recipes.map(recipe => recipe["id"]);
    const favoritesCopy = new Array(recipes.length).fill(false);
    const serverBaseURLString = "http://localhost:8080";
    let serverBaseURL = new URL(serverBaseURLString); 
    let listRecipesEndpoint = new URL("listrecipes", serverBaseURL);
    const options = {
        method: "GET",
        credentials: "include"
    };
    fetch(listRecipesEndpoint, options)
    .then(response => response.json())
    .then(data => {
        data.forEach(savedRecipe => {
            favoritesCopy[recipeIDs.indexOf(savedRecipe["id"])] = true;
        });
        setFavoritedRecipesBitMap(favoritesCopy);
    })
    .catch(error => console.log(error));
  }

  useEffect(() => {
    if (subcategory) {
      // --- Subcategory case ---
     const cache = RECIPE_CACHE[category]?.[subcategory];

    if (cache && Array.isArray(cache)) {
      const randomRecipes = cache.sort(() => 0.5 - Math.random()).slice(0, 8); // display 10 random recipes
      sessionStorage.setItem("recipes", JSON.stringify(randomRecipes));
      setRecipes(randomRecipes);
      setFavoritedRecipesBitMap(new Array(randomRecipes.length).fill(false));
      checkIfSaved(randomRecipes);
    } else {
      console.warn("No cache found for", category, subcategory);
      setRecipes([]);
      setFavoritedRecipesBitMap([]);
    }
    setLoading(false);

    } else {
      // --- Base category case ---
      const categoryEntry = CATEGORY_STRUCTURE.find(c => c.basePath.slice(1) === category);
      if (!categoryEntry) return;

      const fetchRecipesFromCache = () => {
      const tempResults = {};
      const tempFavorites = {};

      categoryEntry.links.forEach((sub) => {
        const key = normalize(sub);
        const cache = RECIPE_CACHE[category]?.[key];
        if (cache && Array.isArray(cache)) {
          const randomSubset = cache.sort(() => 0.5 - Math.random()).slice(0, 4); // display 4 random recipes
          tempResults[sub] = randomSubset;
          tempFavorites[sub] = new Array(randomSubset.length).fill(false);
        } else {
          console.warn("No cache for", category, sub);
          tempResults[sub] = [];
          tempFavorites[sub] = [];
        }
      });

      setRecipesBySubcategory(tempResults);
      setFavoritedRecipesBitMap(tempFavorites);
      setLoading(false);
    };

    fetchRecipesFromCache();
    }
  }, [category, subcategory]);

  // --- Subcategory View ---
  if (subcategory) {
    return (
      <>
        <h1 style={{ textAlign: "center", textTransform: "capitalize" }}>{subcategory} Recipes</h1>
        {loading ? (
          <p style={{ textAlign: "center" }}>Loading…</p>
        ) : recipes.length > 0 ? (
          <ResultsDisplay
            recipes={recipes}
            favoritedRecipesBitMap={favoritedRecipesBitMap}
            setFavoritedRecipesBitMap={setFavoritedRecipesBitMap}
            saveRecipe={saveRecipe}
            removeRecipe={removeRecipe}
            isLoggedIn={isLoggedIn}
            setShowLogin={setShowLogin}
          />
        ) : (
          <div style={{ textAlign: "center", color: "#A52A2A" }}>
            No recipes found for "{subcategory}". Try a different category!
          </div>
        )}
      </>
    );
  }

  // --- Base Category View ---
  return (
    <>
      {loading ? (
        <p style={{ textAlign: "center" }}>Loading…</p>
      ) : (
        Object.entries(recipesBySubcategory).map(([sub, recipes]) => (
          <div key={sub}>
            <h1 style={{ marginLeft: "1rem", textTransform: "capitalize", textAlign: "center" }}>{sub}</h1>
            {recipes.length > 0 ? (
              <ResultsDisplay
                recipes={recipes}
                favoritedRecipesBitMap={favoritedRecipesBitMap[sub]}
                setFavoritedRecipesBitMap={(newMap) =>
                  setFavoritedRecipesBitMap(prev => ({ ...prev, [sub]: newMap }))
                }
                saveRecipe={saveRecipe}
                removeRecipe={removeRecipe}
              />
            ) : (
              <div style={{ marginLeft: "0.5rem", color: "#A52A2A" }}>
                No recipes found.
              </div>
            )}
          </div>
        ))
      )}
    </>
  );
}
