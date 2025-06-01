# backend/interface/http/controllers/summary_controller.py

from flasgger import swag_from
from flask import Blueprint, jsonify, current_app
from infrastructure.security.jwt import token_required
from application.use_cases.summary_use_cases import GetSummaryUseCase
from application.schemas.summary_schema import SummarySchema
from domain.exceptions import APIError

summary_bp = Blueprint('summary', __name__, url_prefix='/summary')
_summary_schema = SummarySchema()

@summary_bp.route('/', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Resumo'],
    'description': 'Retorna métricas resumidas da plataforma:\n'
                   '  - total_users\n'
                   '  - total_courses\n'
                   '  - average_progress_global',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Resumo retornado com sucesso',
            'schema': {'$ref': '#/definitions/Summary'}
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def get_summary():
    """
    Handler para obter o resumo de métricas da plataforma.
    """
    try:
        use_case = GetSummaryUseCase()
        summary = use_case.execute()
    except APIError as e:
        current_app.logger.warning("APIError ao obter resumo: %s", e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro interno ao obter resumo: %s", e)
        return jsonify({'message': 'Erro interno ao obter resumo'}), 500

    return jsonify(_summary_schema.dump(summary)), 200
