package edu.cmsc447.team2.recipe_maker.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public record Recipe(Long id, String title, Integer usedIngredientCount, Integer missedIngredientCount) { }
 //Can use a wrapper class like List<RecipeDetails> instead of individually passing in parameters
// More easily scalable
