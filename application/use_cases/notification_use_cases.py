# backend/application/use_cases/notification_use_cases.py
from typing import List
from domain.repositories.notification_repository import INotificationRepository
from domain.entities.notification import Notification

class SendNotificationUseCase:
    def __init__(self, notif_repo: INotificationRepository):
        self.notif_repo = notif_repo

    def execute(self, user_id: int, message: str) -> Notification:
        return self.notif_repo.create(user_id, message)

class ListNotificationsUseCase:
    def __init__(self, notif_repo: INotificationRepository):
        self.notif_repo = notif_repo

    def execute(self, user_id: int) -> List[Notification]:
        return self.notif_repo.list_for_user(user_id)

class ListUnreadNotificationsUseCase:
    def __init__(self, notif_repo: INotificationRepository):
        self.notif_repo = notif_repo

    def execute(self, user_id: int) -> List[Notification]:
        return self.notif_repo.list_unread(user_id)

class MarkNotificationReadUseCase:
    def __init__(self, notif_repo: INotificationRepository):
        self.notif_repo = notif_repo

    def execute(self, notification_id: int) -> Notification:
        notif = self.notif_repo.get_by_id(notification_id)
        if not notif:
            raise ValueError("Notificação não encontrada")
        return self.notif_repo.mark_as_read(notif)
