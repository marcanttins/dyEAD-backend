# backend/application/use_cases/forum_use_cases.py
from typing import List
from domain.repositories.forum_thread_repository import IForumThreadRepository
from domain.repositories.forum_post_repository   import IForumPostRepository
from domain.entities.forum_thread import ForumThread
from domain.entities.forum_post   import ForumPost

class CreateThreadUseCase:
    def __init__(self, thread_repo: IForumThreadRepository):
        self.thread_repo = thread_repo

    def execute(self, user_id: int, title: str) -> ForumThread:
        return self.thread_repo.create(user_id, title)

class ListThreadsUseCase:
    def __init__(self, thread_repo: IForumThreadRepository):
        self.thread_repo = thread_repo

    def execute(self) -> List[ForumThread]:
        return self.thread_repo.get_all()

class DeleteThreadUseCase:
    def __init__(self, thread_repo: IForumThreadRepository):
        self.thread_repo = thread_repo

    def execute(self, thread_id: int) -> None:
        self.thread_repo.delete(thread_id)

class CreatePostUseCase:
    def __init__(self, post_repo: IForumPostRepository):
        self.post_repo = post_repo

    def execute(self, thread_id: int, user_id: int, content: str) -> ForumPost:
        return self.post_repo.create(thread_id, user_id, content)

class ListPostsUseCase:
    def __init__(self, post_repo: IForumPostRepository):
        self.post_repo = post_repo

    def execute(self, thread_id: int) -> List[ForumPost]:
        return self.post_repo.get_by_thread(thread_id)
