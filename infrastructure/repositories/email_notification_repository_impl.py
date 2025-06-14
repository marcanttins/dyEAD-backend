from typing import Dict, Any, List
from domain.repositories.email_notification_repository import IEmailNotificationRepository
from domain.entities.email_notification import EmailNotification
from infrastructure.database import db
from sqlalchemy.exc import SQLAlchemyError
from domain.exceptions import APIError

class EmailNotificationRepositoryImpl(IEmailNotificationRepository):
    def create(self, data: Dict[str, Any]) -> EmailNotification:
        try:
            notification = EmailNotification(
                subject=data['subject'],
                content=data['content'],
                recipients=data['recipients'],
                template_type=data['template_type']
            )
            db.session.add(notification)
            db.session.commit()
            return notification
        except SQLAlchemyError as e:
            db.session.rollback()
            raise APIError('Erro ao criar notificação', 500)

    def get_or_404(self, notification_id: int) -> EmailNotification:
        notification = EmailNotification.query.get(notification_id)
        if not notification:
            raise APIError('Notificação não encontrada', 404)
        return notification

    def list_all(self) -> List[EmailNotification]:
        return EmailNotification.query.all()

    def update_status(self, notification: EmailNotification, status: str) -> EmailNotification:
        try:
            notification.status = status
            db.session.commit()
            return notification
        except SQLAlchemyError as e:
            db.session.rollback()
            raise APIError('Erro ao atualizar status', 500)

    def delete(self, notification: EmailNotification) -> None:
        try:
            db.session.delete(notification)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise APIError('Erro ao deletar notificação', 500)
