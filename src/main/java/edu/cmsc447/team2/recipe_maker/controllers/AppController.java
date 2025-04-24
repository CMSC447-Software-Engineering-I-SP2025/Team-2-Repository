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

import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;

import java.io.IOException;
import java.util.ArrayList;
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

    /* Define API Endpoints */


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
    @CrossOrigin(origins="http://localhost:5173")
    public RecipeEntity saveRecipe(@RequestBody RecipeDto recipe) {
        //RecipeEntity recipeEntity = recipeMapper.mapFrom(recipe);
        ObjectWriter ow = new ObjectMapper().writer();  //.withDefaultPrettyPrinter()
        String instructionsJSON = "";
        try {
            instructionsJSON = ow.writeValueAsString(recipe.analyzedInstructions());
        }
        
        catch (JsonMappingException e) {
            e.printStackTrace();
        }
        
        catch (JsonGenerationException e) {
            e.printStackTrace();}
        
        catch (IOException e) {
            e.printStackTrace();
        }

        RecipeEntity recipeEntity = new RecipeEntity(
            recipe.id(),
            recipe.title(),
            recipe.usedIngredientCount(), 
            recipe.missedIngredientCount(),
            instructionsJSON,
            recipe.image()
        );

        recipeService.saveRecipe(recipeEntity);
        return recipeEntity;
    }

    // Remove a recipe from the database
    @DeleteMapping(path = "/deleterecipe")
    @CrossOrigin(origins="http://localhost:5173")
    public void deleteRecipe(@RequestBody String recipeID) {
        recipeService.deleteRecipe(Long.valueOf(recipeID));
    }

    // Get all saved recipes
    @GetMapping(path = "/listrecipes")
    @CrossOrigin(origins="http://localhost:5173")
    public List<RecipeDto> listRecipes() {
        List<RecipeEntity> entityList = recipeService.listRecipes();
        ArrayList<RecipeDto> dtoList = new ArrayList<RecipeDto>();
        entityList.forEach(entity -> {
            RecipeDto recipe = new RecipeDto(entity.getId(), entity.getImage(), entity.getTitle(),
                                            entity.getUsedIngredientCount(), entity.getMissedIngredientCount(), 
                                            entity.getInstructions());
            dtoList.add(recipe);
        });
        return dtoList;
    }

    // Add an ingredient to the pantry
    @PutMapping(path = "/addingredient")
    @CrossOrigin(origins="http://localhost:5173")
    public IngredientEntity addIngredient(@RequestBody IngredientDto ingredient) {
        IngredientEntity ingredientEntity = new IngredientEntity(ingredient.id(), ingredient.name(), ingredient.localizedName(), ingredient.image());
        ingredientService.addIngredient(ingredientEntity);
        return ingredientEntity;
    }

    // Remove an ingredient from the pantry
    @DeleteMapping(path = "/removeingredient")
    @CrossOrigin(origins="http://localhost:5173")
    public void removeingredient(@RequestBody String ingredientID) {
        ingredientService.removeingredient(Long.valueOf(ingredientID));
    }

    // List all ingredients
    @GetMapping(path = "/listingredients") 
    @CrossOrigin(origins="http://localhost:5173")
    public List<IngredientDto> listIngredients() {
        List<IngredientEntity> entityList = ingredientService.listIngredients();
        ArrayList<IngredientDto> dtoList = new ArrayList<IngredientDto>();
        entityList.forEach(entity -> {
            IngredientDto ingredient = new IngredientDto(entity.getId(), entity.getName(), entity.getLocalizedName(), entity.getImage());
            //IngredientDto ingredient = ingredientMapper.mapTo(entity);
            dtoList.add(ingredient);
        });
        return dtoList;
    }
}