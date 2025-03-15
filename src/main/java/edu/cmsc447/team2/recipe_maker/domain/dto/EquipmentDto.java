package edu.cmsc447.team2.recipe_maker.domain.dto;

public record EquipmentDto(
    Long id,
    String name,
    String localizedName,
    String image,
    TemperatureDto temperature
) {}
