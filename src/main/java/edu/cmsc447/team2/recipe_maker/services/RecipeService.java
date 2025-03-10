package edu.cmsc447.team2.recipe_maker.services;

import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;

public interface RecipeService {
    RecipeEntity createRecipe(RecipeEntity recipeEntity);
}
