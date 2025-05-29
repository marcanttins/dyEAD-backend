# backend/infrastructure/repositories/material_repository_impl.py
from typing import List
from domain.repositories.material_repository import IMaterialRepository
from domain.entities.material import Material as MaterialEntity
from infrastructure.extensions import db
from infrastructure.orm.models.material import Material as MaterialModel

class MaterialRepositoryImpl(IMaterialRepository):
    def create(self, course_id: int, name: str, url: str, material_type: str) -> MaterialEntity:
        m = MaterialModel(course_id=course_id, name=name, url=url, material_type=material_type)
        db.session.add(m)
        db.session.commit()
        return MaterialEntity(
            id=m.id,
            course_id=m.course_id,
            name=m.name,
            url=m.url,
            material_type=m.material_type,
            uploaded_at=m.uploaded_at
        )

    def get_by_course(self, course_id: int) -> List[MaterialEntity]:
        ms = MaterialModel.query.filter_by(course_id=course_id).all()
        return [
            MaterialEntity(
                id=m.id,
                course_id=m.course_id,
                name=m.name,
                url=m.url,
                material_type=m.material_type,
                uploaded_at=m.uploaded_at
            ) for m in ms
        ]

    def delete(self, material: MaterialEntity) -> None:
        m = MaterialModel.query.get(material.id)
        if m:
            db.session.delete(m)
            db.session.commit()
