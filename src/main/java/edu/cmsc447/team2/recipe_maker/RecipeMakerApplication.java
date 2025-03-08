package edu.cmsc447.team2.recipe_maker;

import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Profile;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class RecipeMakerApplication {

	private static final Logger log = LoggerFactory.getLogger(RecipeMakerApplication.class);

	public static void main(String[] args) {

		SpringApplication.run(RecipeMakerApplication.class, args);
	}

	//TODO Refactor everything below into a service class
	@Bean
	public RestTemplate restTemplate(RestTemplateBuilder builder) {
		return builder.build();
	}

	@Bean
	@Profile("dev") // Allows us to turn beans on or off per profile
	public CommandLineRunner run(RestTemplate restTemplate, ConfigurableApplicationContext context) throws Exception {
		return args -> {
			String baseURL = "https://api.spoonacular.com/recipes/findByIngredients";
			String ingredients = "apples,+flour,+sugar";
			String apiKey = "53dcc7d06e9444f78d2aa6718fa34292"; //Not the safest having this as plaintext

			//Replace this with UriComponentsBuilder, does this automatically
			String queryURL = String.format("%s?ingredients=%s&apiKey=%s", baseURL, ingredients, apiKey);

			// Fetch data and map it into Recipe[]
			RecipeEntity[] recipeEntities = restTemplate.getForObject(queryURL, RecipeEntity[].class); //Sends the actual query

			//Prints out recipes to console
			//In format (id=, title=, usedIngredientCount=, missedIngredientCount=)
			if (recipeEntities != null) {
				for (RecipeEntity recipeEntity : recipeEntities) {
					System.out.println(recipeEntity.toString());
				}
			} else {
				System.out.println("No recipes found.");
			}

			SpringApplication.exit(context, () -> 0); //Closes program afterwards
		};
	}

}
