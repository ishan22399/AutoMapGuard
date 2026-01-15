package com.automapguard.repository;

import com.automapguard.entity.Building;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface BuildingRepository extends JpaRepository<Building, UUID> {

    Page<Building> findByStatus(String status, Pageable pageable);

    @Query("SELECT b FROM Building b WHERE b.version = :version")
    List<Building> findByVersion(Integer version);

    Page<Building> findAll(Pageable pageable);
}
