package com.automapguard.repository;

import com.automapguard.entity.Validation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ValidationRepository extends JpaRepository<Validation, UUID> {

    Optional<Validation> findByChangeId(UUID changeId);

    List<Validation> findByIsValidFalse(); // Invalid geometries
}
