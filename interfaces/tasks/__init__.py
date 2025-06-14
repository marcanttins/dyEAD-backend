# backend/infrastructure/tasks/__init__.py
"""
Pacote de tasks assíncronas gerenciadas pelo Celery.
"""
from .send_async_email import send_async_email
from .generate_certificate import generate_certificate_task

__all__ = [
    'send_async_email',
    'generate_certificate_task',
]
