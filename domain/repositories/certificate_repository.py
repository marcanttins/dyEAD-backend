# backend/domain/repositories/certificate_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
from domain.entities.certificate import Certificate

class ICertificateRepository(ABC):
    @abstractmethod
    def get_by_user_and_course(self, user_id: int, course_id: int) -> Optional[Certificate]:
        """Retorna o certificado existente para um dado usuário e curso, ou None se não existir."""
        pass

    @abstractmethod
    def create(self, user_id: int, course_id: int, file_url: str, issue_date: datetime = None) -> Certificate:
        """Cria um novo certificado para o usuário no curso."""
        pass
