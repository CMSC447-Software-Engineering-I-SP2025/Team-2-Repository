package edu.cmsc447.team2.recipe_maker.controllers;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import edu.cmsc447.team2.recipe_maker.mappers.RecipeMapper;
import edu.cmsc447.team2.recipe_maker.services.interfaces.RecipeService;
import edu.cmsc447.team2.recipe_maker.services.interfaces.RecipeClient;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class RecipeController {

    //Lets us inject recipeService into RecipeController
    private final RecipeService recipeService;
    // private final RecipeClientImpl recipeClient;

    private RecipeMapper<RecipeEntity, RecipeDto> recipeMapper; //Maps from Entity to Dto

    public RecipeController(RecipeService recipeService, RecipeMapper<RecipeEntity, RecipeDto> recipeMapper, RecipeClient recipeClient) {
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
    @CrossOrigin(origins="http://localhost:5173")
    public List<RecipeDto> getRecipe(@RequestParam String ingredients) {
        // Query the API for recipes with the listed ingredients
        return recipeService.getRecipes(ingredients);
        //return recipeClient.getRecipes(ingredients);
    }

    
    @PutMapping(path = "/saverecipe")
    public RecipeEntity saveRecipe(@RequestBody RecipeDto recipe) {
        // Function to a recipe to the database
    
        RecipeEntity recipeEntity = recipeMapper.mapFrom(recipe);
        return recipeService.saveRecipe(recipeEntity);
    }

    @DeleteMapping(path = "/deleterecipe")
    public void deleteRecipe(@RequestBody long recipeID) {
        recipeService.deleteRecipe(recipeID);
    }
}
