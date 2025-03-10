package edu.cmsc447.team2.recipe_maker.services.impl;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import edu.cmsc447.team2.recipe_maker.services.interfaces.RecipeClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.Arrays;
import java.util.List;

@Service
public class RecipeClientImpl implements RecipeClient {

    private final RestTemplate restTemplate;

    @Value("${spoonacular.api.key}")
    private String apiKey;

    public RecipeClientImpl(final RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    } //Allows restTemplate to be injected

    @Override
    public List<RecipeDto> getRecipes(String ingredients) {
        String baseURL = "https://api.spoonacular.com/recipes/findByIngredients";

        //TODO Replace this with UriComponentsBuilder, does this automatically
        String queryURL = UriComponentsBuilder.fromUriString(baseURL)
                .queryParam("ingredients", ingredients)
                .queryParam("apiKey", apiKey)
                .build().toUriString();

        // Fetch data and map it into Recipe[]
        RecipeDto[] recipes = restTemplate.getForObject(queryURL, RecipeDto[].class); //Sends the actual query

        //If no recipes were found, return empty response
        if(recipes == null)
            return List.of();

        return Arrays.asList(recipes);
    }
}
