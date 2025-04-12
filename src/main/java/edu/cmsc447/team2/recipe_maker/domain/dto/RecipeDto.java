package edu.cmsc447.team2.recipe_maker.domain.dto;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public record RecipeDto(
    Long id,
    String image,
    String title,
    Integer usedIngredientCount,
    Integer missedIngredientCount,
    List<InstructionDto> analyzedInstructions
) {    
    public RecipeDto(Long id, String image, String title, Integer usedIngredientCount, 
                    Integer missedIngredientCount, List<InstructionDto> analyzedInstructions) {
        this.id = id;
        this.image = image;
        this.title = title;
        this.usedIngredientCount = usedIngredientCount;
        this.missedIngredientCount = missedIngredientCount;
        this.analyzedInstructions = analyzedInstructions;
    }

    public RecipeDto(Long id, String image, String title, Integer usedIngredientCount, 
                    Integer missedIngredientCount, String analyzedInstructions) {
        this(id, image, title, usedIngredientCount, missedIngredientCount, instructionStringToList(analyzedInstructions));  
    }

    static private List<InstructionDto> instructionStringToList(String instructionString) {
        List<InstructionDto> instructions = null;
        ObjectMapper jsonMapper = new ObjectMapper();
        try {
            instructions = Arrays.stream(jsonMapper.readValue(instructionString, InstructionDto[].class)).toList(); 
        } catch (JsonMappingException e) {
            e.printStackTrace();
        } catch (JsonGenerationException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return instructions;
    }   
}