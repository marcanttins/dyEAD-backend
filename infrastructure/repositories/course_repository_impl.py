# backend/infrastructure/repositories/course_repository_impl.py
from typing import List, Dict, Any
from domain.repositories.course_repository import ICourseRepository
from domain.entities.course import Course as CourseEntity
from infrastructure.extensions import db
from infrastructure.orm.models.course import Course as CourseModel

class CourseRepositoryImpl(ICourseRepository):
    def get_or_404(self, course_id: int) -> CourseEntity:
        m = CourseModel.query.get_or_404(course_id)
        return CourseEntity(
            id=m.id, title=m.title, description=m.description,
            category=m.category, status=m.status,
            instructor_id=m.instructor_id,
            created_at=m.created_at, updated_at=m.updated_at
        )

    def create(self, data: Dict[str, Any], instructor_id: int) -> CourseEntity:
        model = CourseModel(**data, instructor_id=instructor_id)
        db.session.add(model)
        db.session.commit()
        return CourseEntity(
            id=model.id, title=model.title, description=model.description,
            category=model.category, status=model.status,
            instructor_id=model.instructor_id,
            created_at=model.created_at, updated_at=model.updated_at
        )

    def update(self, course: CourseEntity, data: Dict[str, Any]) -> CourseEntity:
        model = CourseModel.query.get_or_404(course.id)
        for attr, val in data.items():
            setattr(model, attr, val)
        db.session.commit()
        return CourseEntity(
            id=model.id, title=model.title, description=model.description,
            category=model.category, status=model.status,
            instructor_id=model.instructor_id,
            created_at=model.created_at, updated_at=model.updated_at
        )

    def delete(self, course: CourseEntity) -> None:
        model = CourseModel.query.get(course.id)
        if model:
            db.session.delete(model)
            db.session.commit()

    def list_all(self) -> List[CourseEntity]:
        return [
            CourseEntity(
                id=m.id, title=m.title, description=m.description,
                category=m.category, status=m.status,
                instructor_id=m.instructor_id,
                created_at=m.created_at, updated_at=m.updated_at
            ) for m in CourseModel.query.all()
        ]

    def list_featured(self, limit: int = 5) -> List[CourseEntity]:
        qs = CourseModel.query.filter_by(status=CourseModel.status.ATIVO)
        qs = qs.order_by(CourseModel.created_at.desc()).limit(limit)
        return [self.get_or_404(m.id) for m in qs.all()]

    def list_for_student(self, user_id: int) -> List[CourseEntity]:
        # Assumindo relação many-to-many model.students
        qs = CourseModel.query.join(CourseModel.students).filter_by(user_id=user_id)
        return [self.get_or_404(m.id) for m in qs.all()]

    def list_for_instructor(self, instructor_id: int) -> List[CourseEntity]:
        qs = CourseModel.query.filter_by(instructor_id=instructor_id)
        return [self.get_or_404(m.id) for m in qs.all()]

    def count_all(self) -> int:
        return CourseModel.query.count()
