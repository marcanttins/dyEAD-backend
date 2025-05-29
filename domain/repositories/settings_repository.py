# backend/domain/repositories/settings_repository.py
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from domain.entities.settings import Settings

class ISettingsRepository(ABC):
    @abstractmethod
    def get_by_user(self, user_id: int) -> Optional[Settings]:
        """Retorna o objeto Settings de um usuário."""
        pass

    @abstractmethod
    def create(self, user_id: int, preferences: Dict[str, Any]) -> Settings:
        """Cria um novo Settings para o usuário."""
        pass

    @abstractmethod
    def update(self, settings: Settings, preferences: Dict[str, Any]) -> Settings:
        """Atualiza as preferências de um Settings existente."""
        pass
