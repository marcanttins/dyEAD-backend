# backend/infrastructure/repositories/progress_repository_impl.py
from typing import Optional
from sqlalchemy import func
from infrastructure.extensions import db
from infrastructure.orm.models.progress import Progress
from domain.repositories.progress_repository import IProgressRepository

class ProgressRepositoryImpl(IProgressRepository):
    """
    Implementação SQLAlchemy de IProgressRepository.
    """
    def create(self, user_id: int, course_id: int) -> Progress:
        """
        Cria um novo registro de progresso com 0% inicial.
        """
        progress = Progress(user_id=user_id, course_id=course_id, percentage=0.0)
        db.session.add(progress)
        db.session.commit()
        return progress

    def update(self, progress: Progress) -> Progress:
        """
        Atualiza o registro de progresso existente.
        """
        existing = db.session.query(Progress).get(progress.id)
        if not existing:
            raise ValueError("Progresso não encontrado")
        existing.percentage = progress.percentage
        db.session.commit()
        return existing

    def get_by_user_and_course(self, user_id: int, course_id: int) -> Optional[Progress]:
        """
        Retorna o registro de progresso de um usuário em um curso.
        """
        return db.session.query(Progress).filter_by(
            user_id=user_id,
            course_id=course_id
        ).first()

    def avg_progress_for_user(self, user_id: int) -> float:
        """
        Calcula a média do progresso para um usuário em todos os cursos.
        """
        result = db.session.query(func.avg(Progress.percentage)).filter_by(
            user_id=user_id
        ).scalar()
        return float(result or 0.0)

    def average_progress_all(self) -> float:
        """
        Calcula a média do progresso para todos os usuários em todos os cursos.
        """
        result = db.session.query(func.avg(Progress.percentage)).scalar()
        return float(result or 0.0)
