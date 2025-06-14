from typing import Dict, Any, List
from domain.repositories.lesson_repository import ILessonRepository
from domain.entities.lesson import Lesson
from infrastructure.database import db
from sqlalchemy.exc import SQLAlchemyError
from domain.exceptions import APIError

class LessonRepositoryImpl(ILessonRepository):
    def create(self, course_id: int, data: Dict[str, Any]) -> Lesson:
        try:
            lesson = Lesson(
                title=data['title'],
                description=data.get('description'),
                type=data['type'],
                status=data.get('status', 'draft'),
                duration=data['duration'],
                video_url=data.get('video_url'),
                material_url=data.get('material_url'),
                questions=data.get('questions', []),
                course_id=course_id
            )
            db.session.add(lesson)
            db.session.commit()
            return lesson
        except SQLAlchemyError as e:
            db.session.rollback()
            raise APIError('Erro ao criar aula', 500)

    def get_or_404(self, lesson_id: int) -> Lesson:
        lesson = Lesson.query.get(lesson_id)
        if not lesson:
            raise APIError('Aula não encontrada', 404)
        return lesson

    def update(self, lesson: Lesson, data: Dict[str, Any]) -> Lesson:
        try:
            for key, value in data.items():
                if hasattr(lesson, key):
                    setattr(lesson, key, value)
            db.session.commit()
            return lesson
        except SQLAlchemyError as e:
            db.session.rollback()
            raise APIError('Erro ao atualizar aula', 500)

    def delete(self, lesson: Lesson) -> None:
        try:
            db.session.delete(lesson)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise APIError('Erro ao deletar aula', 500)

    def list_by_course(self, course_id: int) -> List[Lesson]:
        return Lesson.query.filter_by(course_id=course_id).all()
