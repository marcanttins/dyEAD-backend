# backend/domain/repositories/forum_post_repository.py
from abc import ABC, abstractmethod
from typing import List
from domain.entities.forum_post import ForumPost

class IForumPostRepository(ABC):
    @abstractmethod
    def get_by_thread(self, thread_id: int) -> List[ForumPost]:
        """Retorna todos os posts de uma thread."""
        pass

    @abstractmethod
    def create(self, thread_id: int, user_id: int, content: str) -> ForumPost:
        """Cria um novo post em uma thread."""
        pass
