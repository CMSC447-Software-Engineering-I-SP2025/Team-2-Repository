package edu.cmsc447.team2.recipe_maker.controllers;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import edu.cmsc447.team2.recipe_maker.mappers.Mapper;
import edu.cmsc447.team2.recipe_maker.services.RecipeService;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RecipeController {

    //Lets us inject recipeService into RecipeController
    private final RecipeService recipeService;

    public RecipeController(RecipeService recipeService) {
        this.recipeService = recipeService;
    }

    @PutMapping(path = "/recipes")
    public RecipeEntity addRecipe(@RequestBody RecipeEntity recipe) {
       return recipeService.createRecipe(recipe);
    }
}
