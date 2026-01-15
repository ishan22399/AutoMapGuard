"""
AutoMapGuard Python Geospatial Microservice

This microservice handles:
- Geometry validation (all 6 rule layers)
- Change detection from satellite imagery
- PostGIS database integration
- Image processing

Port: 8081
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional

from geometry_engine import GeometryComplianceEngine
from change_detection import ChangeDetectionEngine


# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize engines
geometry_engine = GeometryComplianceEngine()
change_detection_engine = ChangeDetectionEngine()

# Pydantic models
class GeometryValidationRequest(BaseModel):
    """Request to validate a geometry"""
    geometry: Dict[str, Any]
    strict: bool = False

class ChangeDetectionRequest(BaseModel):
    """Request to detect changes"""
    simulate: bool = True
    num_changes: int = 5

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str

# Lifespan context manager (for startup/shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AutoMapGuard Geospatial Microservice")
    logger.info("Geometry Engine initialized with:")
    logger.info(f"  - MIN_AREA: {geometry_engine.MIN_AREA} m²")
    logger.info(f"  - MIN_EDGE_LENGTH: {geometry_engine.MIN_EDGE_LENGTH} m")
    logger.info(f"  - ANGLE_TOLERANCE: {geometry_engine.ANGLE_TOLERANCE}°")
    logger.info(f"  - SIMPLIFICATION_TOLERANCE: {geometry_engine.SIMPLIFICATION_TOLERANCE} m")
    yield
    # Shutdown
    logger.info("Shutting down AutoMapGuard Geospatial Microservice")

# Create FastAPI app
app = FastAPI(
    title="AutoMapGuard Geospatial Microservice",
    description="GIS geometry validation, change detection, and spatial processing",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ Health Check Routes ============

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy",
        service="AutoMapGuard Geospatial Microservice",
        version="1.0.0"
    )

# ============ Geometry Validation Routes ============

@app.post("/geometry/validate")
async def validate_geometry(request: GeometryValidationRequest):
    """
    Validate a geometry against all 6 rule layers.
    
    Returns:
    - is_valid: bool
    - violations: List[str]  
    - fixed_geometry: Optional[GeoJSON]
    - confidence: float (0-1)
    
    Rule Layers:
    0. Foundational Validity (closed, min vertices, non-zero area, valid coords)
    1. Topological Consistency (no self-intersections, ring orientation, no duplicate points)
    2. Cartographic Quality (min area, min edge length, angle regularization, simplification)
    3. Temporal Consistency (overlap checks, area stability)
    4. Neighbor Topology (building conflicts, minimum distances)
    5. Auto-fix Eligibility (determines if auto-fixable)
    6. System Safety (CRS consistency, precision, versioning)
    """
    try:
        is_valid, violations, fixed_geom = geometry_engine.validate_geometry(request.geometry)
        
        confidence = geometry_engine.calculate_confidence(
            geometry_engine.shape(request.geometry) if is_valid else None,
            is_valid,
            violations
        )
        
        response = {
            "is_valid": is_valid,
            "violations": violations,
            "fixed_geometry": fixed_geom,
            "confidence": round(confidence, 2),
            "auto_fixable": fixed_geom is not None and is_valid,
            "violation_count": len(violations)
        }
        
        logger.info(f"Geometry validation: valid={is_valid}, violations={len(violations)}")
        return response
        
    except Exception as e:
        logger.error(f"Geometry validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")

@app.post("/geometry/auto-fix")
async def auto_fix_geometry(request: GeometryValidationRequest):
    """
    Automatically fix geometry violations where possible.
    
    Applies fixes in order:
    1. Remove duplicate consecutive points
    2. Apply buffer(0) for self-intersections
    3. Regularize angles to orthogonal
    4. Simplify polygon
    """
    try:
        is_valid, violations, fixed_geom = geometry_engine.validate_geometry(request.geometry)
        
        if fixed_geom and is_valid:
            response = {
                "success": True,
                "original_violations": violations,
                "fixed_geometry": fixed_geom,
                "remaining_violations": []
            }
        else:
            response = {
                "success": False,
                "original_violations": violations,
                "fixed_geometry": None,
                "error": "Unable to auto-fix this geometry",
                "remaining_violations": violations
            }
        
        logger.info(f"Auto-fix result: success={response['success']}")
        return response
        
    except Exception as e:
        logger.error(f"Auto-fix error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Auto-fix error: {str(e)}")

# ============ Change Detection Routes ============

@app.post("/changes/detect")
async def detect_changes(request: ChangeDetectionRequest):
    """
    Detect changes in satellite imagery.
    
    For MVP, this simulates detected changes.
    In production, this would:
    1. Load satellite imagery
    2. Align images
    3. Compute difference maps
    4. Detect building footprints
    5. Classify as new/modified/removed
    6. Assign confidence scores
    
    Returns list of detected changes with:
    - change_type: "new" | "modified" | "removed"
    - geometry: GeoJSON Polygon
    - confidence: float (0-1)
    - area: float (m²)
    """
    try:
        if request.simulate:
            changes = change_detection_engine.detect_changes_simulated(
                num_changes=request.num_changes
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Real image-based detection not yet implemented. Use simulate=True"
            )
        
        logger.info(f"Detected {len(changes)} changes")
        return {
            "changes": changes,
            "count": len(changes),
            "detection_type": "simulated" if request.simulate else "real"
        }
        
    except Exception as e:
        logger.error(f"Change detection error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Detection error: {str(e)}")

# ============ Utility Routes ============

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "AutoMapGuard Geospatial Microservice",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "geometry_validate": "POST /geometry/validate",
            "geometry_auto_fix": "POST /geometry/auto-fix",
            "changes_detect": "POST /changes/detect",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# ============ Error Handlers ============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Catch-all exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500
        }
    )

# ============ Running the application ============

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PYTHON_SERVICE_PORT", 8081))
    host = os.getenv("PYTHON_SERVICE_HOST", "0.0.0.0")
    
    logger.info(f"Starting AutoMapGuard Geospatial Microservice on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        reload=os.getenv("ENVIRONMENT", "development") == "development"
    )
