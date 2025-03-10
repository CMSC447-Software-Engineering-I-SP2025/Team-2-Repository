package edu.cmsc447.team2.recipe_maker.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class RestTemplateConfig {

    //Allows restTemplate to be injected
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
