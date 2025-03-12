package edu.cmsc447.team2.recipe_maker.domain.dto;
import java.util.List;

public record StepDto(
    Integer number,
    String step,
    List<IngredientDto> ingredients,
    List<EquipmentDto> equipment,
    LengthDto length
) {}