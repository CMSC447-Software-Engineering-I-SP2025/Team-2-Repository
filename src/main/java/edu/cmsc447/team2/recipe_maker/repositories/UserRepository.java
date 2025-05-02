package edu.cmsc447.team2.recipe_maker.repositories;

import edu.cmsc447.team2.recipe_maker.domain.entities.UserEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<UserEntity, Long> {
    Optional<UserEntity> findByUsername(String username);
}
