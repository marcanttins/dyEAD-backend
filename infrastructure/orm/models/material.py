# backend/infrastructure/orm/models/material.py
from datetime import datetime, timezone
from infrastructure.extensions import db

class Material(db.Model):
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    material_type = db.Column(db.String(50), nullable=False)
    uploaded_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    course = db.relationship('Course', backref=db.backref('materials', lazy='dynamic'))

    def __repr__(self):
        return f"<Material id={self.id} name={self.name!r}>"