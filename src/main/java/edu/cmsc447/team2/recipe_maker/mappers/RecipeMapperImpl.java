package edu.cmsc447.team2.recipe_maker.mappers;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;

import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Component;

// Maps RecipeEntity to RecipeDto and back
@Component
public class RecipeMapperImpl implements RecipeMapper<RecipeEntity, RecipeDto> {

    private ModelMapper modelMapper;

    public RecipeMapperImpl() {modelMapper = new ModelMapper();}

    public RecipeMapperImpl(ModelMapper modelMapper) {this.modelMapper = modelMapper;}

    @Override
    public RecipeDto mapTo(RecipeEntity recipeEntity) {return modelMapper.map(recipeEntity, RecipeDto.class);}

    @Override
    public RecipeEntity mapFrom(RecipeDto recipeDto) {return modelMapper.map(recipeDto, RecipeEntity.class);}
}
