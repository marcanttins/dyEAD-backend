# backend/application/use_cases/feedback_use_cases.py
from typing import List
from domain.repositories.feedback_repository import IFeedbackRepository
from domain.entities.feedback import Feedback

class CreateFeedbackUseCase:
    def __init__(self, feedback_repo: IFeedbackRepository):
        self.feedback_repo = feedback_repo

    def execute(self, user_id: int, course_id: int, message: str, sentiment: str) -> Feedback:
        return self.feedback_repo.create(user_id, course_id, message, sentiment)

class ListFeedbackByCourseUseCase:
    def __init__(self, feedback_repo: IFeedbackRepository):
        self.feedback_repo = feedback_repo

    def execute(self, course_id: int) -> List[Feedback]:
        return self.feedback_repo.list_by_course(course_id)

class ListFeedbackByUserUseCase:
    def __init__(self, feedback_repo: IFeedbackRepository):
        self.feedback_repo = feedback_repo

    def execute(self, user_id: int) -> List[Feedback]:
        return self.feedback_repo.list_by_user(user_id)
