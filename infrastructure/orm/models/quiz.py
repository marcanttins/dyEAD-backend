# backend/infrastructure/orm/models/quiz.py
from datetime import datetime, timezone
from infrastructure.extensions import db

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    course = db.relationship('Course', backref=db.backref('quizzes', lazy='dynamic'))

    def __repr__(self):
        return f"<Quiz id={self.id} title={self.title!r}>"