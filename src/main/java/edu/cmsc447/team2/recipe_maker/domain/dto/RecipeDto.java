package edu.cmsc447.team2.recipe_maker.domain.dto;

//Should match the Recipe class, except for the @id, @generatedvalue, @entity annotations
// No db annotations
public record RecipeDto (
    Long id,
    String title,
    Integer usedIngredientCount,
    Integer missedIngredientCount) { }
