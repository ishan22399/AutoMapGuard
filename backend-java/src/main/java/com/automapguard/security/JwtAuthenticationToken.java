package com.automapguard.security;

import org.springframework.security.authentication.AbstractAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;

import java.util.Collections;
import java.util.UUID;

public class JwtAuthenticationToken extends AbstractAuthenticationToken {

    private final UUID userId;
    private final String email;
    private final String role;

    public JwtAuthenticationToken(UUID userId, String email, String role) {
        super(Collections.singletonList(new SimpleGrantedAuthority("ROLE_" + (role != null ? role.toUpperCase() : "USER"))));
        this.userId = userId;
        this.email = email;
        this.role = role;
        setAuthenticated(true);
    }

    @Override
    public Object getCredentials() {
        return null;
    }

    @Override
    public Object getPrincipal() {
        return email;
    }

    public UUID getUserId() {
        return userId;
    }

    public String getEmail() {
        return email;
    }

    public String getRole() {
        return role;
    }
}
