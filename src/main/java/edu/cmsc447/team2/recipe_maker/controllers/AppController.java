// Handles web routes
package edu.cmsc447.team2.recipe_maker.controllers;


import edu.cmsc447.team2.recipe_maker.mappers.GenericMapper;

// Recipes
import edu.cmsc447.team2.recipe_maker.services.RecipeService;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;

// Ingredients
import edu.cmsc447.team2.recipe_maker.services.IngredientService;
import edu.cmsc447.team2.recipe_maker.domain.entities.IngredientEntity;
import edu.cmsc447.team2.recipe_maker.domain.dto.IngredientDto;

// Other
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
public class AppController {

    // Instantiate mappers and services
    private final RecipeService recipeService;
    private final IngredientService ingredientService;
    private GenericMapper<RecipeEntity, RecipeDto> recipeMapper;
    private GenericMapper<IngredientEntity, IngredientDto> ingredientMapper;


    // Add mappers and services to the controller
    public AppController(
    RecipeService recipeService,
    IngredientService ingredientService,
    GenericMapper<RecipeEntity, RecipeDto> recipeMapper,
    GenericMapper<IngredientEntity, IngredientDto> ingredientMapper) {
        this.recipeService = recipeService;
        this.ingredientService = ingredientService;
        this.recipeMapper = recipeMapper;
        this.ingredientMapper = ingredientMapper;
    }

    // Define paths
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
    public List<RecipeDto> getRecipe(
            @RequestParam(value = "includeIngredients", required = true) String includeIngredients,
            @RequestParam(value = "excludeIngredients", required = false) String excludeIngredients,
            @RequestParam(value = "cuisine", required = false) String cuisineType,
            @RequestParam(value = "intolerances", required = false) String intolerances,
            @RequestParam(value = "diet", required = false) String diet)
    {
        return recipeService.getRecipes(includeIngredients, excludeIngredients, cuisineType, intolerances, diet);
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
    public List<RecipeEntity> listRecipes() {
        return recipeService.listRecipes();
    }

    // Add an ingredient to the pantry
    @PutMapping(path = "/addingredient")
    public void addIngredient(@RequestBody IngredientDto ingredient) {
        IngredientEntity ingredientEntity = ingredientMapper.mapFrom(ingredient);
        ingredientService.addIngredient(ingredientEntity);
    }

    // Remove an ingredient from the pantry
    @DeleteMapping(path = "/removeingredient")
    public void removeingredient(@RequestBody long ingredientID) {
        ingredientService.removeingredient(ingredientID);
    }

    // List all ingredients
    @DeleteMapping(path = "/listingredients") 
    public void removeingredient() {
        ingredientService.listIngredients();
    }
}



// AppController -> Service -> Repository -> Database
// AppController -> Client -> Query -> API
// DTO and Entity are the data transferred between 

/* Two options
 * 1. Filter by selected ingredients
 * 2. Filter by pantry ingredients
 * 
 * 
 * 
 */