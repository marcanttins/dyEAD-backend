from flasgger import swag_from
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError

from application.use_cases.lesson_use_cases import (
    CreateLessonUseCase,
    GetLessonUseCase,
    UpdateLessonUseCase,
    DeleteLessonUseCase,
    ListLessonsUseCase,
)
from infrastructure.repositories.lesson_repository_impl import LessonRepositoryImpl
from domain.exceptions import APIError
from infrastructure.security.jwt import token_required, roles_required
from application.schemas.lesson_schema import LessonRequestSchema, LessonResponseSchema

lessons_bp = Blueprint('lessons', __name__)
_request_schema = LessonRequestSchema()
_response_schema = LessonResponseSchema()
_list_schema = LessonResponseSchema(many=True)

@lessons_bp.route('/<int:course_id>/lessons', methods=['POST'])
@swag_from({
    'tags': ['Aulas'],
    'description': 'Cria uma nova aula para um curso específico.',
    'parameters': [
        {
            'in': 'path',
            'name': 'course_id',
            'required': True,
            'type': 'integer'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/LessonRequest'}
        }
    ],
    'responses': {
        201: {'description': 'Aula criada com sucesso', 'schema': {'$ref': '#/definitions/LessonResponse'}},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
@roles_required('instrutor', 'admin')
def create_lesson(course_id):
    try:
        data = _request_schema.load(request.json)
        use_case = CreateLessonUseCase(LessonRepositoryImpl())
        lesson = use_case.execute(course_id, data)
        return _response_schema.dump(lesson), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except APIError as err:
        return jsonify({'error': str(err)}), err.status_code

@lessons_bp.route('/<int:course_id>/lessons', methods=['GET'])
@swag_from({
    'tags': ['Aulas'],
    'description': 'Lista todas as aulas de um curso específico.',
    'parameters': [
        {
            'in': 'path',
            'name': 'course_id',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        200: {'description': 'Lista de aulas', 'schema': {'$ref': '#/definitions/LessonResponse'}},
        401: {'description': 'Token inválido ou ausente'},
        404: {'description': 'Curso não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
def list_lessons(course_id):
    try:
        use_case = ListLessonsUseCase(LessonRepositoryImpl())
        lessons = use_case.execute(course_id)
        return _list_schema.dump(lessons)
    except APIError as err:
        return jsonify({'error': str(err)}), err.status_code

@lessons_bp.route('/lessons/<int:lesson_id>', methods=['GET'])
@swag_from({
    'tags': ['Aulas'],
    'description': 'Obtém detalhes de uma aula específica.',
    'parameters': [
        {
            'in': 'path',
            'name': 'lesson_id',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        200: {'description': 'Detalhes da aula', 'schema': {'$ref': '#/definitions/LessonResponse'}},
        401: {'description': 'Token inválido ou ausente'},
        404: {'description': 'Aula não encontrada'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
def get_lesson(lesson_id):
    try:
        use_case = GetLessonUseCase(LessonRepositoryImpl())
        lesson = use_case.execute(lesson_id)
        return _response_schema.dump(lesson)
    except APIError as err:
        return jsonify({'error': str(err)}), err.status_code

@lessons_bp.route('/lessons/<int:lesson_id>', methods=['PUT'])
@swag_from({
    'tags': ['Aulas'],
    'description': 'Atualiza uma aula específica.',
    'parameters': [
        {
            'in': 'path',
            'name': 'lesson_id',
            'required': True,
            'type': 'integer'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/LessonRequest'}
        }
    ],
    'responses': {
        200: {'description': 'Aula atualizada com sucesso', 'schema': {'$ref': '#/definitions/LessonResponse'}},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        404: {'description': 'Aula não encontrada'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
@roles_required('instrutor', 'admin')
def update_lesson(lesson_id):
    try:
        data = _request_schema.load(request.json)
        use_case = UpdateLessonUseCase(LessonRepositoryImpl())
        lesson = use_case.execute(lesson_id, data)
        return _response_schema.dump(lesson)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except APIError as err:
        return jsonify({'error': str(err)}), err.status_code

@lessons_bp.route('/lessons/<int:lesson_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Aulas'],
    'description': 'Exclui uma aula específica.',
    'parameters': [
        {
            'in': 'path',
            'name': 'lesson_id',
            'required': True,
            'type': 'integer'
        }
    ],
    'responses': {
        204: {'description': 'Aula excluída com sucesso'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        404: {'description': 'Aula não encontrada'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
@roles_required('instrutor', 'admin')
def delete_lesson(lesson_id):
    try:
        use_case = DeleteLessonUseCase(LessonRepositoryImpl())
        use_case.execute(lesson_id)
        return '', 204
    except APIError as err:
        return jsonify({'error': str(err)}), err.status_code
