import numpy as np
import cv2
from typing import List, Dict, Any, Tuple
import random
from shapely.geometry import box, Polygon, mapping
from datetime import datetime, timezone

class ChangeDetectionEngine:
    """Simple & Explainable Change Detection using image differencing"""
    
    def __init__(self):
        self.threshold = 0.3
        self.min_area = 100  # pixels
    
    def detect_changes_simulated(self, num_changes: int = 5) -> List[Dict[str, Any]]:
        """Simulate change detection for MVP demo
        In production, this would process real satellite imagery
        """
        changes = []
        change_types = ["new", "modified", "removed"]
        
        # Simulate detected changes in a realistic coordinate space
        # Using bounds roughly around a city area
        base_lat, base_lon = 40.7128, -74.0060  # Example: NYC area
        
        for i in range(num_changes):
            change_type = random.choice(change_types)
            
            # Generate random building footprint
            center_lat = base_lat + random.uniform(-0.05, 0.05)
            center_lon = base_lon + random.uniform(-0.05, 0.05)
            
            width = random.uniform(0.0001, 0.0005)
            height = random.uniform(0.0001, 0.0005)
            
            # Create rectangular building footprint
            coords = [
                [center_lon - width/2, center_lat - height/2],
                [center_lon + width/2, center_lat - height/2],
                [center_lon + width/2, center_lat + height/2],
                [center_lon - width/2, center_lat + height/2],
                [center_lon - width/2, center_lat - height/2]
            ]
            
            geometry = {
                "type": "Polygon",
                "coordinates": [coords]
            }
            
            # Calculate confidence based on change type
            if change_type == "new":
                confidence = random.uniform(0.75, 0.95)
            elif change_type == "modified":
                confidence = random.uniform(0.60, 0.85)
            else:  # removed
                confidence = random.uniform(0.70, 0.90)
            
            # Calculate area (rough approximation)
            area = width * height * 111000 * 111000  # Convert to m²
            
            changes.append({
                "change_type": change_type,
                "geometry": geometry,
                "confidence": round(confidence, 2),
                "area": round(area, 2),
                "detected_at": datetime.now(timezone.utc).isoformat()
            })
        
        return changes
    
    def detect_changes_from_images(self, historical_img: np.ndarray, latest_img: np.ndarray) -> List[Dict[str, Any]]:
        """Real image-based change detection (for future enhancement)
        
        Uses:
        1. Image differencing
        2. Thresholding
        3. Contour detection
        """
        # Convert to grayscale
        hist_gray = cv2.cvtColor(historical_img, cv2.COLOR_BGR2GRAY)
        latest_gray = cv2.cvtColor(latest_img, cv2.COLOR_BGR2GRAY)
        
        # Compute absolute difference
        diff = cv2.absdiff(hist_gray, latest_gray)
        
        # Apply threshold
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        
        # Morphological operations to clean noise
        kernel = np.ones((5,5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        changes = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_area:
                # Convert contour to polygon
                epsilon = 0.01 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Convert to coordinates
                coords = [(float(point[0][0]), float(point[0][1])) for point in approx]
                
                if len(coords) >= 3:
                    coords.append(coords[0])  # Close polygon
                    
                    geometry = {
                        "type": "Polygon",
                        "coordinates": [coords]
                    }
                    
                    changes.append({
                        "change_type": "new",  # Would need ML classifier to determine type
                        "geometry": geometry,
                        "confidence": 0.75,  # Placeholder
                        "area": area,
                        "detected_at": datetime.now(timezone.utc).isoformat()
                    })
        
        return changes
