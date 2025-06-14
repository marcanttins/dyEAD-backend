# backend/infrastructure/repositories/email_repository_impl.py
from datetime import datetime, timezone
from typing import Any, Dict
from domain.repositories.email_repository import IEmailRepository
from application.dtos.email_dto import EmailDTO
from interfaces.tasks.send_async_email import send_async_email

class EmailRepositoryImpl(IEmailRepository):
    """
    Implementação de IEmailRepository usando Celery para envio assíncrono.
    """

    def send(self, to: str, subject: str, body: str) -> EmailDTO:
        # Timestamp imediato de enfileiramento
        sent_at = datetime.now(timezone.utc)

        # Enfileira a tarefa Celery para envio de e-mail
        task = send_async_email.delay(to, subject, body)

        # Metadata pode conter o ID da task para rastreamento
        metadata: Dict[str, Any] = {'celery_task_id': task.id}

        return EmailDTO(
            to=to,
            subject=subject,
            body=body,
            sent_at=sent_at,
            message_id=str(task.id),
            metadata=metadata
        )
