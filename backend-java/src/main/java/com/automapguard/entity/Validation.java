package com.automapguard.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.locationtech.jts.geom.Geometry;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.type.SqlTypes;
import org.hibernate.annotations.JdbcTypeCode;

import jakarta.persistence.*;
import com.fasterxml.jackson.databind.JsonNode;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "validations")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Validation {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "change_id")
    private Change change;

    @Column(nullable = false)
    private Boolean isValid;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private JsonNode violations; // Array of violation messages

    @Column(columnDefinition = "boolean default false")
    private Boolean autoFixable;

    @Column(columnDefinition = "geometry(POLYGON, 4326)")
    private Geometry fixedGeometry;

    @CreationTimestamp
    private LocalDateTime validatedAt;

}
