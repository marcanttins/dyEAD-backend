# backend/interface/http/controllers/forum_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from application.use_cases.forum_use_cases import (
    CreateThreadUseCase,
    ListThreadsUseCase,
    DeleteThreadUseCase,
    CreatePostUseCase,
    ListPostsUseCase
)
from infrastructure.repositories.forum_thread_repository_impl import ForumThreadRepositoryImpl
from infrastructure.repositories.forum_post_repository_impl import ForumPostRepositoryImpl
from domain.exceptions import APIError
from application.schemas.forum_schema import (
    ForumThreadRequestSchema,
    ForumThreadResponseSchema,
    ForumPostRequestSchema,
    ForumPostResponseSchema
)

forum_bp = Blueprint('forum', __name__)

_thread_req    = ForumThreadRequestSchema()
_thread_resp   = ForumThreadResponseSchema()
_threads_resp  = ForumThreadResponseSchema(many=True)
_post_req      = ForumPostRequestSchema()
_post_resp     = ForumPostResponseSchema()
_posts_resp    = ForumPostResponseSchema(many=True)


@forum_bp.route('/threads', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Fórum'],
    'description': 'Cria um novo tópico no fórum.',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/ForumThreadRequest'}
    }],
    'responses': {
        201: {
            'description': 'Tópico criado com sucesso',
            'schema': {'$ref': '#/definitions/ForumThreadResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def create_thread():
    try:
        data = _thread_req.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    user_id = get_jwt_identity()
    use_case = CreateThreadUseCase(ForumThreadRepositoryImpl())
    try:
        thread = use_case.execute(user_id=user_id, title=data['title'])
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao criar tópico: %s", e)
        return jsonify({'message': 'Erro interno ao criar tópico'}), 500

    return jsonify(_thread_resp.dump(thread)), 201


@forum_bp.route('/threads', methods=['GET'])
@swag_from({
    'tags': ['Fórum'],
    'description': 'Lista todos os tópicos do fórum.',
    'responses': {
        200: {
            'description': 'Lista de tópicos',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/ForumThreadResponse'}
            }
        },
        500: {'description': 'Erro interno de servidor'}
    }
})
def list_threads():
    use_case = ListThreadsUseCase(ForumThreadRepositoryImpl())
    try:
        threads = use_case.execute()
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao listar tópicos: %s", e)
        return jsonify({'message': 'Erro interno ao listar tópicos'}), 500

    return jsonify(_threads_resp.dump(threads)), 200


@forum_bp.route('/threads/<int:thread_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Fórum'],
    'description': 'Exclui um tópico pelo seu ID.',
    'parameters': [{
        'in': 'path',
        'name': 'thread_id',
        'type': 'integer',
        'required': True,
        'description': 'ID do tópico'
    }],
    'responses': {
        204: {'description': 'Tópico excluído com sucesso'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        404: {'description': 'Tópico não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def delete_thread(thread_id: int):
    use_case = DeleteThreadUseCase(ForumThreadRepositoryImpl())
    try:
        use_case.execute(thread_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao excluir tópico %s: %s", thread_id, e)
        return jsonify({'message': 'Erro interno ao excluir tópico'}), 500

    return '', 204


@forum_bp.route('/threads/<int:thread_id>/posts', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Fórum'],
    'description': 'Cria um novo post dentro de um tópico.',
    'parameters': [
        {
            'in': 'path',
            'name': 'thread_id',
            'type': 'integer',
            'required': True,
            'description': 'ID do tópico'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {'$ref': '#/definitions/ForumPostRequest'}
        }
    ],
    'responses': {
        201: {
            'description': 'Post criado com sucesso',
            'schema': {'$ref': '#/definitions/ForumPostResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        404: {'description': 'Tópico não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def create_post(thread_id: int):
    try:
        data = _post_req.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    use_case = CreatePostUseCase(ForumPostRepositoryImpl())
    try:
        post = use_case.execute(
            thread_id=thread_id,
            user_id=get_jwt_identity(),
            content=data['content']
        )
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao criar post no tópico %s: %s", thread_id, e)
        return jsonify({'message': 'Erro interno ao criar post'}), 500

    return jsonify(_post_resp.dump(post)), 201


@forum_bp.route('/threads/<int:thread_id>/posts', methods=['GET'])
@swag_from({
    'tags': ['Fórum'],
    'description': 'Lista todos os posts de um tópico.',
    'parameters': [{
        'in': 'path',
        'name': 'thread_id',
        'type': 'integer',
        'required': True,
        'description': 'ID do tópico'
    }],
    'responses': {
        200: {
            'description': 'Lista de posts',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/ForumPostResponse'}
            }
        },
        404: {'description': 'Tópico não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def list_posts(thread_id: int):
    use_case = ListPostsUseCase(ForumPostRepositoryImpl())
    try:
        posts = use_case.execute(thread_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao listar posts do tópico %s: %s", thread_id, e)
        return jsonify({'message': 'Erro interno ao listar posts'}), 500

    return jsonify(_posts_resp.dump(posts)), 200
