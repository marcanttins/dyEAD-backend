# backend/infrastructure/config/celery.py
from celery import Celery
from flask import Flask


def make_celery(app: Flask) -> Celery:
    """Cria e configura instância do Celery baseada na app Flask."""
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
    )
    celery.conf.update(app.config)
    return celery
