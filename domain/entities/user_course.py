# backend/domain/entities/user_course.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserCourse:
    user_id: int
    course_id: int
    enrollment_date: datetime
