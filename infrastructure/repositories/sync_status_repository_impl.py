# backend/infrastructure/repositories/sync_status_repository_impl.py
from typing import Optional
from datetime import datetime
from domain.repositories.sync_status_repository import ISyncStatusRepository
from domain.entities.sync_status import SyncStatus as SyncStatusEntity
from infrastructure.extensions import db
from infrastructure.orm.models.sync_status import SyncStatus as SyncStatusModel

class SyncStatusRepositoryImpl(ISyncStatusRepository):
    def get_by_user(self, user_id: int) -> Optional[SyncStatusEntity]:
        m = SyncStatusModel.query.filter_by(user_id=user_id).first()
        if not m:
            return None
        return SyncStatusEntity(
            id=m.id,
            user_id=m.user_id,
            status=m.status,
            last_sync=m.last_sync
        )

    def create(self, user_id: int, status: str, last_sync: datetime = None) -> SyncStatusEntity:
        m = SyncStatusModel(user_id=user_id, status=status, last_sync=last_sync)
        db.session.add(m)
        db.session.commit()
        return SyncStatusEntity(
            id=m.id,
            user_id=m.user_id,
            status=m.status,
            last_sync=m.last_sync
        )

    def update(self, sync_status: SyncStatusEntity, status: str, last_sync: datetime = None) -> SyncStatusEntity:
        m = SyncStatusModel.query.get(sync_status.id)
        if not m:
            raise ValueError("SyncStatus not found")
        m.status = status
        m.last_sync = last_sync
        db.session.commit()
        return SyncStatusEntity(
            id=m.id,
            user_id=m.user_id,
            status=m.status,
            last_sync=m.last_sync
        )
