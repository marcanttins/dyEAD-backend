# backend/application/use_cases/offline_content_use_cases.py
from typing import List
from domain.repositories.offline_content_repository import IOfflineContentRepository
from domain.entities.offline_content import OfflineContent

class CreateOfflineContentUseCase:
    def __init__(self, repo: IOfflineContentRepository):
        self.repo = repo

    def execute(self, user_id: int, content_type: str, content_url: str) -> OfflineContent:
        return self.repo.create(user_id, content_type, content_url)

class GetOfflineContentUseCase:
    def __init__(self, repo: IOfflineContentRepository):
        self.repo = repo

    def execute(self, user_id: int) -> List[OfflineContent]:
        return self.repo.get_by_user(user_id)
