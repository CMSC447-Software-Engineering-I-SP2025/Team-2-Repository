package edu.cmsc447.team2.recipe_maker;

// import com.fasterxml.jackson.core.JsonProcessingException;
// import com.fasterxml.jackson.databind.ObjectMapper;
// import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import org.junit.jupiter.api.Test;
// import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.web.util.UriComponentsBuilder;


import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

@SpringBootTest // Tests the whole appliucation
class RecipeEntityMakerApplicationTests {

// 	//Converts a Java object to a json object
// 	@Test
// 	public void testJavatoJSON() throws JsonProcessingException { //Exception necessary for writeValueAsString
// 		ObjectMapper mapper = new ObjectMapper();
// 		RecipeEntity recipeEntity = new RecipeEntity(123L, "Apple Pie", 3, 1);

// 		String result = mapper.writeValueAsString(recipeEntity);
// 		assertThat(result).isEqualTo("{\"id\":123,\"title\":\"Apple Pie\",\"usedIngredientCount\":3,\"missedIngredientCount\":1}"); //Pass
// 	}

// 	//Converts a JSON object to a Java Object
// 	@Test
// 	public void testJSONtoJava() throws JsonProcessingException { //Exception necessary for readValue
// 		String json = "{\"id\":123,\"title\":\"Apple Pie\",\"usedIngredientCount\":3,\"missedIngredientCount\":1}";

// 		final ObjectMapper mapper = new ObjectMapper();
// 		RecipeEntity result = mapper.readValue(json, RecipeEntity.class); //Reads the JSON string and tries to construct the class given
// 		assertThat(result).isEqualTo(new RecipeEntity(123L, "Apple Pie", 3, 1));
// 	}

// }

    // Test Spoonacular Query builder
    @Test
    public void testQueryBuilder() {
        String baseURL = "https://api.spoonacular.com/recipes/complexSearch";
        String queryURL = UriComponentsBuilder.fromUriString(baseURL)
                .queryParam("includeIngredients", "salt")
                .queryParam("instructionsRequired", true)
                .queryParam("addRecipeInformation", true)
                .queryParam("addRecipeInstructions", true)
                .queryParam("apiKey", "testkey")
                .build().toUriString();
        assertThat(queryURL).isEqualTo("https://api.spoonacular.com/recipes/complexSearch?includeIngredients=salt&instructionsRequired=true&addRecipeInformation=true&addRecipeInstructions=true&apiKey=testkey");
    }
}