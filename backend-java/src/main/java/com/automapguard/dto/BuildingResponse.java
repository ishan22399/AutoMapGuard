package com.automapguard.dto;

import com.fasterxml.jackson.databind.JsonNode;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BuildingResponse {

    private UUID id;
    private Integer version;
    private JsonNode geometry;
    private String status;
    private JsonNode metadata;
    private Double areaMeter;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
