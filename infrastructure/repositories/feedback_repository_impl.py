# backend/infrastructure/repositories/feedback_repository_impl.py
from typing import List
from domain.repositories.feedback_repository import IFeedbackRepository
from domain.entities.feedback import Feedback as FeedbackEntity
from infrastructure.extensions import db
from infrastructure.orm.models.feedback import Feedback as FeedbackModel

class FeedbackRepositoryImpl(IFeedbackRepository):
    def create(self, user_id: int, course_id: int, message: str, sentiment: str) -> FeedbackEntity:
        model = FeedbackModel(
            user_id=user_id, course_id=course_id,
            message=message, sentiment=sentiment
        )
        db.session.add(model)
        db.session.commit()
        return FeedbackEntity(
            id=model.id, user_id=model.user_id,
            course_id=model.course_id, message=model.message,
            sentiment=model.sentiment, created_at=model.created_at
        )

    def list_by_course(self, course_id: int) -> List[FeedbackEntity]:
        return [
            FeedbackEntity(
                id=m.id, user_id=m.user_id, course_id=m.course_id,
                message=m.message, sentiment=m.sentiment,
                created_at=m.created_at
            ) for m in FeedbackModel.query.filter_by(course_id=course_id).all()
        ]

    def list_by_user(self, user_id: int) -> List[FeedbackEntity]:
        return [
            FeedbackEntity(
                id=m.id, user_id=m.user_id, course_id=m.course_id,
                message=m.message, sentiment=m.sentiment,
                created_at=m.created_at
            ) for m in FeedbackModel.query.filter_by(user_id=user_id).all()
        ]
