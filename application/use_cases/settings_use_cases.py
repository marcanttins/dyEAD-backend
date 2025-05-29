# backend/application/use_cases/settings_use_cases.py
from typing import Dict, Any, Optional
from domain.repositories.settings_repository import ISettingsRepository
from domain.entities.settings import Settings

class GetSettingsUseCase:
    def __init__(self, repo: ISettingsRepository):
        self.repo = repo

    def execute(self, user_id: int) -> Optional[Settings]:
        return self.repo.get_by_user(user_id)

class CreateSettingsUseCase:
    def __init__(self, repo: ISettingsRepository):
        self.repo = repo

    def execute(self, user_id: int, prefs: Dict[str, Any]) -> Settings:
        return self.repo.create(user_id, prefs)

class UpdateSettingsUseCase:
    def __init__(self, repo: ISettingsRepository):
        self.repo = repo

    def execute(self, user_id: int, prefs: Dict[str, Any]) -> Settings:
        settings = self.repo.get_by_user(user_id)
        return self.repo.update(settings, prefs)
