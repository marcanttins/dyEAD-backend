# backend/infrastructure/repositories/certificate_repository_impl.py
from typing import Optional
from domain.repositories.certificate_repository import ICertificateRepository
from domain.entities.certificate import Certificate as CertificateEntity
from infrastructure.extensions import db
from infrastructure.orm.models.certificate import Certificate as CertificateModel

class CertificateRepositoryImpl(ICertificateRepository):
    def get_by_user_and_course(self, user_id: int, course_id: int) -> Optional[CertificateEntity]:
        model = CertificateModel.query.filter_by(user_id=user_id, course_id=course_id).first()
        if not model:
            return None
        return CertificateEntity(
            id=model.id,
            user_id=model.user_id,
            course_id=model.course_id,
            issue_date=model.issue_date,
            file_url=model.file_url
        )

    def create(self, user_id: int, course_id: int, file_url: str, issue_date=None) -> CertificateEntity:
        model = CertificateModel(
            user_id=user_id,
            course_id=course_id,
            file_url=file_url,
            issue_date=issue_date
        )
        db.session.add(model)
        db.session.commit()
        return CertificateEntity(
            id=model.id,
            user_id=model.user_id,
            course_id=model.course_id,
            issue_date=model.issue_date,
            file_url=model.file_url
        )
