package edu.cmsc447.team2.recipe_maker.domain.entities;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
// Change this stuff to change what the Spoonacular API returns.
public record RecipeEntity(
        Long id,
        String title,
        Integer usedIngredientCount,
        Integer missedIngredientCount) { }
 //Can use a wrapper class like List<RecipeDetails> instead of individually passing in parameters
// More easily scalable
