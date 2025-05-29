# backend/application/use_cases/sync_status_use_cases.py
from typing import Optional

from domain.entities.sync_status import SyncStatus
from domain.repositories.sync_status_repository import ISyncStatusRepository


class GetSyncStatusUseCase:
    def __init__(self, repo: ISyncStatusRepository):
        self.repo = repo

    def execute(self, user_id: int) -> Optional[SyncStatus]:
        return self.repo.get_by_user(user_id)

class CreateSyncStatusUseCase:
    def __init__(self, repo: ISyncStatusRepository):
        self.repo = repo

    def execute(self, user_id: int, status: str) -> SyncStatus:
        return self.repo.create(user_id, status)

class UpdateSyncStatusUseCase:
    def __init__(self, repo: ISyncStatusRepository):
        self.repo = repo

    def execute(self, user_id: int, status: str) -> SyncStatus:
        sync = self.repo.get_by_user(user_id)
        return self.repo.update(sync, status)
