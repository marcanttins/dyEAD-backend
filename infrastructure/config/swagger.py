# backend/infrastructure/config/swagger.py
from flasgger import Swagger
from flask import Flask


def setup_swagger(app: Flask) -> None:
    """Configura a documentação Swagger para a app Flask."""
    template = {
        'swagger': '2.0',
        'info': {
            'title': 'API da Plataforma EAD',
            'description': (
                'Documentação da API da Plataforma EAD, inclusive autenticação JWT.'
            ),
            'version': '1.0.0',
        },
        'host': app.config.get('SWAGGER_HOST', 'localhost:5000'),
        'basePath': '/',
        'schemes': ['http', 'https'],
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': (
                    "JWT Authorization header usando Bearer. Ex: 'Bearer {token}'"
                ),
            }
        },
        'security': [{'Bearer': []}],
    }
    Swagger(app, template=template)
