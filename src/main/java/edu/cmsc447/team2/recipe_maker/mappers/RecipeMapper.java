package edu.cmsc447.team2.recipe_maker.mappers;

// Generic mapping between classes `A` and `B`
public interface RecipeMapper<A,B> {
    B mapTo(A a);
    A mapFrom(B b);
}
