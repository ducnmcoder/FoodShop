package com.foodshop.controller;

import com.foodshop.dto.LoginRequest;
import com.foodshop.dto.RegisterRequest;
import com.foodshop.model.User;
import com.foodshop.repository.UserRepository;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private UserRepository userRepository;

    @PostMapping("/register")
    public ResponseEntity<?> registerUser(@Valid @RequestBody RegisterRequest registerRequest) {
        if (userRepository.findByUsername(registerRequest.getUsername()).isPresent()) {
            return ResponseEntity.badRequest().body(Map.of("message", "Error: Username is already taken!"));
        }

        if (userRepository.findByEmail(registerRequest.getEmail()).isPresent()) {
            return ResponseEntity.badRequest().body(Map.of("message", "Error: Email is already in use!"));
        }

        User user = new User();
        user.setUsername(registerRequest.getUsername());
        user.setEmail(registerRequest.getEmail());
        // For a real app, hash the password (e.g., using BCrypt). Keeping it simple for this task.
        user.setPassword(registerRequest.getPassword());

        userRepository.save(user);

        return ResponseEntity.ok(Map.of("message", "User registered successfully!"));
    }

    @PostMapping("/login")
    public ResponseEntity<?> loginUser(@Valid @RequestBody LoginRequest loginRequest) {
        Optional<User> userOptional = userRepository.findByEmail(loginRequest.getEmail());

        if (userOptional.isPresent()) {
            User user = userOptional.get();
            if (user.isLocked()) {
                return ResponseEntity.status(403).body(Map.of("message", "Error: Account is locked. Please contact admin."));
            }
            // In a real app, check hashed password.
            if (user.getPassword().equals(loginRequest.getPassword())) {
                Map<String, Object> response = new HashMap<>();
                response.put("id", user.getId());
                response.put("username", user.getUsername());
                response.put("email", user.getEmail());
                response.put("role", user.getRole());
                response.put("message", "Login successful!");
                return ResponseEntity.ok(response);
            }
        }
        return ResponseEntity.status(401).body(Map.of("message", "Error: Invalid credentials"));
    }
}
