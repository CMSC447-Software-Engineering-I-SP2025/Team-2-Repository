package edu.cmsc447.team2.recipe_maker.domain.dto;

import lombok.Data;

@Data
public class AuthRequestDto {
    private String username;
    private String password;
}
