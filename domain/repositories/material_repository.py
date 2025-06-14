# backend/domain/repositories/material_repository.py
from abc import ABC, abstractmethod
from typing import List
from domain.entities.material import Material

class IMaterialRepository(ABC):
    @abstractmethod
    def create(self, course_id: int, name: str, url: str, material_type: str) -> Material:
        """Cria e persiste um novo material."""
        pass

    @abstractmethod
    def get_by_course(self, course_id: int) -> List[Material]:
        """Retorna materiais de um curso."""
        pass

    @abstractmethod
    def delete(self, material: Material) -> None:
        """Remove um material."""
        pass
