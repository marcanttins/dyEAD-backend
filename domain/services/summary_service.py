# backend/domain/services/summary_service.py
from typing import Dict

from domain.repositories.course_repository import ICourseRepository
from domain.repositories.progress_repository import IProgressRepository
from domain.repositories.user_repository import IUserRepository


class SummaryService:
    """
    Serviço de domínio para gerar métricas resumidas da plataforma:
      - total de usuários
      - total de cursos
      - progresso médio global
    """

    def __init__(
            self,
            user_repo: IUserRepository,
            course_repo: ICourseRepository,
            progress_repo: IProgressRepository
    ):
        self._user_repo = user_repo
        self._course_repo = course_repo
        self._progress_repo = progress_repo

        # backend/domain/services/summary_service.py

    def get_summary(self) -> Dict[str, float]:
        total_users = self._user_repo.count_all()
        total_courses = self._course_repo.count_all()
        # chama o método definido na interface
        average_progress = self._progress_repo.average_progress_all()

        return {
            'total_users': total_users,
            'total_courses': total_courses,
            'average_progress_global': average_progress
        }
