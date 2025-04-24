package edu.cmsc447.team2.recipe_maker.domain.entities;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

// Recipe Entity for database writing
@Entity
@Table(name = "recipes")
@JsonIgnoreProperties(ignoreUnknown = true)
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder

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

    // TOdo implement later
//    @ManyToOne
//    @JoinColumn(name = "user_id", nullable = false)
//    private UserEntity user;
}
