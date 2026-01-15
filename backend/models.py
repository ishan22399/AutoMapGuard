from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User

class BuildingFootprint(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    geometry: Dict[str, Any]  # GeoJSON geometry
    properties: Dict[str, Any] = Field(default_factory=dict)
    version: int = 1
    status: str = "active"  # active, removed, modified
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChangeDetection(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    building_id: Optional[str] = None
    change_type: str  # new, modified, removed
    geometry: Dict[str, Any]
    confidence: float
    area: float
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "pending"  # pending, approved, rejected
    user_id: Optional[str] = None

class GeometryValidation(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    building_id: str
    is_valid: bool
    violations: List[str] = Field(default_factory=list)
    auto_fixable: bool = False
    fixed_geometry: Optional[Dict[str, Any]] = None
    validated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ReviewItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    change_id: str
    change_type: str
    geometry: Dict[str, Any]
    confidence: float
    violations: List[str] = Field(default_factory=list)
    status: str = "pending"
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChangeDetectionRequest(BaseModel):
    historical_image_url: Optional[str] = None
    latest_image_url: Optional[str] = None
    simulate: bool = True  # For MVP, we'll simulate changes

class GeometryValidationRequest(BaseModel):
    geometry: Dict[str, Any]

class ReviewDecision(BaseModel):
    review_id: str
    decision: str  # approve, reject
    notes: Optional[str] = None

class DashboardStats(BaseModel):
    total_buildings: int
    pending_changes: int
    pending_reviews: int
    total_detections: int
    accuracy_rate: float
    recent_activity: List[Dict[str, Any]] = Field(default_factory=list)
