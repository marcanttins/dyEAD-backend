# backend/infrastructure/repositories/leaderboard_repository_impl.py
from typing import List, Dict
from sqlalchemy import func
from domain.repositories.leaderboard_repository import ILeaderboardRepository
from infrastructure.extensions import db
from infrastructure.orm.models.progress import Progress as ProgressModel
from infrastructure.orm.models.user import User as UserModel

class LeaderboardRepositoryImpl(ILeaderboardRepository):
    def get_global_leaderboard(self) -> List[Dict[str, float]]:
        results = db.session.query(
            ProgressModel.user_id,
            func.avg(ProgressModel.percentage).label('avg_percentage')
        ).group_by(ProgressModel.user_id) \
         .order_by(func.avg(ProgressModel.percentage).desc()) \
         .all()
        return [
            {'user_id': uid, 'average_percentage': avg}
            for uid, avg in results
        ]

    def get_global_leaderboard_with_names(self, limit: int = 10) -> List[Dict]:
        results = db.session.query(
            ProgressModel.user_id,
            func.avg(ProgressModel.percentage).label('avg_percentage'),
            UserModel.name
        ).join(UserModel, UserModel.id == ProgressModel.user_id) \
         .group_by(ProgressModel.user_id, UserModel.name) \
         .order_by(func.avg(ProgressModel.percentage).desc()) \
         .limit(limit) \
         .all()
        return [
            {'user_id': uid, 'name': name, 'average_percentage': avg}
            for uid, avg, name in results
        ]
