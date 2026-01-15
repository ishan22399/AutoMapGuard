package com.automapguard.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "reviews", indexes = {
    @Index(name = "idx_reviews_status", columnList = "status"),
    @Index(name = "idx_reviews_confidence", columnList = "confidence_threshold")
})
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Review {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "change_id")
    private Change change;

    @Column(columnDefinition = "VARCHAR(50) DEFAULT 'pending'")
    private String status; // pending, approved, rejected

    @Column(name = "confidence_threshold")
    private Double confidenceThreshold;

    @ManyToOne
    @JoinColumn(name = "reviewed_by")
    private User reviewedBy;

    private LocalDateTime reviewedAt;

    @Column(length = 1000)
    private String notes;

    private String decision; // approve, reject

    @CreationTimestamp
    private LocalDateTime createdAt;

}
