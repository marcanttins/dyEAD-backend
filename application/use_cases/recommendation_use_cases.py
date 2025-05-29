# backend/application/use_cases/recommendation_use_cases.py
from typing import List
from domain.repositories.recommendation_repository import IRecommendationRepository
from domain.entities.recommendation import Recommendation

class CreateRecommendationUseCase:
    def __init__(self, repo: IRecommendationRepository):
        self.repo = repo

    def execute(self, user_id: int, text: str) -> Recommendation:
        return self.repo.create(user_id, text)

class ListRecommendationsUseCase:
    def __init__(self, repo: IRecommendationRepository):
        self.repo = repo

    def execute(self, user_id: int) -> List[Recommendation]:
        return self.repo.list_for_user(user_id)
