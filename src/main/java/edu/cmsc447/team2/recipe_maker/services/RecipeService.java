package edu.cmsc447.team2.recipe_maker.services;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import edu.cmsc447.team2.recipe_maker.repositories.RecipeRepository;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;

// Recipe service to call RecipeClient for queries or RecipeRepository for database CRUD.
@Service
public class RecipeService {

    @Autowired
    private RecipeClient recipeClient;    

    private final RecipeRepository recipeRepository;

    @Autowired
    public RecipeService(RecipeRepository recipeRepository) {this.recipeRepository = recipeRepository;}

    public RecipeEntity createRecipe(RecipeEntity recipeEntity) {
        return null;
    }

    public List<RecipeDto> getRecipes(String ingredients) {
        return recipeClient.getRecipes(ingredients);
    }

    public RecipeEntity saveRecipe(RecipeEntity recipeEntity) {
        return recipeRepository.save(recipeEntity);
    }

    public void deleteRecipe(long recipeID) {
        recipeRepository.deleteById(recipeID);
    }


    public List<RecipeEntity> listRecipes() {
        return recipeRepository.findAll();
    }
}
