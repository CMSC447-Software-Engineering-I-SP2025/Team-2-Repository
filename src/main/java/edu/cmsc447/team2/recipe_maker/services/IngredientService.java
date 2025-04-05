package edu.cmsc447.team2.recipe_maker.services;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;

import edu.cmsc447.team2.recipe_maker.domain.entities.IngredientEntity;
import edu.cmsc447.team2.recipe_maker.repositories.IngredientRepository;

public class IngredientService {
    
    private final IngredientRepository IngredientRepository;

    @Autowired
    public IngredientService(IngredientRepository IngredientRepository) {this.IngredientRepository = IngredientRepository;}

    public IngredientEntity addIngredient(IngredientEntity IngredientEntity) {return IngredientRepository.save(IngredientEntity);}

    public void removeIngredient(long ingredientID) {IngredientRepository.deleteById(ingredientID);}

    public List<IngredientEntity> listIngredients() {return IngredientRepository.findAll();}
}