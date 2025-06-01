# backend/infrastructure/tasks/send_async_email.py
from celery import shared_task
from datetime import datetime, timezone
from flask_mail import Message
from infrastructure.extensions import mail

@shared_task(name='send_async_email')
def send_async_email(to: str, subject: str, body: str) -> dict:
    """
    Envia um e-mail de forma assíncrona usando Celery.

    Args:
        to (str): Endereço do destinatário.
        subject (str): Assunto da mensagem.
        body (str): Conteúdo da mensagem.

    Returns:
        dict: Informações sobre o envio, incluindo timestamp.
    """
    msg = Message(subject, recipients=[to], body=body)
    mail.send(msg)
    return {
        'to': to,
        'subject': subject,
        'sent_at': datetime.now(timezone.utc).isoformat()
    }
