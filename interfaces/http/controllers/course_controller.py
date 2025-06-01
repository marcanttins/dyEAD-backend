# backend/interface/http/controllers/course_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError

from application.use_cases.course_use_cases import (
    CreateCourseUseCase,
    ListCoursesUseCase,
    ListFeaturedCoursesUseCase,
    GetCourseUseCase,
    UpdateCourseUseCase,
    DeleteCourseUseCase,
)
from infrastructure.repositories.course_repository_impl import CourseRepositoryImpl
from domain.exceptions import APIError
from infrastructure.security.jwt import token_required, roles_required
from application.schemas.course_schema import CourseRequestSchema, CourseResponseSchema

courses_bp = Blueprint('courses', __name__)
_request_schema = CourseRequestSchema()
_response_schema = CourseResponseSchema()
_list_schema = CourseResponseSchema(many=True)


@courses_bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Cursos'],
    'description': 'Cria um novo curso para o instrutor autenticado.',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/CourseRequest'}
    }],
    'responses': {
        201: {'description': 'Curso criado com sucesso', 'schema': {'$ref': '#/definitions/CourseResponse'}},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
@roles_required('instrutor', 'admin')
def create_course():
    try:
        data = _request_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    use_case = CreateCourseUseCase(CourseRepositoryImpl())
    course = use_case.execute(data, instructor_id=get_jwt_identity())
    return jsonify(_response_schema.dump(course)), 201


@courses_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Cursos'],
    'description': 'Lista todos os cursos disponíveis.',
    'responses': {
        200: {
            'description': 'Lista de cursos',
            'schema': {'type': 'array', 'items': {'$ref': '#/definitions/CourseResponse'}}
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
def list_courses():
    use_case = ListCoursesUseCase(CourseRepositoryImpl())
    courses = use_case.execute()
    return jsonify(_list_schema.dump(courses)), 200


@courses_bp.route('/featured', methods=['GET'])
@swag_from({
    'tags': ['Cursos'],
    'description': 'Lista cursos em destaque, limitado pelo parâmetro `limit`.',
    'parameters': [{
        'in': 'query',
        'name': 'limit',
        'type': 'integer',
        'required': False,
        'default': 5,
        'description': 'Número máximo de cursos em destaque'
    }],
    'responses': {
        200: {
            'description': 'Cursos em destaque',
            'schema': {'type': 'array', 'items': {'$ref': '#/definitions/CourseResponse'}}
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
def list_featured_courses():
    limit = request.args.get('limit', 5, type=int)
    use_case = ListFeaturedCoursesUseCase(CourseRepositoryImpl())
    courses = use_case.execute(limit)
    return jsonify(_list_schema.dump(courses)), 200


@courses_bp.route('/<int:course_id>', methods=['GET'])
@swag_from({
    'tags': ['Cursos'],
    'description': 'Obtém os detalhes de um curso pelo seu ID.',
    'parameters': [{
        'in': 'path',
        'name': 'course_id',
        'type': 'integer',
        'required': True,
        'description': 'ID do curso'
    }],
    'responses': {
        200: {'description': 'Dados do curso', 'schema': {'$ref': '#/definitions/CourseResponse'}},
        401: {'description': 'Token inválido ou ausente'},
        404: {'description': 'Curso não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
def get_course(course_id: int):
    use_case = GetCourseUseCase(CourseRepositoryImpl())
    try:
        course = use_case.execute(course_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    return jsonify(_response_schema.dump(course)), 200


@courses_bp.route('/<int:course_id>', methods=['PUT'])
@swag_from({
    'tags': ['Cursos'],
    'description': 'Atualiza os dados de um curso existente.',
    'parameters': [
        {
            'in': 'path',
            'name': 'course_id',
            'type': 'integer',
            'required': True,
            'description': 'ID do curso'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/CourseRequest'}
        }
    ],
    'responses': {
        200: {'description': 'Curso atualizado', 'schema': {'$ref': '#/definitions/CourseResponse'}},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        404: {'description': 'Curso não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
@roles_required('instrutor', 'admin')
def update_course(course_id: int):
    try:
        data = _request_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    use_case = UpdateCourseUseCase(CourseRepositoryImpl())
    try:
        course = use_case.execute(course_id, data)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    return jsonify(_response_schema.dump(course)), 200


@courses_bp.route('/<int:course_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Cursos'],
    'description': 'Remove um curso pelo seu ID.',
    'parameters': [{
        'in': 'path',
        'name': 'course_id',
        'type': 'integer',
        'required': True,
        'description': 'ID do curso'
    }],
    'responses': {
        204: {'description': 'Curso removido com sucesso'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        404: {'description': 'Curso não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
@token_required
@roles_required('instrutor', 'admin')
def delete_course(course_id: int):
    use_case = DeleteCourseUseCase(CourseRepositoryImpl())
    try:
        use_case.execute(course_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    return '', 204
