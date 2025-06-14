# backend/infrastructure/orm/models/associations.py
from infrastructure.extensions import db

# Tabela de associação entre usuários e cursos (matrículas)
user_course = db.Table(
    'user_course',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)