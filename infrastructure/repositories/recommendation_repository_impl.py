# backend/infrastructure/repositories/recommendation_repository_impl.py
from typing import List
from domain.repositories.recommendation_repository import IRecommendationRepository
from domain.entities.recommendation import Recommendation as RecommendationEntity
from infrastructure.extensions import db
from infrastructure.orm.models.recommendation import Recommendation as RecommendationModel

class RecommendationRepositoryImpl(IRecommendationRepository):
    def create(self, user_id: int, recommendation_text: str) -> RecommendationEntity:
        m = RecommendationModel(user_id=user_id, recommendation_text=recommendation_text)
        db.session.add(m)
        db.session.commit()
        return RecommendationEntity(
            id=m.id,
            user_id=m.user_id,
            course_id=m.course_id,
            recommendation_text=m.recommendation_text,
            created_at=m.created_at,
            updated_at=m.updated_at
        )

    def list_for_user(self, user_id: int) -> List[RecommendationEntity]:
        ms = RecommendationModel.query.filter_by(user_id=user_id).all()
        return [
            RecommendationEntity(
                id=m.id,
                user_id=m.user_id,
                course_id=m.course_id,
                recommendation_text=m.recommendation_text,
                created_at=m.created_at,
                updated_at=m.updated_at
            ) for m in ms
        ]
