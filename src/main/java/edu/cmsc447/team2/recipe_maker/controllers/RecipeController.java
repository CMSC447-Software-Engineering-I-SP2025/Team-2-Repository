// Handles web routes
package edu.cmsc447.team2.recipe_maker.controllers;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import edu.cmsc447.team2.recipe_maker.mappers.RecipeMapper;
import edu.cmsc447.team2.recipe_maker.services.RecipeService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class RecipeController {
    private final RecipeService recipeService;
    private RecipeMapper<RecipeEntity, RecipeDto> recipeMapper; //Maps between Entity and Dto

    public RecipeController(RecipeService recipeService, RecipeMapper<RecipeEntity, RecipeDto> recipeMapper) {
        this.recipeService = recipeService;
        this.recipeMapper = recipeMapper;
    }

    // Map a RecipeDto to a RecipeEntity
    @PutMapping(path = "/recipes")
    public RecipeDto addRecipe(@RequestBody RecipeDto recipe) {
        RecipeEntity recipeEntity = recipeMapper.mapFrom(recipe);
        RecipeEntity savedRecipesEntity = recipeService.createRecipe(recipeEntity);
        return recipeMapper.mapTo(savedRecipesEntity);
    }

    // Query the API for recipes with the listed ingredients
    @GetMapping(path = "/recipes")
    @CrossOrigin(origins="http://localhost:5173")
    public List<RecipeDto> getRecipe(@RequestParam String ingredients) {
        return recipeService.getRecipes(ingredients);
    }

    // Save a recipe to the database
    @PutMapping(path = "/saverecipe")
    public RecipeEntity saveRecipe(@RequestBody RecipeDto recipe) {
        RecipeEntity recipeEntity = recipeMapper.mapFrom(recipe);
        return recipeService.saveRecipe(recipeEntity);
    }

    // Remove a recipe from the database
    @DeleteMapping(path = "/deleterecipe")
    public void deleteRecipe(@RequestBody long recipeID) {
        recipeService.deleteRecipe(recipeID);
    }

    // Get all saved recipes
    @GetMapping(path = "/listrecipes")
    List<RecipeEntity> listRecipes() {
        return recipeService.listRecipes();
    }  
}
