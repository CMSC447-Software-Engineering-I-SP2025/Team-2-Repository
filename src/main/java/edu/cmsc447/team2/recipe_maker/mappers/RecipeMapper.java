package edu.cmsc447.team2.recipe_maker.mappers;

//Encapsulates all logic for mapping for the application
// Maps any class A to any class B
public interface RecipeMapper<A,B> {

    B mapTo(A a);

    A mapFrom(B b);
}
