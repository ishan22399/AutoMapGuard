package com.automapguard.repository;

import com.automapguard.entity.Review;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface ReviewRepository extends JpaRepository<Review, UUID> {

    Page<Review> findByStatus(String status, Pageable pageable);

    List<Review> findByChangeId(UUID changeId);

    Page<Review> findByReviewedByIsNull(Pageable pageable); // Pending reviews
}
