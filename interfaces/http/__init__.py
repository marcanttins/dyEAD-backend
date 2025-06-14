# backend/interface/http/__init__.py
"""
Pacote que contém a camada de interface HTTP (API REST).
Define o entrypoint da aplicação e agrupa controllers.
"""

# O pacote importa a factory para facilitar importações em run.py
from .app import create_app
from .error_handlers import register_error_handlers

__all__ = [
    "create_app",
    "register_error_handlers"
]