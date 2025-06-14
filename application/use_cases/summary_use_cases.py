# backend/application/use_cases/summary_use_cases.py
from domain.services import SummaryService
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.repositories.course_repository_impl import CourseRepositoryImpl
from infrastructure.repositories.progress_repository_impl import ProgressRepositoryImpl

class GetSummaryUseCase:
    """
    Use case que delega ao SummaryService a geração do resumo.
    """
    def __init__(self):
        # injeta as implementações concretas de repositório no serviço de domínio
        self._service = SummaryService(
            UserRepositoryImpl(),
            CourseRepositoryImpl(),
            ProgressRepositoryImpl()
        )

    def execute(self):
        return self._service.get_summary()

