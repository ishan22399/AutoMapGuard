package com.automapguard.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.locationtech.jts.geom.Geometry;
import org.hibernate.annotations.CreationTimestamp;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "changes", indexes = {
    @Index(name = "idx_changes_status", columnList = "status"),
    @Index(name = "idx_changes_type", columnList = "change_type"),
    @Index(name = "idx_changes_confidence", columnList = "confidence")
})
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Change {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "building_id")
    private Building building;

    @Column(nullable = false)
    private String changeType; // new, modified, removed

    @Column(columnDefinition = "geometry(POLYGON, 4326)")
    private Geometry geometry;

    @Column(nullable = false)
    private Double confidence; // 0-1

    @Column(name = "area_m2")
    private Double areaMeter;

    @CreationTimestamp
    private LocalDateTime detectedAt;

    @Column(columnDefinition = "VARCHAR(50) DEFAULT 'pending'")
    private String status; // pending, approved, rejected

    @ManyToOne
    @JoinColumn(name = "created_by")
    private User createdBy;

}
