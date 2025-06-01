# backend/infrastructure/logger.py
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

def setup_logging(app: Flask) -> None:
    """
    Configura o logger principal do Flask para usar rotações de arquivo,
    níveis e formato definidos em app.config.
    Espera estas chaves de configuração em app.config:
      LOGGER_FILE, LOGGER_MAX_BYTES, LOGGER_BACKUP_COUNT, LOGGER_ENCODING
    """
    # Remove handlers padrão para não duplicar logs
    for handler in list(app.logger.handlers):
        app.logger.removeHandler(handler)

    # Cria um handler rotativo
    level = getattr(logging, app.config['LOG_LEVEL'].upper(), logging.INFO)
    handler = RotatingFileHandler(
        filename=app.config['LOGGER_FILE'],
        maxBytes=app.config['LOGGER_MAX_BYTES'],
        backupCount=app.config['LOGGER_BACKUP_COUNT'],
        encoding=app.config['LOGGER_ENCODING']
    )
    handler.setLevel(level)

    # Formato de saída: timestamp, nível, logger, arquivo:linha e mensagem
    fmt = logging.Formatter(
        '%(asctime)s %(levelname)-5s [%(name)s] %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(fmt)

    # Ajusta o logger da aplicação
    app.logger.setLevel(level)
    app.logger.addHandler(handler)
