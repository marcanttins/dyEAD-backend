# backend/domain/repositories/recommendation_repository.py
from abc import ABC, abstractmethod
from typing import List
from domain.entities.recommendation import Recommendation

class IRecommendationRepository(ABC):
    @abstractmethod
    def create(self, user_id: int, recommendation_text: str) -> Recommendation:
        """Cria e persiste uma nova Recommendation."""
        pass

    @abstractmethod
    def list_for_user(self, user_id: int) -> List[Recommendation]:
        """Retorna todas as Recommendation de um usuário."""
        pass
