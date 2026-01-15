package com.automapguard.repository;

import com.automapguard.entity.BuildingVersion;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface BuildingVersionRepository extends JpaRepository<BuildingVersion, UUID> {

    List<BuildingVersion> findByBuildingIdOrderByVersionNumberDesc(UUID buildingId);

    Optional<BuildingVersion> findByBuildingIdAndVersionNumber(UUID buildingId, Integer versionNumber);
}
