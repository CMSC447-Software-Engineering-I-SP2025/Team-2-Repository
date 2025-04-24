package edu.cmsc447.team2.recipe_maker.domain.dto;
import edu.cmsc447.team2.recipe_maker.domain.dto.recipe_dependencies.EquipmentDto;
import edu.cmsc447.team2.recipe_maker.domain.dto.recipe_dependencies.IngredientDto;

import java.util.List;

public record StepDto(
    Integer number,
    String step,
    List<IngredientDto> ingredients,
    List<EquipmentDto> equipment,
    LengthDto length
) {}