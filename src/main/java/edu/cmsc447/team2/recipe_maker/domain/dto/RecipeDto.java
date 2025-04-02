package edu.cmsc447.team2.recipe_maker.domain.dto;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public record RecipeDto(
    Long id,
    String image,
    String title,
    Integer usedIngredientCount,
    Integer missedIngredientCount,
    List<InstructionDto> analyzedInstructions
) {}
