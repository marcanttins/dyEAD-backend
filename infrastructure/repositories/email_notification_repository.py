from typing import Dict, Any, List
from domain.entities.email_notification import EmailNotification

class IEmailNotificationRepository:
    def create(self, data: Dict[str, Any]) -> EmailNotification:
        """Cria uma nova notificação de email."""
        pass

    def get_or_404(self, notification_id: int) -> EmailNotification:
        """Obtém uma notificação específica ou levanta erro 404."""
        pass

    def list_all(self) -> List[EmailNotification]:
        """Lista todas as notificações."""
        pass

    def update_status(self, notification: EmailNotification, status: str) -> EmailNotification:
        """Atualiza o status de uma notificação."""
        pass

    def delete(self, notification: EmailNotification) -> None:
        """Deleta uma notificação."""
        pass
