package edu.cmsc447.team2.recipe_maker.domain.dto;

public record IngredientDto(
    Long id,
    String name,
    String localizedName,
    String image
) {}


