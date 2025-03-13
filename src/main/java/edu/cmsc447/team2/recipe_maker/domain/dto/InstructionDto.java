package edu.cmsc447.team2.recipe_maker.domain.dto;
import java.util.List;

public record InstructionDto(
    String name,
    List<StepDto> steps
) {}