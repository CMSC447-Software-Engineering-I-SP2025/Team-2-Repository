package edu.cmsc447.team2.recipe_maker.controllers;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import edu.cmsc447.team2.recipe_maker.mappers.Mapper;
import edu.cmsc447.team2.recipe_maker.services.RecipeService;
import edu.cmsc447.team2.recipe_maker.services.impl.RecipeClientImpl;
import edu.cmsc447.team2.recipe_maker.services.interfaces.RecipeClient;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class RecipeController {

    //Lets us inject recipeService into RecipeController
    private final RecipeService recipeService;
    private final RecipeClientImpl recipeClient;

    private Mapper<RecipeEntity, RecipeDto> recipeMapper; //Maps from Entity to Dto

    public RecipeController(RecipeService recipeService, Mapper<RecipeEntity, RecipeDto> recipeMapper, RecipeClientImpl recipeClient) {
        this.recipeService = recipeService;
        this.recipeMapper = recipeMapper;
        this.recipeClient = recipeClient;
    }

    @PutMapping(path = "/recipes")
    public RecipeDto addRecipe(@RequestBody RecipeDto recipe) {
        RecipeEntity recipeEntity = recipeMapper.mapFrom(recipe);
        RecipeEntity savedRecipesEntity = recipeService.createRecipe(recipeEntity);
        return recipeMapper.mapTo(savedRecipesEntity);
    }

    @GetMapping(path = "/recipes")
    public List<RecipeDto> getRecipe() {
        //Using as a dummy for now

        return recipeClient.getRecipes();

    }
}
