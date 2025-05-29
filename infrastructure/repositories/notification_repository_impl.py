# backend/infrastructure/repositories/notification_repository_impl.py
from typing import List, Optional
from domain.repositories.notification_repository import INotificationRepository
from domain.entities.notification import Notification as NotificationEntity
from infrastructure.extensions import db
from infrastructure.orm.models.notification import Notification as NotificationModel

class NotificationRepositoryImpl(INotificationRepository):
    def create(self, user_id: int, message: str) -> NotificationEntity:
        m = NotificationModel(user_id=user_id, message=message)
        db.session.add(m)
        db.session.commit()
        return NotificationEntity(
            id=m.id,
            user_id=m.user_id,
            message=m.message,
            read_status=m.read_status,
            created_at=m.created_at
        )

    def list_for_user(self, user_id: int) -> List[NotificationEntity]:
        ms = NotificationModel.query.filter_by(user_id=user_id).all()
        return [
            NotificationEntity(
                id=m.id,
                user_id=m.user_id,
                message=m.message,
                read_status=m.read_status,
                created_at=m.created_at
            ) for m in ms
        ]

    def list_unread(self, user_id: int) -> List[NotificationEntity]:
        ms = NotificationModel.query.filter_by(user_id=user_id, read_status=False).all()
        return [
            NotificationEntity(
                id=m.id,
                user_id=m.user_id,
                message=m.message,
                read_status=m.read_status,
                created_at=m.created_at
            ) for m in ms
        ]

    def get_by_id(self, notification_id: int) -> Optional[NotificationEntity]:
        m = NotificationModel.query.get(notification_id)
        if not m:
            return None
        return NotificationEntity(
            id=m.id,
            user_id=m.user_id,
            message=m.message,
            read_status=m.read_status,
            created_at=m.created_at
        )

    def mark_as_read(self, notification: NotificationEntity) -> NotificationEntity:
        m = NotificationModel.query.get(notification.id)
        if not m:
            raise ValueError("Notification not found")
        m.read_status = True
        db.session.commit()
        return NotificationEntity(
            id=m.id,
            user_id=m.user_id,
            message=m.message,
            read_status=m.read_status,
            created_at=m.created_at
        )
