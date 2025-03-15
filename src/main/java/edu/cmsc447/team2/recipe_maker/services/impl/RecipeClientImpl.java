package edu.cmsc447.team2.recipe_maker.services.impl;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeResponse;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import edu.cmsc447.team2.recipe_maker.services.interfaces.RecipeClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonParser;

import java.util.Arrays;
import java.util.List;
import java.io.IOException;

import java.nio.file.Files;
import java.nio.file.Path;

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


        String baseURL = "https://api.spoonacular.com/recipes/complexSearch";
        List<RecipeDto> recipes= null;
        //TODO Replace this with UriComponentsBuilder, does this automatically
        String queryURL = UriComponentsBuilder.fromUriString(baseURL)
                .queryParam("includeIngredients", ingredients)
                .queryParam("instructionsRequired", true)
                .queryParam("addRecipeInformation", true)
                .queryParam("addRecipeInstructions", true)
                .queryParam("apiKey", apiKey)
                .build().toUriString();

        // Fetch data and map it into Recipe[]
        try {

            // Read JSON data
            String content = Files.readString(Path.of("cached.json")); //System.out.println("Raw Response: " + rawResponse);
            ResponseEntity<String> responseEntity = ResponseEntity.ok(content);

            String rawResponse = responseEntity.getBody();

            ObjectMapper objectMapper = new ObjectMapper()
            .configure(JsonParser.Feature.ALLOW_UNQUOTED_CONTROL_CHARS, true);
            //recipes = objectMapper.readValue(rawResponse, RecipeDto[].class);
            RecipeResponse recipeResponse = objectMapper.readValue(rawResponse, RecipeResponse.class);
            recipes = recipeResponse.getResults();


            // ResponseEntity<String> responseEntity = restTemplate.exchange(queryURL, HttpMethod.GET, null, String.class);
            // Files.readString(Path.of("cached.json"));

        }
        catch (JsonProcessingException e) {
            System.out.println("JSON Processing exception" + e); 
        }

        catch (IOException e) {
            System.out.println("IO Exception" + e); 
        }

        if(recipes == null) {
            return List.of();
        }

        return recipes;
        // RecipeDto[] recipes = restTemplate.getForObject(queryURL, RecipeDto[].class); //Sends the actual query

        //If no recipes were found, return empty response

    }
}
