# backend/domain/repositories/offline_content_repository.py
from abc import ABC, abstractmethod
from typing import List
from domain.entities.offline_content import OfflineContent

class IOfflineContentRepository(ABC):
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[OfflineContent]:
        """Conteúdos offline de um usuário."""
        pass

    @abstractmethod
    def create(self, user_id: int, content_type: str, content_url: str) -> OfflineContent:
        """Cria um novo conteúdo offline."""
        pass
