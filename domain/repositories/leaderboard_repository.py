# backend/domain/repositories/leaderboard_repository.py
from abc import ABC, abstractmethod
from typing import List, Dict, Union

class ILeaderboardRepository(ABC):
    @abstractmethod
    def get_global_leaderboard(self) -> List[Dict[str, Union[int, float]]]:
        """Retorna ranking global por progresso acumulado."""
        pass

    @abstractmethod
    def get_global_leaderboard_with_names(self, limit: int = 10) -> List[Dict[str, Union[int, float, str]]]:
        """Ranking global com nomes de usuário, limitado."""
        pass
