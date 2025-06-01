# backend/interface/http/controllers/feedback_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from application.schemas.feedback_schema import FeedbackRequestSchema, FeedbackResponseSchema
from application.use_cases.feedback_use_cases import (
    CreateFeedbackUseCase,
    ListFeedbackByCourseUseCase,
    ListFeedbackByUserUseCase
)
from infrastructure.repositories.feedback_repository_impl import FeedbackRepositoryImpl
from domain.exceptions import APIError

feedback_bp = Blueprint('feedback', __name__)

_request_schema       = FeedbackRequestSchema()
_response_schema      = FeedbackResponseSchema()
_list_response_schema = FeedbackResponseSchema(many=True)


@feedback_bp.route('/', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Feedback'],
    'description': 'Cria um novo feedback para um curso.',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/FeedbackRequest'}
    }],
    'responses': {
        201: {
            'description': 'Feedback criado com sucesso',
            'schema': {'$ref': '#/definitions/FeedbackResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def create_feedback():
    try:
        data = _request_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    user_id = get_jwt_identity()
    use_case = CreateFeedbackUseCase(FeedbackRepositoryImpl())

    try:
        feedback = use_case.execute(
            user_id   = user_id,
            course_id = data['course_id'],
            message   = data['message'],
            sentiment = data['sentiment']
        )
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao criar feedback: %s", e)
        return jsonify({'message': 'Erro interno ao criar feedback'}), 500

    return jsonify(_response_schema.dump(feedback)), 201


@feedback_bp.route('/course/<int:course_id>', methods=['GET'])
@swag_from({
    'tags': ['Feedback'],
    'description': 'Lista todos os feedbacks de um curso específico.',
    'parameters': [{
        'in': 'path',
        'name': 'course_id',
        'type': 'integer',
        'required': True,
        'description': 'ID do curso'
    }],
    'responses': {
        200: {
            'description': 'Lista de feedbacks',
            'schema': {'type': 'array', 'items': {'$ref': '#/definitions/FeedbackResponse'}}
        },
        404: {'description': 'Curso não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def list_feedback_by_course(course_id: int):
    use_case = ListFeedbackByCourseUseCase(FeedbackRepositoryImpl())
    try:
        feedbacks = use_case.execute(course_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao listar feedbacks do curso %s: %s", course_id, e)
        return jsonify({'message': 'Erro interno ao listar feedbacks'}), 500

    return jsonify(_list_response_schema.dump(feedbacks)), 200


@feedback_bp.route('/me', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Feedback'],
    'description': 'Lista todos os feedbacks do usuário autenticado.',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Feedbacks do usuário',
            'schema': {'type': 'array', 'items': {'$ref': '#/definitions/FeedbackResponse'}}
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def list_my_feedback():
    user_id = get_jwt_identity()
    use_case = ListFeedbackByUserUseCase(FeedbackRepositoryImpl())

    try:
        feedbacks = use_case.execute(user_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao listar feedbacks do usuário %s: %s", user_id, e)
        return jsonify({'message': 'Erro interno ao listar feedbacks'}), 500

    return jsonify(_list_response_schema.dump(feedbacks)), 200
