# backend/infrastructure/orm/models/quiz_question.py
from infrastructure.extensions import db
from sqlalchemy.dialects.postgresql import JSON

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    options = db.Column(JSON, nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

    quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))
