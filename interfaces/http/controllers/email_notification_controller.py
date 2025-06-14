from flasgger import swag_from
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError

from application.use_cases.email_notification_use_cases import (
    CreateEmailNotificationUseCase,
    GetEmailNotificationUseCase,
    ListEmailNotificationsUseCase,
    UpdateEmailNotificationStatusUseCase,
    DeleteEmailNotificationUseCase,
)
from infrastructure.repositories.email_notification_repository_impl import EmailNotificationRepositoryImpl
from domain.exceptions import APIError
from infrastructure.security.jwt import token_required, roles_required
from application.schemas.email_notification_schema import EmailNotificationRequestSchema, EmailNotificationResponseSchema

notifications_bp = Blueprint('notifications', __name__)
_request_schema = EmailNotificationRequestSchema()
_response_schema = EmailNotificationResponseSchema()
_list_schema = EmailNotificationResponseSchema(many=True)

@notifications_bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Notificações'],
    'description': 'Cria uma nova notificação de email.',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/EmailNotificationRequest'}
        }
    ],
    'responses': {
        201: {'description': 'Notificação criada com sucesso', 'schema': {'$ref': '#/definitions/EmailNotificationResponse'}},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
@roles_required('admin')
def create_notification():
    try:
        data = _request_schema.load(request.json)
        use_case = CreateEmailNotificationUseCase(EmailNotificationRepositoryImpl())
        notification = use_case.execute(data)
        return _response_schema.dump(notification), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except APIError as err:
        return jsonify({'error': str(err)}), err.status_code

@notifications_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Notificações'],
    'description': 'Lista todas as notificações de email.',
    'responses': {
        200: {'description': 'Lista de notificações', 'schema': {'$ref': '#/definitions/EmailNotificationResponse'}},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
@roles_required('admin')
def list_notifications():
    try:
        use_case = ListEmailNotificationsUseCase(EmailNotificationRepositoryImpl())
        notifications = use_case.execute()
        return _list_schema.dump(notifications)
    except APIError as err:
        return jsonify({'error': str(err)}), err.status_code

@notifications_bp.route('/<int:notification_id>', methods=['GET'])
@swag_from({
    'tags': ['Notificações'],
    'description': 'Obtém detalhes de uma notificação específica.',
    'parameters': [
        {
            'in': 'path',
            'name': 'notification_id',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        200: {'description': 'Detalhes da notificação', 'schema': {'$ref': '#/definitions/EmailNotificationResponse'}},
        401: {'description': 'Token inválido ou ausente'},
        404: {'description': 'Notificação não encontrada'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
@roles_required('admin')
def get_notification(notification_id):
    try:
        use_case = GetEmailNotificationUseCase(EmailNotificationRepositoryImpl())
        notification = use_case.execute(notification_id)
        return _response_schema.dump(notification)
    except APIError as err:
        return jsonify({'error': str(err)}), err.status_code

@notifications_bp.route('/<int:notification_id>/status', methods=['PUT'])
@swag_from({
    'tags': ['Notificações'],
    'description': 'Atualiza o status de uma notificação.',
    'parameters': [
        {
            'in': 'path',
            'name': 'notification_id',
            'required': True,
            'type': 'integer'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {'type': 'object', 'properties': {'status': {'type': 'string'}}}
        }
    ],
    'responses': {
        200: {'description': 'Status atualizado com sucesso', 'schema': {'$ref': '#/definitions/EmailNotificationResponse'}},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        404: {'description': 'Notificação não encontrada'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
@roles_required('admin')
def update_notification_status(notification_id):
    try:
        status = request.json.get('status')
        if not status:
            return jsonify({'error': 'status é obrigatório'}), 400
        
        use_case = UpdateEmailNotificationStatusUseCase(EmailNotificationRepositoryImpl())
        notification = use_case.execute(notification_id, status)
        return _response_schema.dump(notification)
    except APIError as err:
        return jsonify({'error': str(err)}), err.status_code

@notifications_bp.route('/<int:notification_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Notificações'],
    'description': 'Exclui uma notificação específica.',
    'parameters': [
        {
            'in': 'path',
            'name': 'notification_id',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        204: {'description': 'Notificação excluída com sucesso'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        404: {'description': 'Notificação não encontrada'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
@roles_required('admin')
def delete_notification(notification_id):
    try:
        use_case = DeleteEmailNotificationUseCase(EmailNotificationRepositoryImpl())
        use_case.execute(notification_id)
        return '', 204
    except APIError as err:
        return jsonify({'error': str(err)}), err.status_code
