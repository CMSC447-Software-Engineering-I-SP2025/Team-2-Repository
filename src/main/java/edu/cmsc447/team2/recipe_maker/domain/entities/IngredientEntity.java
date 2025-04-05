package edu.cmsc447.team2.recipe_maker.domain.entities;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@Entity
@Table(name = "ingredients")
@JsonIgnoreProperties(ignoreUnknown = true)
public class IngredientEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ingredient_id", nullable = false, updatable = false)
    private Long id;

    @Column(name = "name", length = 100, nullable = false)
    private String name;

    @Column(name = "ingredient_name", length = 100)
    private String localizedName;

    @Column(name = "image_url", length = 500)
    private String image;

    // Default constructor (required by JPA)
    public IngredientEntity() {}

    // Parameterized constructor
    public IngredientEntity(Long id, String name, String localizedName, String image) {
        this.id = id;
        this.name = name;
        this.localizedName = localizedName;
        this.image = image;
    }

    // Getters and Setters
    // public Long getId() {return id;}
    // public void setId(Long id) {this.id = id;}
    
    // public String getName() {return name;}
    // public void setName(String name) {this.name = name;}
    
    // public String getLocalizedName() {return localizedName;}
    // public void setLocalizedName(String localizedName) {this.localizedName = localizedName;}
    
    // public String getImage() {return image;}
    // public void setImage(String image) {this.image = image;}
}
