# backend/infrastructure/repositories/forum_thread_repository_impl.py
from typing import List
from domain.repositories.forum_thread_repository import IForumThreadRepository
from domain.entities.forum_thread import ForumThread as ForumThreadEntity
from infrastructure.extensions import db
from infrastructure.orm.models.forum_thread import ForumThread as ForumThreadModel

class ForumThreadRepositoryImpl(IForumThreadRepository):
    def get_all(self) -> List[ForumThreadEntity]:
        ms = ForumThreadModel.query.all()
        return [
            ForumThreadEntity(
                id=m.id,
                title=m.title,
                user_id=m.user_id,
                created_at=m.created_at,
                updated_at=m.updated_at
            ) for m in ms
        ]

    def get_by_id(self, thread_id: int) -> ForumThreadEntity:
        m = ForumThreadModel.query.get_or_404(thread_id)
        return ForumThreadEntity(
            id=m.id,
            title=m.title,
            user_id=m.user_id,
            created_at=m.created_at,
            updated_at=m.updated_at
        )

    def create(self, user_id: int, title: str) -> ForumThreadEntity:
        m = ForumThreadModel(user_id=user_id, title=title)
        db.session.add(m)
        db.session.commit()
        return ForumThreadEntity(
            id=m.id,
            title=m.title,
            user_id=m.user_id,
            created_at=m.created_at,
            updated_at=m.updated_at
        )

    def delete(self, thread_id: int) -> None:
        m = ForumThreadModel.query.get(thread_id)
        if m:
            db.session.delete(m)
            db.session.commit()
