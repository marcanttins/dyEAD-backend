# backend/domain/entities/material.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Material:
    id: Optional[int]
    course_id: int
    name: str
    url: str
    material_type: str
    uploaded_at: datetime
