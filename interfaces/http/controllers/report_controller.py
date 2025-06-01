# backend/interface/http/controllers/report_controller.py

from flasgger import swag_from
from flask import Blueprint, jsonify, current_app

from infrastructure.security.jwt import token_required
from application.use_cases.report_use_cases import CountUsersUseCase
from infrastructure.repositories.report_repository_impl import ReportRepositoryImpl
from application.schemas.reports_schema import UserCountReportSchema
from domain.exceptions import APIError

report_bp = Blueprint('reports', __name__, url_prefix='/reports')
_report_schema = UserCountReportSchema()


@report_bp.route('/users/count', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Relatórios'],
    'description': 'Retorna o total de usuários cadastrados na plataforma.',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Total de usuários retornado com sucesso',
            'schema': {'$ref': '#/definitions/UserCountReport'}
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def get_users_count():
    """
    Endpoint para contar usuários.
    """
    try:
        use_case = CountUsersUseCase(ReportRepositoryImpl())
        total = use_case.execute()
    except APIError as e:
        current_app.logger.warning("APIError ao obter contagem de usuários: %s", e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro inesperado ao obter contagem de usuários: %s", e)
        return jsonify({'message': 'Erro interno ao obter contagem de usuários'}), 500

    # Serializa o resultado
    return jsonify(_report_schema.dump({'total_users': total})), 200
