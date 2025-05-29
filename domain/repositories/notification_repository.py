# backend/domain/repositories/notification_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.notification import Notification

class INotificationRepository(ABC):
    @abstractmethod
    def create(self, user_id: int, message: str) -> Notification:
        """Cria uma nova notificação."""
        pass

    @abstractmethod
    def list_for_user(self, user_id: int) -> List[Notification]:
        """Retorna todas as notificações de um usuário."""
        pass

    @abstractmethod
    def list_unread(self, user_id: int) -> List[Notification]:
        """Retorna notificações não lidas."""
        pass

    @abstractmethod
    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        """Retorna a notificação ou None se não existir."""
        pass

    @abstractmethod
    def mark_as_read(self, notification: Notification) -> Notification:
        """Marca uma notificação como lida."""
        pass
