# backend/interface/http/controllers/progress_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError

from infrastructure.security.jwt import token_required
from application.schemas.progress_schema import (
    ProgressCreateRequestSchema,
    ProgressUpdateRequestSchema,
    ProgressResponseSchema
)
from application.use_cases.progress_use_cases import (
    CreateProgressUseCase,
    UpdateProgressUseCase,
    GetProgressUseCase,
    AverageProgressUseCase
)
from infrastructure.repositories.progress_repository_impl import ProgressRepositoryImpl
from domain.exceptions import APIError

progress_bp = Blueprint('progress', __name__, url_prefix='/progress')

_create_schema   = ProgressCreateRequestSchema()
_update_schema   = ProgressUpdateRequestSchema()
_response_schema = ProgressResponseSchema()


@progress_bp.route('/', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Progresso'],
    'description': 'Registra progresso inicial para um curso para o usuário autenticado.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/ProgressCreateRequest'}
    }],
    'responses': {
        201: {
            'description': 'Progresso criado com sucesso',
            'schema': {'$ref': '#/definitions/ProgressResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def create_progress():
    try:
        data = _create_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    user_id = get_jwt_identity()
    use_case = CreateProgressUseCase(ProgressRepositoryImpl())
    try:
        progress = use_case.execute(user_id=user_id, course_id=data['course_id'])
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao criar progresso: %s", e)
        return jsonify({'message': 'Erro interno ao criar progresso'}), 500

    return jsonify(_response_schema.dump(progress)), 201


@progress_bp.route('/', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Progresso'],
    'description': 'Atualiza o progresso de um curso para o usuário autenticado.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/ProgressUpdateRequest'}
    }],
    'responses': {
        200: {
            'description': 'Progresso atualizado com sucesso',
            'schema': {'$ref': '#/definitions/ProgressResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        404: {'description': 'Progresso não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def update_progress():
    try:
        data = _update_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    user_id = get_jwt_identity()
    use_case = UpdateProgressUseCase(ProgressRepositoryImpl())
    try:
        progress = use_case.execute(
            user_id=user_id,
            course_id=data['course_id'],
            percentage=data['percentage']
        )
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao atualizar progresso: %s", e)
        return jsonify({'message': 'Erro interno ao atualizar progresso'}), 500

    return jsonify(_response_schema.dump(progress)), 200


@progress_bp.route('/<int:course_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Progresso'],
    'description': 'Retorna o progresso do usuário autenticado para o curso especificado.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'path',
        'name': 'course_id',
        'required': True,
        'schema': {'type': 'integer', 'example': 123},
        'description': 'ID do curso'
    }],
    'responses': {
        200: {
            'description': 'Progresso encontrado',
            'schema': {'$ref': '#/definitions/ProgressResponse'}
        },
        401: {'description': 'Token inválido ou ausente'},
        404: {'description': 'Progresso não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def get_progress(course_id: int):
    user_id = get_jwt_identity()
    use_case = GetProgressUseCase(ProgressRepositoryImpl())
    try:
        progress = use_case.execute(user_id=user_id, course_id=course_id)
        if progress is None:
            return jsonify({'message': 'Progresso não encontrado'}), 404
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao obter progresso: %s", e)
        return jsonify({'message': 'Erro interno ao obter progresso'}), 500

    return jsonify(_response_schema.dump(progress)), 200


@progress_bp.route('/average', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Progresso'],
    'description': 'Retorna a média de progresso de todos os cursos do usuário autenticado.',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Média de progresso retornada',
            'schema': {
                'type': 'object',
                'properties': {
                    'average_progress': {'type': 'number', 'format': 'float'}
                }
            }
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def average_progress():
    user_id = get_jwt_identity()
    use_case = AverageProgressUseCase(ProgressRepositoryImpl())
    try:
        avg = use_case.execute(user_id=user_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao calcular média de progresso: %s", e)
        return jsonify({'message': 'Erro interno ao calcular média de progresso'}), 500

    return jsonify({'average_progress': avg}), 200
