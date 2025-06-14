# backend/infrastructure/repositories/user_repository_impl.py

from typing import Optional, Tuple, List
from domain.repositories.user_repository import IUserRepository
from domain.entities.user import User as UserEntity
from infrastructure.extensions import db
from infrastructure.orm.models.user import User as UserModel

class UserRepositoryImpl(IUserRepository):
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        m = UserModel.query.filter_by(email=email).first()
        if not m:
            return None
        return UserEntity(
            id=m.id,
            name=m.name,
            email=m.email,
            password_hash=m.password_hash,
            role=m.role,
            created_at=m.created_at,
            updated_at=m.updated_at
        )

    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        m = UserModel.query.get(user_id)
        if not m:
            return None
        return UserEntity(
            id=m.id,
            name=m.name,
            email=m.email,
            password_hash=m.password_hash,
            role=m.role,
            created_at=m.created_at,
            updated_at=m.updated_at
        )

    def create(self, name: str, email: str, password_hash: str, role: str) -> UserEntity:
        m = UserModel(name=name, email=email, password_hash=password_hash, role=role)
        db.session.add(m)
        db.session.commit()
        return UserEntity(
            id=m.id,
            name=m.name,
            email=m.email,
            password_hash=m.password_hash,
            role=m.role,
            created_at=m.created_at,
            updated_at=m.updated_at
        )

    def update(self, user: UserEntity, **attrs) -> UserEntity:
        m = UserModel.query.get(user.id)
        if not m:
            raise ValueError("User not found")
        for key, val in attrs.items():
            setattr(m, key, val)
        db.session.commit()
        return UserEntity(
            id=m.id,
            name=m.name,
            email=m.email,
            password_hash=m.password_hash,
            role=m.role,
            created_at=m.created_at,
            updated_at=m.updated_at
        )

    def delete(self, user: UserEntity) -> None:
        m = UserModel.query.get(user.id)
        if m:
            db.session.delete(m)
            db.session.commit()

    def paginate(
        self,
        page: int,
        per_page: int,
        error_out: bool = False
    ) -> Tuple[List[UserEntity], int, int, int]:
        pagination = UserModel.query.paginate(page=page, per_page=per_page, error_out=error_out)
        items = [
            UserEntity(
                id=u.id,
                name=u.name,
                email=u.email,
                password_hash=u.password_hash,
                role=u.role,
                created_at=u.created_at,
                updated_at=u.updated_at
            )
            for u in pagination.items
        ]
        return items, pagination.page, pagination.pages, pagination.total

    def count_all(self) -> int:
        return UserModel.query.count()
