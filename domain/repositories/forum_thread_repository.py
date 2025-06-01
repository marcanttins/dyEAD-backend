# backend/domain/repositories/forum_thread_repository.py
from abc import ABC, abstractmethod
from typing import List
from domain.entities.forum_thread import ForumThread

class IForumThreadRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[ForumThread]:
        """Retorna todas as threads."""
        pass

    @abstractmethod
    def get_by_id(self, thread_id: int) -> ForumThread:
        """Retorna a thread ou dispara exceção se não encontrada."""
        pass

    @abstractmethod
    def create(self, user_id: int, title: str) -> ForumThread:
        """Cria uma nova thread."""
        pass

    @abstractmethod
    def delete(self, thread_id: int) -> None:
        """Remove uma thread existente."""
        pass
