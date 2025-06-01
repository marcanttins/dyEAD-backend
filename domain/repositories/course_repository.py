# backend/domain/repositories/course_repository.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from domain.entities.course import Course


class ICourseRepository(ABC):
    @abstractmethod
    def get_or_404(self, course_id: int) -> Course:
        """Retorna o curso ou dispara exceção se não existir."""
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any], instructor_id: int) -> Course:
        """Cria e persiste um novo curso."""
        pass

    @abstractmethod
    def update(self, course: Course, data: Dict[str, Any]) -> Course:
        """Atualiza campos de um curso existente."""
        pass

    @abstractmethod
    def delete(self, course: Course) -> None:
        """Remove um curso do banco."""
        pass

    @abstractmethod
    def list_all(self) -> List[Course]:
        """Retorna todos os cursos."""
        pass

    @abstractmethod
    def list_featured(self, limit: int = 5) -> List[Course]:
        """Retorna cursos ativos ordenados por data, até o limite."""
        pass

    @abstractmethod
    def list_for_student(self, user_id: int) -> List[Course]:
        """Cursos em que o estudante está matriculado."""
        pass

    @abstractmethod
    def list_for_instructor(self, instructor_id: int) -> List[Course]:
        """Cursos criados pelo instrutor."""
        pass

    @abstractmethod
    def count_all(self) -> int:
        """Total de cursos existentes."""
        pass
