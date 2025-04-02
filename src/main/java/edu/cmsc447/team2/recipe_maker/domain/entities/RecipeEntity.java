package edu.cmsc447.team2.recipe_maker.domain.entities;

//import java.util.ArrayList;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;

// Change this Entity (and change what we request of the spoonacular API)
// to change what recipe data we get / support.
@Entity
@JsonIgnoreProperties(ignoreUnknown = true)
public record RecipeEntity(
        Long id,
        String title,
        Integer usedIngredientCount,
        Integer missedIngredientCount,
        String instructions,
        String image) { }
// Can use a wrapper class like List<RecipeDetails> instead of individually passing in parameters
// More easily scalable
