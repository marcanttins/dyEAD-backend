# backend/infrastructure/repositories/offline_content_repository_impl.py
from typing import List
from domain.repositories.offline_content_repository import IOfflineContentRepository
from domain.entities.offline_content import OfflineContent as OfflineContentEntity
from infrastructure.extensions import db
from infrastructure.orm.models.offline_content import OfflineContent as OfflineContentModel

class OfflineContentRepositoryImpl(IOfflineContentRepository):
    def get_by_user(self, user_id: int) -> List[OfflineContentEntity]:
        ms = OfflineContentModel.query.filter_by(user_id=user_id).all()
        return [
            OfflineContentEntity(
                id=m.id,
                user_id=m.user_id,
                content_type=m.content_type,
                content_url=m.content_url,
                downloaded_at=m.downloaded_at
            ) for m in ms
        ]

    def create(self, user_id: int, content_type: str, content_url: str) -> OfflineContentEntity:
        m = OfflineContentModel(user_id=user_id, content_type=content_type, content_url=content_url)
        db.session.add(m)
        db.session.commit()
        return OfflineContentEntity(
            id=m.id,
            user_id=m.user_id,
            content_type=m.content_type,
            content_url=m.content_url,
            downloaded_at=m.downloaded_at
        )
