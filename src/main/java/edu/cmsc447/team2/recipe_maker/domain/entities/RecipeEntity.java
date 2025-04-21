package edu.cmsc447.team2.recipe_maker.domain.entities;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;

// Recipe Entity for database writing
@Entity
@Table(name = "recipes") // Changed this from recipies
@JsonIgnoreProperties(ignoreUnknown = true)

// Class definition + JPA tagging.
public class RecipeEntity {
    @Id
    @Column(name = "recipe_id", nullable = false, updatable = false)
    private Long id;   

    @Column(name = "title", length = 100, nullable = false)
    private String title;

    @Column(name = "used_ingredients")
    private Integer usedIngredientCount;

    @Column(name = "missed_ingredients")
    private Integer missedIngredientCount;

    @Column(name = "instructions", columnDefinition = "TEXT")
    private String instructions;

    @Column(name = "image_url", length = 500)
    private String image;

    // Default constructor (required by JPA)
    public RecipeEntity() {}

    // Parameterized constructor
    public RecipeEntity(Long id, String title, Integer usedIngredientCount, Integer missedIngredientCount, String instructions, String image) {
        this.id = id;
        this.title = title;
        this.usedIngredientCount = usedIngredientCount;
        this.missedIngredientCount = missedIngredientCount;
        this.instructions = instructions;
        this.image = image;
    }

    // Getters and setters (required for JPA)
    public Long getId() {return id;}
    public void setId(Long id) {this.id = id;}
    
    public String getTitle() {return title;}
    public void setTitle(String title) {this.title = title;}
    
    public Integer getUsedIngredientCount() {return usedIngredientCount;}
    public void setUsedIngredientCount(Integer usedIngredientCount) { this.usedIngredientCount = usedIngredientCount;}
    
    public Integer getMissedIngredientCount() {return missedIngredientCount;}
    public void setMissedIngredientCount(Integer missedIngredientCount) { this.missedIngredientCount = missedIngredientCount;}
    
    public String getInstructions() {return instructions;}
    public void setInstructions(String instructions) {this.instructions = instructions;}
    
    public String getImage() { return image; }
    public void setImage(String image) { this.image = image; }
}
