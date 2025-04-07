package edu.cmsc447.team2.recipe_maker.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import edu.cmsc447.team2.recipe_maker.domain.entities.RecipeEntity;

// Allow for abstracted database funtions to be used.
@Repository
public interface RecipeRepository extends JpaRepository<RecipeEntity, Long> {}
