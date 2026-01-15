package com.automapguard.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Map;

@Service
public class GeometryServiceClient {

    private final WebClient webClient;
    private final ObjectMapper objectMapper;

    @Value("${python.microservice.url:http://localhost:8081}")
    private String pythonServiceUrl;

    public GeometryServiceClient(WebClient.Builder webClientBuilder, ObjectMapper objectMapper) {
        this.webClient = webClientBuilder.build();
        this.objectMapper = objectMapper;
    }

    /**
     * Call Python microservice to validate geometry
     */
    public Map<String, Object> validateGeometry(JsonNode geometry) {
        Map<String, Object> payload = objectMapper.convertValue(geometry, new TypeReference<Map<String, Object>>() {});

        try {
            String response = webClient.post()
                    .uri(pythonServiceUrl + "/geometry/validate")
                    .bodyValue(payload)
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();

            return objectMapper.readValue(response, new TypeReference<Map<String, Object>>() {});
        } catch (Exception e) {
            throw new RuntimeException("Failed to validate geometry: " + e.getMessage(), e);
        }
    }

    /**
     * Call Python microservice to auto-fix geometry
     */
    public Map<String, Object> autoFixGeometry(JsonNode geometry) {
        Map<String, Object> payload = objectMapper.convertValue(geometry, new TypeReference<Map<String, Object>>() {});

        try {
            String response = webClient.post()
                    .uri(pythonServiceUrl + "/geometry/auto-fix")
                    .bodyValue(payload)
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();

            return objectMapper.readValue(response, new TypeReference<Map<String, Object>>() {});
        } catch (Exception e) {
            throw new RuntimeException("Failed to auto-fix geometry: " + e.getMessage(), e);
        }
    }

    /**
     * Call Python microservice to detect changes
     */
    public Map<String, Object> detectChanges(boolean simulate) {
        try {
            String response = webClient.post()
                    .uri(pythonServiceUrl + "/changes/detect?simulate=" + simulate)
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();

            return objectMapper.readValue(response, new TypeReference<Map<String, Object>>() {});
        } catch (Exception e) {
            throw new RuntimeException("Failed to detect changes: " + e.getMessage(), e);
        }
    }

    /**
     * Health check for Python microservice
     */
    public boolean isHealthy() {
        try {
            String response = webClient.get()
                    .uri(pythonServiceUrl + "/health")
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();

            return response != null && response.contains("\"status\":\"healthy\"");
        } catch (Exception e) {
            return false;
        }
    }
}
