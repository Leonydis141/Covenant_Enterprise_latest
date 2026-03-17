"""
COVENANT.AI Enterprise - Data Transfer Objects (DTOs)
Validated via Pydantic v2.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: Any # UUID
    is_active: bool
    created_at: datetime

class ConstraintSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., pattern=r"^[a-zA-Z0-9_-]+$")
    name: str
    description: str
    is_hard_constraint: bool = True
    logic_config: Dict[str, Any] = Field(default_factory=dict)
    version: str = "1.0.0"

class EvaluationRequest(BaseModel):
    action_type: str
    actor_id: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    context_tags: List[str] = Field(default_factory=list)

class EvaluationResponse(BaseModel):
    is_allowed: bool
    score: float = Field(..., ge=0, le=1)
    action_id: str
    violations: List[Dict[str, Any]] = []
    performance_ms: float
