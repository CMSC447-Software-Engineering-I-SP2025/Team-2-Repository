package edu.cmsc447.team2.recipe_maker.mappers;

import edu.cmsc447.team2.recipe_maker.domain.dto.IngredientDto;
import edu.cmsc447.team2.recipe_maker.domain.entities.IngredientEntity;

import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Component;

// Maps RecipeEntity to RecipeDto and back
@Component
public class IngredientMapper implements GenericMapper<IngredientEntity, IngredientDto> {

    private ModelMapper modelMapper;

    public IngredientMapper() {modelMapper = new ModelMapper();}

    public IngredientMapper(ModelMapper modelMapper) {this.modelMapper = modelMapper;}

    @Override
    public IngredientDto mapTo(IngredientEntity ingredientEntity) {return modelMapper.map(ingredientEntity, IngredientDto.class);}

    @Override
    public IngredientEntity mapFrom(IngredientDto ingredientDto) {return modelMapper.map(ingredientDto, IngredientEntity.class);}
}
