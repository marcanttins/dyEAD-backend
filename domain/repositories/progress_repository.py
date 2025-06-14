# backend/domain/repositories/progress_repository.py
from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.progress import Progress


class IProgressRepository(ABC):
    """
    Interface para persistência de progresso de curso.
    """

    @abstractmethod
    def create(self, user_id: int, course_id: int) -> Progress:
        """
        Cria um novo registro de progresso iniciando em 0% para o usuário e curso.
        Retorna a entidade Progress criada.
        """
        pass

    @abstractmethod
    def update(self, progress: Progress) -> Progress:
        """
        Atualiza o registro de progresso existente.
        Retorna a entidade Progress atualizada.
        """
        pass

    @abstractmethod
    def get_by_user_and_course(self, user_id: int, course_id: int) -> Optional[Progress]:
        """
        Retorna o registro de progresso de um usuário em um curso,
        ou None se não existir.
        """
        pass

    @abstractmethod
    def avg_progress_for_user(self, user_id: int) -> float:
        """
        Retorna o progresso médio (0-100) de um usuário em todos os seus cursos.
        """
        pass

    @abstractmethod
    def average_progress_all(self) -> float:
        """
        Retorna o progresso médio global (0-100) de todos os usuários em todos os cursos.
        """
        pass
