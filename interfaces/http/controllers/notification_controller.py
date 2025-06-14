# backend/interface/http/controllers/notification_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError

from infrastructure.security.jwt import token_required, roles_required
from application.schemas.notification_schema import (
    NotificationRequestSchema,
    NotificationResponseSchema
)
from application.use_cases.notification_use_cases import (
    SendNotificationUseCase,
    ListNotificationsUseCase,
    ListUnreadNotificationsUseCase,
    MarkNotificationReadUseCase
)
from infrastructure.repositories.notification_repository_impl import NotificationRepositoryImpl
from domain.exceptions import APIError

notification_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

_req_schema        = NotificationRequestSchema()
_resp_schema       = NotificationResponseSchema()
_list_resp_schema  = NotificationResponseSchema(many=True)


@notification_bp.route('/', methods=['POST'])
@token_required
@roles_required('admin', 'instrutor')
@swag_from({
    'tags': ['Notificações'],
    'description': 'Envia uma notificação para um usuário específico.',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/NotificationRequest'}
    }],
    'responses': {
        201: {
            'description': 'Notificação enviada com sucesso',
            'schema': {'$ref': '#/definitions/NotificationResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def send_notification():
    try:
        data = _req_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    use_case = SendNotificationUseCase(NotificationRepositoryImpl())
    try:
        notification = use_case.execute(
            user_id = data['user_id'],
            message = data['message']
        )
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao enviar notificação: %s", e)
        return jsonify({'message': 'Erro interno ao enviar notificação'}), 500

    return jsonify(_resp_schema.dump(notification)), 201


@notification_bp.route('/', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Notificações'],
    'description': 'Lista todas as notificações do usuário autenticado.',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Lista de notificações',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/NotificationResponse'}
            }
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def list_notifications():
    user_id = int(get_jwt_identity())
    use_case = ListNotificationsUseCase(NotificationRepositoryImpl())
    try:
        notifications = use_case.execute(user_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao listar notificações: %s", e)
        return jsonify({'message': 'Erro interno ao listar notificações'}), 500

    return jsonify(_list_resp_schema.dump(notifications)), 200


@notification_bp.route('/unread', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Notificações'],
    'description': 'Lista apenas as notificações não lidas do usuário autenticado.',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Notificações não lidas',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/NotificationResponse'}
            }
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def list_unread_notifications():
    user_id = int(get_jwt_identity())
    use_case = ListUnreadNotificationsUseCase(NotificationRepositoryImpl())
    try:
        notifications = use_case.execute(user_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao listar notificações não lidas: %s", e)
        return jsonify({'message': 'Erro interno ao listar notificações não lidas'}), 500

    return jsonify(_list_resp_schema.dump(notifications)), 200


@notification_bp.route('/<int:notification_id>/read', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Notificações'],
    'description': 'Marca uma notificação como lida pelo seu ID.',
    'parameters': [{
        'in': 'path',
        'name': 'notification_id',
        'type': 'integer',
        'required': True,
        'description': 'ID da notificação'
    }],
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Notificação marcada como lida',
            'schema': {'$ref': '#/definitions/NotificationResponse'}
        },
        401: {'description': 'Token inválido ou ausente'},
        404: {'description': 'Notificação não encontrada'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def mark_notification_read(notification_id: int):
    use_case = MarkNotificationReadUseCase(NotificationRepositoryImpl())
    try:
        notification = use_case.execute(notification_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao marcar notificação %s como lida: %s", notification_id, e)
        return jsonify({'message': 'Erro interno ao marcar notificação como lida'}), 500

    return jsonify(_resp_schema.dump(notification)), 200
