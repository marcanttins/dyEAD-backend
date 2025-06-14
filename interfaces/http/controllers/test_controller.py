# backend/interface/http/controllers/test_controller.py

from flasgger import swag_from
from flask import Blueprint
from domain.exceptions import APIError

test_bp = Blueprint('test', __name__, url_prefix='/test')


@test_bp.route('/api-error', methods=['GET'])
@swag_from({
    'tags': ['Teste'],
    'description': 'Dispara um APIError para simular erro de negócio.',
    'responses': {
        422: {
            'description': 'Erro de validação de negócio',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Este é um erro de teste (APIError)'
                    },
                    'errors': {
                        'type': 'object',
                        'example': {'field': 'mensagem inválida'}
                    }
                }
            }
        }
    }
})
def test_api_error():
    """
    Simula um erro de negócio usando APIError.
    """
    raise APIError(
        message="Este é um erro de teste (APIError)",
        status_code=422,
        errors={"field": "mensagem inválida"}
    )


@test_bp.route('/exception', methods=['GET'])
@swag_from({
    'tags': ['Teste'],
    'description': 'Dispara uma exceção genérica para simular erro inesperado.',
    'responses': {
        500: {
            'description': 'Erro interno inesperado',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Erro interno inesperado para teste'
                    }
                }
            }
        }
    }
})
def test_exception():
    """
    Simula um erro interno inesperado (exceção genérica).
    """
    raise RuntimeError("Erro interno inesperado para teste")
