# backend/infrastructure/config/limiter.py

from flask import request, Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def custom_key_func():
    if request.method == "OPTIONS" or request.path in ['/api/auth/logout', '/api/auth/login']:
        return None  # Ignora rate limit para CORS preflight
    return get_remote_address()  # Limita outras requisições por IP

def make_limiter(app: Flask) -> Limiter:
    """Cria e configura o Limiter de requisições para a app Flask."""
    limiter = Limiter(
        app=app,
        key_func=custom_key_func,
        storage_uri=app.config['RATELIMIT_STORAGE_URL'],
        default_limits=["200 per day", "50 per hour"]
    )

    return limiter

