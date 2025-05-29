# backend/application/use_cases/report_use_cases.py
from domain.repositories.report_repository import IReportRepository

class CountUsersUseCase:
    def __init__(self, repo: IReportRepository):
        self.repo = repo

    def execute(self) -> int:
        return self.repo.count_users()
