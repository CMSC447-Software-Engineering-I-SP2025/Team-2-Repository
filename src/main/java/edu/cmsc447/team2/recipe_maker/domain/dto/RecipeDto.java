package edu.cmsc447.team2.recipe_maker.domain.dto;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public record RecipeDto(
    Long id,
    String image,
    String imageType,
    String title,
    Integer readyInMinutes,
    Integer servings,
    String sourceUrl,
    Boolean vegetarian,
    Boolean vegan,
    Boolean glutenFree,
    Boolean dairyFree,
    Boolean veryHealthy,
    Boolean cheap,
    Boolean veryPopular,
    Boolean sustainable,
    Boolean lowFodmap,
    Integer weightWatcherSmartPoints,
    String gaps,
    Integer preparationMinutes, // Changed from String to Integer
    Integer cookingMinutes,    // Changed from String to Integer
    Integer aggregateLikes,
    Double healthScore,        // Changed from Integer to Double
    String creditsText,
    String license,
    String sourceName,
    Double pricePerServing,   // Changed from Integer to Double
    String summary,
    List<String> cuisines,     // Assuming cuisines is a list of strings
    List<String> dishTypes,    // Assuming dishTypes is a list of strings
    List<String> diets,       // Assuming diets is a list of strings
    List<String> occasions,    // Assuming occasions is a list of strings
    Integer usedIngredientCount,
    Integer missedIngredientCount,
    List<InstructionDto> analyzedInstructions,
    Double spoonacularScore,
    String spoonacularSourceUrl
) {}
