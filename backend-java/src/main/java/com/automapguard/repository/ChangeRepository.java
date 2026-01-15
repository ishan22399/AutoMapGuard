package com.automapguard.repository;

import com.automapguard.entity.Change;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface ChangeRepository extends JpaRepository<Change, UUID> {

    Page<Change> findByStatus(String status, Pageable pageable);

    List<Change> findByBuildingId(UUID buildingId);

    Page<Change> findByChangeType(String changeType, Pageable pageable);

    List<Change> findByConfidenceLessThan(Double confidence);
}
