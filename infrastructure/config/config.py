# backend/infrastructure/config/config.py

import os
from datetime import timedelta
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """
    Configurações base compartilhadas por todos os ambientes.
    """
    DEBUG: bool = False
    TESTING: bool = False

    SECRET_KEY: str = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY não definido no ambiente")

    SQLALCHEMY_DATABASE_URI: str = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(
        minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_MINUTES', '15'))
    )
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(
        days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES_DAYS', '7'))
    )
    PROPAGATE_EXCEPTIONS: bool = True

    CELERY_BROKER_URL: str = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND: str = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    MAIL_SERVER: str = os.getenv('MAIL_SERVER', 'smtp.example.com')
    MAIL_PORT: int = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS: bool = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME: str = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD')

    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOGGER_FILE: str = os.getenv('LOG_FILE', 'app.log')
    LOGGER_MAX_BYTES: int = int(os.getenv('LOG_MAX_BYTES', '10000000'))
    LOGGER_BACKUP_COUNT: int = int(os.getenv('LOG_BACKUP_COUNT', '5'))
    LOGGER_ENCODING: str = os.getenv('LOG_ENCODING', 'utf-8')

    RATELIMIT_STORAGE_URL: str = os.getenv('RATE_LIMIT_STORAGE_URL', 'redis://localhost:6379/1')



class DevelopmentConfig(Config):
    """
    Configurações específicas para desenvolvimento.
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Configurações específicas para testes automatizados.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


class ProductionConfig(Config):
    """
    Configurações específicas para produção.
    """
    pass


# Mapeia chave de ambiente para classe de configuração
config_by_name = {
    # keys longas
    'development': DevelopmentConfig,
    'testing'   : TestingConfig,
    'production': ProductionConfig,
    # aliases curtas
    'dev' : DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,
}