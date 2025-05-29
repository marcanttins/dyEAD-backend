# backend/infrastructure/repositories/report_repository_impl.py
from domain.repositories.report_repository import IReportRepository
from infrastructure.orm.models.user import User as UserModel

class ReportRepositoryImpl(IReportRepository):
    def count_users(self) -> int:
        return UserModel.query.count()
