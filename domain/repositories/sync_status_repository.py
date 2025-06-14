# backend/domain/repositories/sync_status_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
from domain.entities.sync_status import SyncStatus

class ISyncStatusRepository(ABC):
    @abstractmethod
    def get_by_user(self, user_id: int) -> Optional[SyncStatus]:
        """Retorna o SyncStatus de um usuário."""
        pass

    @abstractmethod
    def create(self, user_id: int, status: str, last_sync: datetime = None) -> SyncStatus:
        """Cria um novo SyncStatus."""
        pass

    @abstractmethod
    def update(self, sync_status: SyncStatus, status: str, last_sync: datetime = None) -> SyncStatus:
        """Atualiza o estado e timestamp de SyncStatus existente."""
        pass
