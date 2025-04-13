package edu.cmsc447.team2.recipe_maker.mappers;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import edu.cmsc447.team2.recipe_maker.mappers.RecipeMapper;

import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Component;

// Maps Between RecipeEntity and RecipeDto
@Component
public class RecipeMapper implements GenericMapper<RecipeEntity, RecipeDto> {

    private ModelMapper modelMapper;

    public RecipeMapper() {modelMapper = new ModelMapper();}

    public RecipeMapper(ModelMapper modelMapper) {this.modelMapper = modelMapper;}

    // RecipeEntity -> RecipeDto
    @Override
    public RecipeDto mapTo(RecipeEntity recipeEntity) {return modelMapper.map(recipeEntity, RecipeDto.class);}

    @Override
    public RecipeEntity mapFrom(RecipeDto recipeDto) {return modelMapper.map(recipeDto, RecipeEntity.class);}
}