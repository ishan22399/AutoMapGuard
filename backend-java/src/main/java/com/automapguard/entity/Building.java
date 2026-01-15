package com.automapguard.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.locationtech.jts.geom.Geometry;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import jakarta.persistence.*;
import com.fasterxml.jackson.databind.JsonNode;
import org.hibernate.type.SqlTypes;
import org.hibernate.annotations.JdbcTypeCode;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "buildings")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Building {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(columnDefinition = "integer default 1")
    private Integer version;

    @Column(columnDefinition = "geometry(POLYGON, 4326)")
    private Geometry geometry;

    @Column(columnDefinition = "VARCHAR(50) DEFAULT 'active'")
    private String status; // active, removed, modified

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private JsonNode metadata; // Additional properties

    @Column(name = "area_m2")
    private Double areaMeter; // in square meters

    @CreationTimestamp
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;

    @ManyToOne
    @JoinColumn(name = "created_by")
    private User createdBy;

}
