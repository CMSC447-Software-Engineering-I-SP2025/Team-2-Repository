package edu.cmsc447.team2.recipe_maker.services.impl;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import edu.cmsc447.team2.recipe_maker.services.interfaces.RecipeClient;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.List;

@Service
public class RecipeClientImpl implements RecipeClient {

    private final RestTemplate restTemplate;
    private final String apiKey = "53dcc7d06e9444f78d2aa6718fa34292"; //Change this to properties

    public RecipeClientImpl(final RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    } //Allows restTemplate to be injected

    @Override
    public List<RecipeDto> getRecipes() {
        String baseURL = "https://api.spoonacular.com/recipes/findByIngredients";
        String ingredients = "apples,+flour,+sugar"; // Would need to be fetched in

        //Replace this with UriComponentsBuilder, does this automatically
        String queryURL = String.format("%s?ingredients=%s&apiKey=%s", baseURL, ingredients, apiKey);

        // Fetch data and map it into Recipe[]
        RecipeDto[] recipes = restTemplate.getForObject(queryURL, RecipeDto[].class); //Sends the actual query

        System.out.println("Fetched Recipes: " + Arrays.toString(recipes));

        return Arrays.asList(recipes); // TODO Implement properly, right now just to test
    }
}
