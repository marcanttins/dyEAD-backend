# backend/application/use_cases/user_use_cases.py
from typing import Dict, Any, Tuple, List

from werkzeug.security import generate_password_hash

from domain.entities.user import User
from domain.repositories.user_repository import IUserRepository


class CreateUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, data: Dict[str, Any]) -> User:
        hashed = generate_password_hash(data['password'], method='sha256')
        return self.user_repo.create(
            name=data['name'],
            email=data['email'],
            password_hash=hashed,
            role=data.get('role', 'aluno')
        )

class UpdateUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int, data: Dict[str, Any]) -> User:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise ValueError("Usuário não encontrado")
        attrs: Dict[str, Any] = {}
        if 'name' in data:
            attrs['name'] = data['name']
        if 'email' in data:
            attrs['email'] = data['email']
        if 'password' in data and data['password']:
            attrs['password_hash'] = generate_password_hash(data['password'], method='sha256')
        if 'role' in data:
            attrs['role'] = data['role']
        return self.user_repo.update(user, **attrs)

class DeleteUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int) -> None:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise ValueError("Usuário não encontrado")
        self.user_repo.delete(user)

class GetUserByIdUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise ValueError("Usuário não encontrado")
        return user

class PaginateUsersUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, page: int, per_page: int) -> Tuple[List[User], int, int, int]:
        return self.user_repo.paginate(page, per_page)
