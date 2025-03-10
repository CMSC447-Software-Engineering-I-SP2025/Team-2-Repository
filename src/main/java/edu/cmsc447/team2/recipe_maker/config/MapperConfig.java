package edu.cmsc447.team2.recipe_maker.config;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Configurable;
import org.springframework.context.annotation.Bean;

@Configurable
public class MapperConfig {

    //Used to map entity class to Dto
    @Bean
    public ModelMapper modelMapper() {
        return new ModelMapper();
    }
}

