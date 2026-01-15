package com.automapguard.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.locationtech.jts.geom.Geometry;
import org.hibernate.type.SqlTypes;
import org.hibernate.annotations.JdbcTypeCode;

import jakarta.persistence.*;
import com.fasterxml.jackson.databind.JsonNode;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "versions", indexes = {
    @Index(name = "idx_versions_building", columnList = "building_id,version_number")
})
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BuildingVersion {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "building_id")
    private Building building;

    @Column(name = "version_number")
    private Integer versionNumber;

    @Column(columnDefinition = "geometry(POLYGON, 4326)")
    private Geometry geometry;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private JsonNode metadata;

    private LocalDateTime createdAt;

    @ManyToOne
    @JoinColumn(name = "created_by")
    private User createdBy;

}
