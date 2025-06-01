# backend/domain/repositories/user_repository.py

from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from domain.entities.user import User

class IUserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Retorna o usuário com o email informado."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retorna o usuário pelo ID."""
        pass

    @abstractmethod
    def create(
        self,
        name: str,
        email: str,
        password_hash: str,
        role: str
    ) -> User:
        """Cria e persiste um novo usuário."""
        pass

    @abstractmethod
    def update(self, user: User, **attrs) -> User:
        """Atualiza atributos de um usuário existente."""
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        """Remove um usuário do banco de dados."""
        pass

    @abstractmethod
    def paginate(
        self,
        page: int,
        per_page: int,
        error_out: bool = False
    ) -> Tuple[List[User], int, int, int]:
        """
        Retorna tupla (items, page, pages, total) paginada de usuários.
        """
        pass

    @abstractmethod
    def count_all(self) -> int:
        """Retorna o total de usuários cadastrados."""
        pass
