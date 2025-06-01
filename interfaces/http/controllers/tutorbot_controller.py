# backend/interface/http/controllers/tutorbot_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError

from infrastructure.security.jwt import token_required
from infrastructure.repositories.ai_repository_impl import AiRepositoryImpl
from application.use_cases.tutorbot_use_cases import TutorBotUseCase
from application.schemas.tutorbot_schema import TutorBotRequestSchema, TutorBotResponseSchema
from domain.exceptions import APIError

tutorbot_bp = Blueprint('tutorbot', __name__, url_prefix='/tutorbot')

_req_schema  = TutorBotRequestSchema()
_resp_schema = TutorBotResponseSchema()


@tutorbot_bp.route('/', methods=['POST'])
@token_required
@swag_from({
    'tags': ['TutorBot'],
    'description': 'Envia um prompt para o TutorBot (IA) e retorna a resposta.',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/TutorBotRequest'}
        }
    ],
    'responses': {
        200: {
            'description': 'Interação bem-sucedida',
            'schema': {'$ref': '#/definitions/TutorBotResponse'}
        },
        400: {'description': 'Erro de validação do payload'},
        500: {'description': 'Erro interno ao processar prompt'}
    }
})
def send_tutorbot():
    try:
        data = _req_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'message': 'Erro de validação', 'errors': err.messages}), 400

    user_id = get_jwt_identity()
    use_case = TutorBotUseCase(AiRepositoryImpl())
    try:
        interaction = use_case.execute(user_id=user_id, prompt=data['prompt'])
    except APIError as e:
        current_app.logger.warning("TutorBot APIError: %s", e)
        return jsonify({'message': e.message}), 500
    except Exception as e:
        current_app.logger.exception("Erro interno no TutorBot: %s", e)
        return jsonify({'message': 'Erro interno ao processar prompt'}), 500

    return jsonify(_resp_schema.dump(interaction)), 200


@tutorbot_bp.route('/history', methods=['GET'])
@token_required
@swag_from({
    'tags': ['TutorBot'],
    'description': 'Retorna o histórico de interações do usuário autenticado com o TutorBot.',
    'responses': {
        200: {
            'description': 'Histórico de interações',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/TutorBotResponse'}
            }
        },
        500: {'description': 'Erro interno ao recuperar histórico'}
    }
})
def history_tutorbot():
    user_id = get_jwt_identity()
    use_case = TutorBotUseCase(AiRepositoryImpl())
    try:
        history = use_case.list_history(user_id=user_id)
    except APIError as e:
        current_app.logger.warning("TutorBot history APIError: %s", e)
        return jsonify({'message': e.message}), 500
    except Exception as e:
        current_app.logger.exception("Erro interno ao recuperar histórico TutorBot: %s", e)
        return jsonify({'message': 'Erro interno ao recuperar histórico'}), 500

    return jsonify(_resp_schema.dump(history, many=True)), 200
