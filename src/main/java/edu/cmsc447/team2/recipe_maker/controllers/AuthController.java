package edu.cmsc447.team2.recipe_maker.controllers;

import edu.cmsc447.team2.recipe_maker.domain.dto.AuthRequestDto;
import edu.cmsc447.team2.recipe_maker.domain.dto.AuthResponseDto;
import edu.cmsc447.team2.recipe_maker.domain.entities.UserEntity;
import edu.cmsc447.team2.recipe_maker.repositories.UserRepository;
import edu.cmsc447.team2.recipe_maker.security.JwtUtil;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth") // Prefixes all endpoints with /api/auth
@RequiredArgsConstructor
@Slf4j
public class AuthController {

    private final AuthenticationManager authenticationManager;
    private final JwtUtil jwtUtil;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @PostMapping("/login")
    public AuthResponseDto login(@RequestBody AuthRequestDto authRequestDto) {
        log.info("Incoming login: username = {}, password = {}", authRequestDto.getUsername(), authRequestDto.getPassword());

        //TODO remove for testing
        UserEntity user = userRepository.findByUsername(authRequestDto.getUsername()).orElseThrow(() -> new UsernameNotFoundException("User not found: " + authRequestDto.getUsername()));

        boolean matches = passwordEncoder.matches(authRequestDto.getPassword(), user.getPassword());
        log.info("Password match? {}", matches);

        // Authenticate credentials
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(authRequestDto.getUsername(), authRequestDto.getPassword()));

        // Grab the authenticated user
        UserDetails userDetails = (UserDetails) authentication.getPrincipal();

        // Generate the JWT token
        String token = jwtUtil.generateToken(userDetails.getUsername());
        return new AuthResponseDto(token);
    }
}
