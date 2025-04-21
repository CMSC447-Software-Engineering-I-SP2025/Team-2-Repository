package edu.cmsc447.team2.recipe_maker.mappers;

// Generic mapping between classes `A` and `B`
public interface GenericMapper<A,B> {
    B mapTo(A a); // A -> B
    A mapFrom(B b); // B -> A
}
