# backend/domain/repositories/quiz_repository.py
from abc import ABC, abstractmethod
from typing import List
from domain.entities.quiz import Quiz

class IQuizRepository(ABC):
    """
    Interface para gerenciamento de quizzes (questionários) na camada de domínio.
    Define o contrato que implementações concretas devem seguir.
    """

    @abstractmethod
    def create(self, course_id: int, title: str) -> Quiz:
        """
        Cria um novo quiz para o curso especificado.

        Args:
            course_id (int): ID do curso ao qual o quiz pertence.
            title (str): Título do quiz.

        Returns:
            Quiz: Entidade do quiz recém-criado.
        """
        pass

    @abstractmethod
    def get_by_id(self, quiz_id: int) -> Quiz:
        """
        Recupera um quiz pelo seu ID, ou dispara exceção se não existir.

        Args:
            quiz_id (int): ID do quiz.

        Returns:
            Quiz: Entidade do quiz.
        """
        pass

    @abstractmethod
    def list_by_course(self, course_id: int) -> List[Quiz]:
        """
        Lista todos os quizzes associados a um curso.

        Args:
            course_id (int): ID do curso.

        Returns:
            List[Quiz]: Lista de entidades Quiz.
        """
        pass

    @abstractmethod
    def delete(self, quiz: Quiz) -> None:
        """
        Remove um quiz existente.

        Args:
            quiz (Quiz): Entidade do quiz a ser removido.
        """
        pass
