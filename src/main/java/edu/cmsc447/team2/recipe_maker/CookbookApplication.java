package edu.cmsc447.team2.recipe_maker;

import edu.cmsc447.team2.recipe_maker.domain.entities.UserEntity;
import edu.cmsc447.team2.recipe_maker.repositories.UserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.security.crypto.password.PasswordEncoder;


@SpringBootApplication
public class CookbookApplication {
	// private static final Logger log = LoggerFactory.getLogger(RecipeMakerApplication.class);


	public static void main(String[] args) {SpringApplication.run(CookbookApplication.class, args);}

	// Testing inserting
	/*
	@Bean
	CommandLineRunner seedUser(UserRepository repo, PasswordEncoder encoder) {
		return args -> {
			if (repo.findByUsername("testuser").isEmpty()) {
				UserEntity user = UserEntity.builder()
						.username("testuser")
						.password(encoder.encode("testpass")) // ✅ hashed using current encoder
						.build();
				repo.save(user);
				System.out.println("✅ Test user created: testuser / testpass");
			}
		};
	}
	 */
}
