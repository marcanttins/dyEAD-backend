# backend/infrastructure/orm/models/progress.py
from datetime import datetime, timezone
from infrastructure.extensions import db

class Progress(db.Model):
    __tablename__ = 'progresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    percentage = db.Column(db.Float, default=0.0, nullable=False)
    last_updated = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship('User', backref=db.backref('progresses', lazy='dynamic'))
    course = db.relationship('Course', backref=db.backref('progresses', lazy='dynamic'))

    def __repr__(self):
        return f"<Progress id={self.id} percentage={self.percentage:.2f}>"