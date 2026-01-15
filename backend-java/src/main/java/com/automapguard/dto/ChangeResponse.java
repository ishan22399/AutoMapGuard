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
public class ChangeResponse {

    private UUID id;
    private UUID buildingId;
    private String changeType; // new, modified, removed
    private JsonNode geometry;
    private Double confidence;
    private Double areaMeter;
    private LocalDateTime detectedAt;
    private String status; // pending, approved, rejected
    private UUID createdBy;
}
