# backend/infrastructure/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_marshmallow import Marshmallow

# Instâncias únicas de extensões para todo o projeto
# Importar em models, repositórios e tasks:

# SQLAlchemy para ORM (models, repositórios)
db = SQLAlchemy()
# Flask-Mail para envio de e-mails (tasks, infra)
mail = Mail()
# Marshmallow para serialização de dados (schemas, repositórios)
ma = Marshmallow()
