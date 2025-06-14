# backend/application/use_cases/progress_use_cases.py
from typing import Optional
from domain.repositories.progress_repository import IProgressRepository
from domain.entities.progress import Progress

class CreateProgressUseCase:
    def __init__(self, repo: IProgressRepository):
        self.repo = repo

    def execute(self, user_id: int, course_id: int) -> Progress:
        return self.repo.create(user_id, course_id)

class UpdateProgressUseCase:
    def __init__(self, repo: IProgressRepository):
        self.repo = repo

    def execute(self, user_id: int, course_id: int, percentage: float) -> Progress:
        prog = self.repo.get_by_user_and_course(user_id, course_id)
        prog.percentage = percentage
        return self.repo.update(prog)

class GetProgressUseCase:
    def __init__(self, repo: IProgressRepository):
        self.repo = repo

    def execute(self, user_id: int, course_id: int) -> Optional[Progress]:
        return self.repo.get_by_user_and_course(user_id, course_id)

class AverageProgressUseCase:
    def __init__(self, repo: IProgressRepository):
        self.repo = repo

    def execute(self, user_id: int) -> float:
        return self.repo.avg_progress_for_user(user_id)
