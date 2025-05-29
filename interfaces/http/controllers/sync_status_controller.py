# backend/interface/http/controllers/sync_status_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity

from infrastructure.security.jwt import token_required
from application.schemas.sync_status_schema import (
    SyncStatusRequestSchema,
    SyncStatusResponseSchema
)
from application.use_cases.sync_status_use_cases import (
    GetSyncStatusUseCase,
    CreateSyncStatusUseCase,
    UpdateSyncStatusUseCase
)
from infrastructure.repositories.sync_status_repository_impl import SyncStatusRepositoryImpl
from domain.exceptions import APIError

sync_status_bp = Blueprint('sync_status', __name__, url_prefix='/sync-status')

_req_schema  = SyncStatusRequestSchema()
_resp_schema = SyncStatusResponseSchema()


@sync_status_bp.route('/', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Sincronização'],
    'description': 'Retorna o status de sincronização do usuário autenticado.',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Status de sincronização retornado com sucesso',
            'schema': {'$ref': '#/definitions/SyncStatusResponse'}
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def get_sync_status():
    user_id = int(get_jwt_identity())
    use_case = GetSyncStatusUseCase(SyncStatusRepositoryImpl())
    try:
        status = use_case.execute(user_id)
        if status is None:
            return jsonify({}), 200
        return jsonify(_resp_schema.dump(status)), 200
    except APIError as e:
        current_app.logger.warning("APIError ao obter status de sincronização: %s", e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro inesperado ao obter status de sincronização: %s", e)
        return jsonify({'message': 'Erro interno ao obter status de sincronização'}), 500


@sync_status_bp.route('/', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Sincronização'],
    'description': 'Cria o status de sincronização para o usuário autenticado.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/SyncStatusRequest'}
    }],
    'responses': {
        201: {
            'description': 'Status de sincronização criado com sucesso',
            'schema': {'$ref': '#/definitions/SyncStatusResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def create_sync_status():
    try:
        data = _req_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    user_id = int(get_jwt_identity())
    use_case = CreateSyncStatusUseCase(SyncStatusRepositoryImpl())
    try:
        status = use_case.execute(user_id, data['status'])
        return jsonify(_resp_schema.dump(status)), 201
    except APIError as e:
        current_app.logger.warning("APIError ao criar status de sincronização: %s", e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro inesperado ao criar status de sincronização: %s", e)
        return jsonify({'message': 'Erro interno ao criar status de sincronização'}), 500


@sync_status_bp.route('/', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Sincronização'],
    'description': 'Atualiza o status de sincronização do usuário autenticado.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/SyncStatusRequest'}
    }],
    'responses': {
        200: {
            'description': 'Status de sincronização atualizado com sucesso',
            'schema': {'$ref': '#/definitions/SyncStatusResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        404: {'description': 'Status de sincronização não encontrado'},
        500: {'description': 'Erro interno do servidor'}
    }
})
def update_sync_status():
    try:
        data = _req_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    user_id = int(get_jwt_identity())
    use_case = UpdateSyncStatusUseCase(SyncStatusRepositoryImpl())
    try:
        status = use_case.execute(user_id, data['status'])
        return jsonify(_resp_schema.dump(status)), 200
    except APIError as e:
        current_app.logger.warning("APIError ao atualizar status de sincronização: %s", e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro inesperado ao atualizar status de sincronização: %s", e)
        return jsonify({'message': 'Erro interno ao atualizar status de sincronização'}), 500
