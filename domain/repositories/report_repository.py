# backend/domain/repositories/report_repository.py
from abc import ABC, abstractmethod

class IReportRepository(ABC):
    @abstractmethod
    def count_users(self) -> int:
        """Retorna o total de usuários cadastrados."""
        pass
