package edu.cmsc447.team2.recipe_maker.domain.dto;
import java.util.List;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class RecipeResponse {
    private List<RecipeDto> results;

    // Getters and setters
    public List<RecipeDto> getResults() {
        return results;
    }

    public void setResults(List<RecipeDto> results) {
        this.results = results;
    }
}
