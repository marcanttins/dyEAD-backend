# backend/infrastructure/repositories/settings_repository_impl.py
from typing import Optional, Dict, Any
from domain.repositories.settings_repository import ISettingsRepository
from domain.entities.settings import Settings as SettingsEntity
from infrastructure.extensions import db
from infrastructure.orm.models.settings import Settings as SettingsModel

class SettingsRepositoryImpl(ISettingsRepository):
    def get_by_user(self, user_id: int) -> Optional[SettingsEntity]:
        m = SettingsModel.query.filter_by(user_id=user_id).first()
        if not m:
            return None
        return SettingsEntity(
            id=m.id,
            user_id=m.user_id,
            preferences=m.preferences,
            updated_at=m.updated_at
        )

    def create(self, user_id: int, preferences: Dict[str, Any]) -> SettingsEntity:
        m = SettingsModel(user_id=user_id, preferences=preferences)
        db.session.add(m)
        db.session.commit()
        return SettingsEntity(
            id=m.id,
            user_id=m.user_id,
            preferences=m.preferences,
            updated_at=m.updated_at
        )

    def update(self, settings: SettingsEntity, preferences: Dict[str, Any]) -> SettingsEntity:
        m = SettingsModel.query.get(settings.id)
        if not m:
            raise ValueError("Settings not found")
        m.preferences = preferences
        db.session.commit()
        return SettingsEntity(
            id=m.id,
            user_id=m.user_id,
            preferences=m.preferences,
            updated_at=m.updated_at
        )
