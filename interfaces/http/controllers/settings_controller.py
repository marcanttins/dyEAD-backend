# backend/interface/http/controllers/settings_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError

from infrastructure.security.jwt import token_required
from flask_jwt_extended import get_jwt_identity

from application.schemas.settings_schema import SettingsSchema
from application.use_cases.settings_use_cases import (
    GetSettingsUseCase,
    CreateSettingsUseCase,
    UpdateSettingsUseCase,
)
from infrastructure.repositories.settings_repository_impl import SettingsRepositoryImpl
from domain.exceptions import APIError

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')
_schema = SettingsSchema()


@settings_bp.route('/', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Configurações'],
    'description': 'Retorna as configurações do usuário autenticado.',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Configurações retornadas com sucesso',
            'schema': {'$ref': '#/definitions/SettingsResponse'}
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def get_settings():
    user_id = get_jwt_identity()
    use_case = GetSettingsUseCase(SettingsRepositoryImpl())
    try:
        settings = use_case.execute(user_id)
    except APIError as e:
        current_app.logger.warning("APIError ao obter configurações: %s", e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao obter configurações: %s", e)
        return jsonify({'message': 'Erro interno ao obter configurações'}), 500

    if settings is None:
        return jsonify({}), 200

    return jsonify(_schema.dump(settings)), 200


@settings_bp.route('/', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Configurações'],
    'description': 'Cria as configurações iniciais para o usuário autenticado.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/SettingsRequest'}
    }],
    'responses': {
        201: {
            'description': 'Configurações criadas com sucesso',
            'schema': {'$ref': '#/definitions/SettingsResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def create_settings():
    try:
        data = _schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    user_id = get_jwt_identity()
    use_case = CreateSettingsUseCase(SettingsRepositoryImpl())
    try:
        settings = use_case.execute(user_id, data['preferences'])
    except APIError as e:
        current_app.logger.warning("APIError ao criar configurações: %s", e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao criar configurações: %s", e)
        return jsonify({'message': 'Erro interno ao criar configurações'}), 500

    return jsonify(_schema.dump(settings)), 201


@settings_bp.route('/', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Configurações'],
    'description': 'Atualiza as configurações do usuário autenticado.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/SettingsRequest'}
    }],
    'responses': {
        200: {
            'description': 'Configurações atualizadas com sucesso',
            'schema': {'$ref': '#/definitions/SettingsResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        404: {'description': 'Configurações não encontradas'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def update_settings():
    try:
        data = _schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    user_id = get_jwt_identity()
    use_case = UpdateSettingsUseCase(SettingsRepositoryImpl())
    try:
        settings = use_case.execute(user_id, data.get('preferences'))
    except APIError as e:
        current_app.logger.warning("APIError ao atualizar configurações: %s", e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao atualizar configurações: %s", e)
        return jsonify({'message': 'Erro interno ao atualizar configurações'}), 500

    return jsonify(_schema.dump(settings)), 200
