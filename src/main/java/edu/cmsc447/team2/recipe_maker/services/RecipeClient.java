package edu.cmsc447.team2.recipe_maker.services;

import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeDto;
import edu.cmsc447.team2.recipe_maker.domain.dto.RecipeResponse;
// import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
// import edu.cmsc447.team2.recipe_maker.mappers.impl.RecipeMapperImpl;
// import edu.cmsc447.team2.recipe_maker.mappers.interfaces.Mapper;
// import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
// import edu.cmsc447.team2.recipe_maker.services.interfaces.RecipeClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonParser;

// import java.io.IOException;
// import java.nio.file.Files;
// import java.nio.file.Path;
import java.util.List;

@Service
public class RecipeClient {
    /* This function queries the spoonacular API, maps the returned data to Recipe DTO objects,
    and returns a list of those objects.*/  


    // Private vars
    private final RestTemplate restTemplate;
    @Value("${spoonacular.api.key}")
    private String apiKey;
    public RecipeClient(final RestTemplate restTemplate) {this.restTemplate = restTemplate;}

    
    public List<RecipeDto> getRecipes(String ingredients) {

        String baseURL = "https://api.spoonacular.com/recipes/complexSearch";
        String queryURL = UriComponentsBuilder.fromUriString(baseURL)
                .queryParam("includeIngredients", ingredients)
                .queryParam("instructionsRequired", true)
                .queryParam("addRecipeInformation", true)
                .queryParam("addRecipeInstructions", true)
                .queryParam("apiKey", apiKey)
                .build().toUriString();

        System.out.println(queryURL);


        // Fetch data and map it into Recipe[]
        try {

            // Option 1: Get data from cached JSON
            //ResponseEntity<String> responseEntity = ResponseEntity.ok(Files.readString(Path.of("cached.json")));

            // Option 2: Get data from API
            ResponseEntity<String> responseEntity = restTemplate.exchange(queryURL, HttpMethod.GET, null, String.class);

            // Map data to recipeResponse object
            String rawResponse = responseEntity.getBody();
            ObjectMapper objectMapper = new ObjectMapper().configure(JsonParser.Feature.ALLOW_UNQUOTED_CONTROL_CHARS, true);
            RecipeResponse recipeResponse = objectMapper.readValue(rawResponse, RecipeResponse.class);
            return recipeResponse.getResults();
        }

        // Exception / no data handling
        catch (JsonProcessingException e) {
            System.out.println("JSON Processing exception" + e);
            return List.of();
        }
    }
}
