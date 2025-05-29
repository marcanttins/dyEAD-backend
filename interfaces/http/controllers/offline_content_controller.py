# backend/interface/http/controllers/offline_content_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity

from infrastructure.security.jwt import token_required
from application.schemas.offline_content_schema import (
    OfflineContentRequestSchema,
    OfflineContentResponseSchema
)
from application.use_cases.offline_content_use_cases import (
    CreateOfflineContentUseCase,
    GetOfflineContentUseCase
)
from infrastructure.repositories.offline_content_repository_impl import OfflineContentRepositoryImpl
from domain.exceptions import APIError

offline_bp = Blueprint('offline_content', __name__, url_prefix='/offline-content')

_req_schema         = OfflineContentRequestSchema()
_resp_schema        = OfflineContentResponseSchema()
_list_resp_schema   = OfflineContentResponseSchema(many=True)


@offline_bp.route('/', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Conteúdo Offline'],
    'description': 'Cria um novo conteúdo offline para o usuário autenticado.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/OfflineContentRequest'}
    }],
    'responses': {
        201: {
            'description': 'Conteúdo offline criado com sucesso',
            'schema': {'$ref': '#/definitions/OfflineContentResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def create_offline_content():
    try:
        data = _req_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    user_id = get_jwt_identity()
    use_case = CreateOfflineContentUseCase(OfflineContentRepositoryImpl())
    try:
        content = use_case.execute(
            user_id      = user_id,
            content_type = data['content_type'],
            content_url  = data['content_url']
        )
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao criar conteúdo offline: %s", e)
        return jsonify({'message': 'Erro interno ao criar conteúdo offline'}), 500

    return jsonify(_resp_schema.dump(content)), 201


@offline_bp.route('/', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Conteúdo Offline'],
    'description': 'Lista todos os conteúdos offline do usuário autenticado.',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Lista de conteúdos offline',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/OfflineContentResponse'}
            }
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def list_offline_content():
    user_id = get_jwt_identity()
    use_case = GetOfflineContentUseCase(OfflineContentRepositoryImpl())
    try:
        contents = use_case.execute(user_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao listar conteúdos offline: %s", e)
        return jsonify({'message': 'Erro interno ao listar conteúdos offline'}), 500

    return jsonify(_list_resp_schema.dump(contents)), 200
