from typing import Dict, Any, List
from domain.repositories.email_notification_repository import IEmailNotificationRepository
from domain.entities.email_notification import EmailNotification

class CreateEmailNotificationUseCase:
    def __init__(self, notification_repo: IEmailNotificationRepository):
        self.notification_repo = notification_repo

    def execute(self, data: Dict[str, Any]) -> EmailNotification:
        return self.notification_repo.create(data)

class GetEmailNotificationUseCase:
    def __init__(self, notification_repo: IEmailNotificationRepository):
        self.notification_repo = notification_repo

    def execute(self, notification_id: int) -> EmailNotification:
        return self.notification_repo.get_or_404(notification_id)

class ListEmailNotificationsUseCase:
    def __init__(self, notification_repo: IEmailNotificationRepository):
        self.notification_repo = notification_repo

    def execute(self) -> List[EmailNotification]:
        return self.notification_repo.list_all()

class UpdateEmailNotificationStatusUseCase:
    def __init__(self, notification_repo: IEmailNotificationRepository):
        self.notification_repo = notification_repo

    def execute(self, notification_id: int, status: str) -> EmailNotification:
        notification = self.notification_repo.get_or_404(notification_id)
        return self.notification_repo.update_status(notification, status)

class DeleteEmailNotificationUseCase:
    def __init__(self, notification_repo: IEmailNotificationRepository):
        self.notification_repo = notification_repo

    def execute(self, notification_id: int) -> None:
        notification = self.notification_repo.get_or_404(notification_id)
        self.notification_repo.delete(notification)
