# backend/application/use_cases/dashboard_use_cases.py
from typing import Dict
from domain.repositories.report_repository import IReportRepository

class GetDashboardStatsUseCase:
    def __init__(self, report_repo: IReportRepository):
        self.repo = report_repo

    def execute(self) -> Dict[str, int]:
        total_users = self.repo.count_users()
        return {'total_users': total_users}
