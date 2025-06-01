# backend/infrastructure/orm/models/course.py
from datetime import datetime, timezone
from infrastructure.extensions import db
from sqlalchemy import Enum as SAEnum
from domain.entities.course import CourseStatus

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    status = db.Column(
        SAEnum(CourseStatus, name='course_status', native_enum=False),
        default=CourseStatus.DRAFT,
        server_default=CourseStatus.DRAFT.value,
        nullable=False
    )
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    instructor = db.relationship(
        'User', backref=db.backref('courses', lazy='dynamic')
    )

    def __repr__(self):
        return f"<Course id={self.id} title={self.title!r} status={self.status.name}>"
