# backend/domain/repositories/quiz_question_repository.py
from abc import ABC, abstractmethod
from typing import List
from domain.entities.quiz import QuizQuestion

class IQuizQuestionRepository(ABC):
    @abstractmethod
    def get_by_quiz(self, quiz_id: int) -> List[QuizQuestion]:
        """Retorna todas as perguntas de um quiz."""
        pass

    @abstractmethod
    def save_questions(self, quiz_id: int, questions: List[dict]) -> None:
        """Persiste questões geradas para um quiz."""
        pass
