# backend/infrastructure/repositories/forum_post_repository_impl.py
from typing import List
from domain.repositories.forum_post_repository import IForumPostRepository
from domain.entities.forum_post import ForumPost as ForumPostEntity
from infrastructure.extensions import db
from infrastructure.orm.models.forum_post import ForumPost as ForumPostModel

class ForumPostRepositoryImpl(IForumPostRepository):
    def get_by_thread(self, thread_id: int) -> List[ForumPostEntity]:
        ms = ForumPostModel.query.filter_by(thread_id=thread_id).all()
        return [
            ForumPostEntity(
                id=m.id,
                thread_id=m.thread_id,
                user_id=m.user_id,
                content=m.content,
                created_at=m.created_at
            ) for m in ms
        ]

    def create(self, thread_id: int, user_id: int, content: str) -> ForumPostEntity:
        m = ForumPostModel(thread_id=thread_id, user_id=user_id, content=content)
        db.session.add(m)
        db.session.commit()
        return ForumPostEntity(
            id=m.id,
            thread_id=m.thread_id,
            user_id=m.user_id,
            content=m.content,
            created_at=m.created_at
        )
