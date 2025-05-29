# backend/infrastructure/orm/models/certificate.py
from datetime import datetime, timezone
from infrastructure.extensions import db

class Certificate(db.Model):
    __tablename__ = 'certificates'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)
    issue_date = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = db.relationship('User', backref=db.backref('certificates', lazy='dynamic'))
    course = db.relationship('Course', backref=db.backref('certificates', lazy='dynamic'))

    def __repr__(self):
        return f"<Certificate id={self.id} user_id={self.user_id} course_id={self.course_id}>"
