package edu.cmsc447.team2.recipe_maker.security;

import edu.cmsc447.team2.recipe_maker.domain.entities.UserEntity;
import edu.cmsc447.team2.recipe_maker.repositories.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

/**
 * Provides an interface to Spring Security that fetches user from the database
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class CustomUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        log.info("Authenticating user: {}", username);

        UserEntity user = userRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found: " + username));
        log.info("Found user: {}, password hash: {}", user.getUsername(), user.getPassword());
        return new UserDetailsImpl(user);
    }
}
