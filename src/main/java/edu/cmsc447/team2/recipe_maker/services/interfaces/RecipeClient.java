package edu.cmsc447.team2.recipe_maker.services.interfaces;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;

import java.util.List;

public interface RecipeClient {

    //Use Dto on presentation layer
    List<RecipeDto> getRecipes();
}
