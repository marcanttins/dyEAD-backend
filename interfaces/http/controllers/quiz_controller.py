# backend/interface/http/controllers/quiz_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError

from infrastructure.security.jwt import token_required, roles_required
from application.schemas.quiz_schema import (
    QuizRequestSchema,
    QuizResponseSchema,
    QuizQuestionRequestSchema,
    QuizQuestionResponseSchema
)
from application.use_cases.quiz_use_cases import (
    CreateQuizUseCase,
    ListQuizQuestionsUseCase,
    SaveQuizQuestionsUseCase
)
from infrastructure.repositories.quiz_repository_impl import QuizRepositoryImpl
from infrastructure.repositories.quiz_question_repository_impl import QuizQuestionRepositoryImpl
from domain.exceptions import APIError

quiz_bp = Blueprint('quizzes', __name__, url_prefix='/quizzes')

_quiz_req_schema      = QuizRequestSchema()
_quiz_resp_schema     = QuizResponseSchema()
_question_req_schema  = QuizQuestionRequestSchema(many=True)
_question_resp_schema = QuizQuestionResponseSchema(many=True)


@quiz_bp.route('/', methods=['POST'])
@token_required
@roles_required('instrutor', 'admin')
@swag_from({
    'tags': ['Quizzes'],
    'description': 'Cria um novo quiz para um curso.',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/QuizRequest'}
    }],
    'responses': {
        201: {
            'description': 'Quiz criado com sucesso',
            'schema': {'$ref': '#/definitions/QuizResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def create_quiz():
    try:
        data = _quiz_req_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    use_case = CreateQuizUseCase(QuizRepositoryImpl())
    try:
        quiz = use_case.execute(
            course_id=data['course_id'],
            title=data['title']
        )
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao criar quiz: %s", e)
        return jsonify({'message': 'Erro interno ao criar quiz'}), 500

    return jsonify(_quiz_resp_schema.dump(quiz)), 201


@quiz_bp.route('/<int:quiz_id>/questions', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Quizzes'],
    'description': 'Lista todas as questões de um quiz.',
    'parameters': [{
        'in': 'path',
        'name': 'quiz_id',
        'type': 'integer',
        'required': True,
        'description': 'ID do quiz'
    }],
    'responses': {
        200: {
            'description': 'Lista de questões',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/QuizQuestionResponse'}
            }
        },
        401: {'description': 'Token inválido ou ausente'},
        404: {'description': 'Quiz não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def list_quiz_questions(quiz_id: int):
    use_case = ListQuizQuestionsUseCase(QuizQuestionRepositoryImpl())
    try:
        questions = use_case.execute(quiz_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao listar questões do quiz %s: %s", quiz_id, e)
        return jsonify({'message': 'Erro interno ao listar questões'}), 500

    return jsonify(_question_resp_schema.dump(questions)), 200


@quiz_bp.route('/<int:quiz_id>/questions', methods=['POST'])
@token_required
@roles_required('instrutor', 'admin')
@swag_from({
    'tags': ['Quizzes'],
    'description': 'Salva ou atualiza as questões de um quiz existente.',
    'parameters': [
        {
            'in': 'path',
            'name': 'quiz_id',
            'type': 'integer',
            'required': True,
            'description': 'ID do quiz'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/QuizQuestionRequest'}
        }
    ],
    'responses': {
        204: {'description': 'Questões salvas com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        404: {'description': 'Quiz não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def save_quiz_questions(quiz_id: int):
    try:
        questions_data = _question_req_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    use_case = SaveQuizQuestionsUseCase(QuizQuestionRepositoryImpl())
    try:
        use_case.execute(quiz_id, questions_data)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao salvar questões do quiz %s: %s", quiz_id, e)
        return jsonify({'message': 'Erro interno ao salvar questões'}), 500

    return '', 204
