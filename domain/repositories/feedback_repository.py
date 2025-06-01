# backend/domain/repositories/feedback_repository.py
from abc import ABC, abstractmethod
from typing import List
from domain.entities.feedback import Feedback

class IFeedbackRepository(ABC):
    @abstractmethod
    def create(self, user_id: int, course_id: int, message: str, sentiment: str) -> Feedback:
        """Cria e persiste um novo feedback."""
        pass

    @abstractmethod
    def list_by_course(self, course_id: int) -> List[Feedback]:
        """Retorna todos os feedbacks de um curso."""
        pass

    @abstractmethod
    def list_by_user(self, user_id: int) -> List[Feedback]:
        """Retorna todos os feedbacks de um usuário."""
        pass
