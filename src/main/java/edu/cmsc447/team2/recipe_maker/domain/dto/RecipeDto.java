package edu.cmsc447.team2.recipe_maker.domain.dto;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public record RecipeDto(
    Long id,
    String image,
    // String imageType,
    String title,
    // Integer readyInMinutes,
    // Integer servings,
    // String sourceUrl,
    // Boolean vegetarian,
    // Boolean vegan,
    // Boolean glutenFree,
    // Boolean dairyFree,
    // Boolean veryHealthy,
    // Boolean cheap,
    // Boolean veryPopular,
    // Boolean sustainable,
    // Boolean lowFodmap,
    // Integer weightWatcherSmartPoints,
    // String gaps,
    // Integer preparationMinutes,
    // Integer cookingMinutes,    
    // Integer aggregateLikes,
    // Double healthScore,
    // String creditsText,
    // String license,
    // String sourceName,
    // Double pricePerServing,
    // String summary,
    // List<String> cuisines,
    // List<String> dishTypes,
    // List<String> diets,
    // List<String> occasions,
    Integer usedIngredientCount,
    Integer missedIngredientCount,
    List<InstructionDto> analyzedInstructions
    // Double spoonacularScore,
    // String spoonacularSourceUrl
) {}
