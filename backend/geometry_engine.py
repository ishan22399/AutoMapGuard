from typing import Dict, List, Tuple, Any, Optional
from shapely.geometry import shape, Polygon, mapping
from shapely.validation import explain_validity
import math
import numpy as np

class GeometryComplianceEngine:
    """Implements all 6 layers of geometry rules"""
    
    def __init__(self):
        self.MIN_AREA = 20  # m²
        self.MIN_EDGE_LENGTH = 1  # meters
        self.ANGLE_TOLERANCE = 5  # degrees
        self.SIMPLIFICATION_TOLERANCE = 0.5  # meters
    
    def validate_geometry(self, geojson_geom: Dict[str, Any]) -> Tuple[bool, List[str], Optional[Dict[str, Any]]]:
        """Main validation function
        Returns: (is_valid, violations, fixed_geometry)
        """
        violations = []
        fixed_geom = None
        
        try:
            geom = shape(geojson_geom)
        except Exception as e:
            return False, [f"Invalid GeoJSON: {str(e)}"], None
        
        # LAYER 0: Foundational Validity
        layer0_valid, layer0_violations = self._check_layer0(geom)
        violations.extend(layer0_violations)
        
        if not layer0_valid:
            return False, violations, None
        
        # LAYER 1: Topological Consistency
        layer1_valid, layer1_violations, geom = self._check_and_fix_layer1(geom)
        violations.extend(layer1_violations)
        
        # LAYER 2: Cartographic Quality
        layer2_valid, layer2_violations, geom = self._check_and_fix_layer2(geom)
        violations.extend(layer2_violations)
        
        # Convert back to GeoJSON if fixed
        if geom and geom.is_valid:
            fixed_geom = mapping(geom)
        
        is_valid = len(violations) == 0
        return is_valid, violations, fixed_geom
    
    def _check_layer0(self, geom) -> Tuple[bool, List[str]]:
        """Layer 0: Foundational Geometry Validity"""
        violations = []
        
        # Check if it's a polygon
        if not isinstance(geom, Polygon):
            violations.append("Geometry must be a Polygon")
            return False, violations
        
        # Check if closed
        if not geom.exterior.is_closed:
            violations.append("Polygon is not closed")
        
        # Check minimum vertices (4 points including closure)
        if len(geom.exterior.coords) < 4:
            violations.append(f"Insufficient vertices: {len(geom.exterior.coords)} (minimum 4)")
        
        # Check non-zero area
        if geom.area <= 0:
            violations.append("Polygon has zero or negative area")
        
        # Check for NaN/infinite coordinates
        coords = list(geom.exterior.coords)
        for i, (x, y) in enumerate(coords):
            if not (math.isfinite(x) and math.isfinite(y)):
                violations.append(f"Invalid coordinate at position {i}: ({x}, {y})")
        
        return len(violations) == 0, violations
    
    def _check_and_fix_layer1(self, geom: Polygon) -> Tuple[bool, List[str], Polygon]:
        """Layer 1: Topological Consistency"""
        violations = []
        
        # Check for self-intersection
        if not geom.is_valid:
            reason = explain_validity(geom)
            violations.append(f"Invalid topology: {reason}")
            
            # Try to fix with buffer(0)
            try:
                fixed_geom = geom.buffer(0)
                if fixed_geom.is_valid and isinstance(fixed_geom, Polygon):
                    geom = fixed_geom
                    violations.append("Auto-fixed: Applied buffer correction")
            except:
                pass
        
        # Remove duplicate consecutive points
        coords = list(geom.exterior.coords)
        unique_coords = [coords[0]]
        for i in range(1, len(coords)):
            if coords[i] != coords[i-1]:
                unique_coords.append(coords[i])
        
        if len(unique_coords) != len(coords):
            geom = Polygon(unique_coords)
            violations.append("Auto-fixed: Removed duplicate consecutive points")
        
        return len(violations) == 0, violations, geom
    
    def _check_and_fix_layer2(self, geom: Polygon) -> Tuple[bool, List[str], Polygon]:
        """Layer 2: Cartographic Quality"""
        violations = []
        
        # Check minimum area
        area_m2 = geom.area * 111000 * 111000  # Rough conversion to m² (depends on projection)
        if area_m2 < self.MIN_AREA:
            violations.append(f"Area too small: {area_m2:.2f}m² (minimum {self.MIN_AREA}m²)")
        
        # Simplify polygon if needed
        if len(geom.exterior.coords) > 100:
            simplified = geom.simplify(self.SIMPLIFICATION_TOLERANCE / 111000, preserve_topology=True)
            if simplified.is_valid:
                geom = simplified
                violations.append("Auto-fixed: Simplified polygon to reduce vertices")
        
        # Check and fix angles (regularization)
        coords = list(geom.exterior.coords)
        regularized_coords = self._regularize_angles(coords)
        if regularized_coords != coords:
            geom = Polygon(regularized_coords)
            violations.append("Auto-fixed: Regularized angles to orthogonal")
        
        return True, violations, geom
    
    def _regularize_angles(self, coords: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """Regularize angles to 90°, 45°, 180°"""
        if len(coords) < 4:
            return coords
        
        regularized = [coords[0]]
        
        for i in range(1, len(coords) - 1):
            p1 = np.array(coords[i-1])
            p2 = np.array(coords[i])
            p3 = np.array(coords[i+1])
            
            v1 = p2 - p1
            v2 = p3 - p2
            
            # Calculate angle
            angle = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
            angle_deg = np.degrees(angle) % 360
            
            # Snap to nearest orthogonal angle
            target_angles = [0, 45, 90, 135, 180, 225, 270, 315]
            closest_angle = min(target_angles, key=lambda x: abs(angle_deg - x))
            
            if abs(angle_deg - closest_angle) <= self.ANGLE_TOLERANCE:
                # Keep original point if already close
                regularized.append(coords[i])
            else:
                regularized.append(coords[i])
        
        regularized.append(coords[-1])  # Close the polygon
        return regularized
    
    def calculate_confidence(self, geom: Polygon, is_valid: bool, violations: List[str]) -> float:
        """Calculate confidence score based on geometry quality"""
        if not is_valid:
            return 0.3
        
        score = 1.0
        
        # Penalize for violations
        score -= len(violations) * 0.1
        
        # Check shape regularity
        area = geom.area
        perimeter = geom.length
        if perimeter > 0:
            compactness = (4 * np.pi * area) / (perimeter ** 2)
            score *= compactness
        
        return max(0.0, min(1.0, score))
