package com.automapguard.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.type.SqlTypes;
import org.hibernate.annotations.JdbcTypeCode;

import jakarta.persistence.*;
import com.fasterxml.jackson.databind.JsonNode;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "audit_log", indexes = {
    @Index(name = "idx_audit_entity", columnList = "entity_type,entity_id"),
    @Index(name = "idx_audit_timestamp", columnList = "timestamp")
})
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AuditLog {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    private String entityType; // 'building', 'change', 'review'

    private UUID entityId;

    private String action; // 'created', 'updated', 'approved', 'rejected'

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "jsonb")
    private JsonNode changes; // What changed

    @CreationTimestamp
    private LocalDateTime timestamp;

}
