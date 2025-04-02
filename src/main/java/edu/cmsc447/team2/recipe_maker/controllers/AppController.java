// Handles web routes
package edu.cmsc447.team2.recipe_maker.controllers;

// Recipes
import edu.cmsc447.team2.recipe_maker.services.RecipeService;
import edu.cmsc447.team2.recipe_maker.mappers.RecipeMapper;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;

// Ingredients
import edu.cmsc447.team2.recipe_maker.services.IngredientService;
import edu.cmsc447.team2.recipe_maker.mappers.IngredientMapper;
import edu.cmsc447.team2.recipe_maker.domain.entities.IngredientEntity;
import edu.cmsc447.team2.recipe_maker.domain.dto.IngredientDto;

// Other
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
public class AppController {
    private final RecipeService recipeService;
    private RecipeMapper<RecipeEntity, RecipeDto> recipeMapper;
    private IngredientMapper<IngredientEntity, IngredientDto> ingredientMapper;

    public AppController(RecipeService recipeService, RecipeMapper<RecipeEntity, RecipeDto> recipeMapper) {
        this.recipeService = recipeService;
        this.recipeMapper = recipeMapper;
        this.ingredientMapper = ingredientMapper;
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
    public List<RecipeEntity> listRecipes() {
        return recipeService.listRecipes();
    }

    // Add an ingredient to the pantry
    @PutMapping(path = "/addingredient")
    public void addIngredient(@RequestBody IngredientDto ingredient) {
        IngredientEntity ingredientEntity = ingredientMapper.mapFrom(ingredient);
        ingredientService.addIngredient();
    }

    // Remove an ingredient to the pantry
}



// AppController -> Service -> Repository -> Database
// AppController -> Client -> Query -> API
// DTO and Entity are the data transferred between 