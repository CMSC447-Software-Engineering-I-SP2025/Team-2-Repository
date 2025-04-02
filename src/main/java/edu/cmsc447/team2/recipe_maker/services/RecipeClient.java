package edu.cmsc447.team2.recipe_maker.services;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
// import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.json.JsonReadFeature;


import java.util.List;

@Service
public class RecipeClient {
    // Query Spoonacular API, map returned data to a RecipeDto objects, and return those object in a list.
    
    private final RestTemplate restTemplate;
    @Value("${spoonacular.api.key}")
    private String apiKey;
    public RecipeClient(final RestTemplate restTemplate) {this.restTemplate = restTemplate;}
    
    public List<RecipeDto> getRecipes(String ingredients) {

        // Build Query
        String queryURL = UriComponentsBuilder.fromUriString("https://api.spoonacular.com/recipes/complexSearch")
                .queryParam("includeIngredients", ingredients)
                .queryParam("instructionsRequired", true)
                .queryParam("addRecipeInformation", true)
                .queryParam("addRecipeInstructions", true)
                .queryParam("apiKey", apiKey)
                .build().toUriString();
        // System.out.println(queryURL);

        try {

            // Option 1: Get data from cached JSON
            //ResponseEntity<String> responseEntity = ResponseEntity.ok(Files.readString(Path.of("cached.json")));

            // Make query to API 
            ResponseEntity<String> responseEntity = restTemplate.exchange(queryURL, HttpMethod.GET, null, String.class);

            // Map returned data to recipeResponse object
            String rawResponse = responseEntity.getBody();
            ObjectMapper objectMapper = new ObjectMapper().configure(JsonReadFeature.ALLOW_UNESCAPED_CONTROL_CHARS.mappedFeature(), true);
            RecipeResponse recipeResponse = objectMapper.readValue(rawResponse, RecipeResponse.class);
            return recipeResponse.getResults();
        }

        // Handle exceptions
        catch (JsonProcessingException e) {
            System.out.println("JSON Processing exception" + e);
            return List.of();
        }
    }
}
