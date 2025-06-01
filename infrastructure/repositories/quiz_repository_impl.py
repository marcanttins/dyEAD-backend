# backend/infrastructure/repositories/quiz_repository_impl.py
from typing import List
from domain.repositories.quiz_repository import IQuizRepository
from domain.entities.quiz import Quiz as QuizEntity
from infrastructure.extensions import db
from infrastructure.orm.models.quiz import Quiz as QuizModel

class QuizRepositoryImpl(IQuizRepository):
    """
    Implementação concreta de IQuizRepository usando SQLAlchemy.
    """

    def create(self, course_id: int, title: str) -> QuizEntity:
        model = QuizModel(course_id=course_id, title=title)
        db.session.add(model)
        db.session.commit()
        return QuizEntity(
            id=model.id,
            course_id=model.course_id,
            title=model.title,
            created_at=model.created_at
        )

    def get_by_id(self, quiz_id: int) -> QuizEntity:
        model = QuizModel.query.get_or_404(quiz_id)
        return QuizEntity(
            id=model.id,
            course_id=model.course_id,
            title=model.title,
            created_at=model.created_at
        )

    def list_by_course(self, course_id: int) -> List[QuizEntity]:
        models = QuizModel.query.filter_by(course_id=course_id).all()
        return [
            QuizEntity(
                id=m.id,
                course_id=m.course_id,
                title=m.title,
                created_at=m.created_at
            ) for m in models
        ]

    def delete(self, quiz: QuizEntity) -> None:
        model = QuizModel.query.get(quiz.id)
        if model:
            db.session.delete(model)
            db.session.commit()