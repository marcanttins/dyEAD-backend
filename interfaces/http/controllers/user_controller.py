from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError

from infrastructure.security.jwt import token_required, roles_required
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from application.schemas.user_schema import UserRequestSchema, UserResponseSchema
from application.schemas.pagination_schema import PaginationSchema
from domain.exceptions import APIError

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

# Schemas de validação e serialização
_user_req_schema = UserRequestSchema()
_user_resp_schema = UserResponseSchema()
_pagination_schema = PaginationSchema()

@user_bp.route('/', methods=['POST'])
@token_required
@roles_required('admin')
@swag_from({
    'tags': ['Usuários'],
    'description': 'Cria um novo usuário.',
    'parameters': [{
        'in': 'body', 'name': 'body', 'required': True,
        'schema': {'$ref': '#/definitions/UserRequest'}
    }],
    'responses': {
        '201': {'description': 'Usuário criado', 'schema': {'$ref': '#/definitions/UserResponse'}},
        '400': {'description': 'Dados inválidos'},
        '401': {'description': 'Não autenticado'},
        '403': {'description': 'Permissão insuficiente'},
        '500': {'description': 'Erro interno'}
    }
})
def create_user():
    try:
        data = _user_req_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({'message': 'Erro de validação', 'errors': err.messages}), 400

    # Gera hash da senha
    password = data.get('password')
    password_hash = generate_password_hash(password)

    repo = UserRepositoryImpl()
    try:
        user = repo.create(
            name=data.get('name'),
            email=data.get('email'),
            password_hash=password_hash,
            role=data.get('role', 'aluno')
        )
        return jsonify(_user_resp_schema.dump(user)), 201
    except APIError as e:
        current_app.logger.warning(f"APIError ao criar usuário: {e}")
        return jsonify({'message': e.message}), e.status_code
    except SQLAlchemyError as err:

        # import traceback
        # tb = traceback.format_exc()
        # current_app.logger.error(f"Traceback completo: {tb}")

        current_app.logger.exception(f"Erro interno ao criar usuário: {err}")
        return jsonify({'message': 'Erro interno ao criar usuário'}), 500

@user_bp.route('/', methods=['GET'])
@token_required
@roles_required('admin')
@swag_from({
    'tags': ['Usuários'],
    'description': 'Lista usuários com paginação.',
    'parameters': [
        {'in': 'query', 'name': 'page', 'type': 'integer', 'default': 1},
        {'in': 'query', 'name': 'per_page', 'type': 'integer', 'default': 10}
    ],
    'responses': {
        '200': {'description': 'Lista paginada', 'schema': {'$ref': '#/definitions/Pagination'}},
        '400': {'description': 'Parâmetros inválidos'},
        '401': {'description': 'Não autenticado'},
        '403': {'description': 'Permissão insuficiente'},
        '500': {'description': 'Erro interno'}
    }
})
def list_users():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
    except ValueError:
        return jsonify({'message': 'page e per_page devem ser inteiros'}), 400

    repo = UserRepositoryImpl()
    try:
        items, current_page, total_pages, total_items = repo.paginate(page, per_page)
    except APIError as e:
        current_app.logger.warning(f"APIError ao paginar usuários: {e}")
        return jsonify({'message': e.message}), e.status_code
    except SQLAlchemyError as err:
        current_app.logger.exception(f"Erro interno ao listar usuários: {err}")
        return jsonify({'message': 'Erro interno ao listar usuários'}), 500

    # Serializa usuários e paginação
    payload = {
        'items': items,
        'page': current_page,
        'pages': total_pages,
        'total': total_items
    }
    return jsonify(_pagination_schema.dump(payload)), 200

@user_bp.route('/<int:user_id>', methods=['GET'])
@token_required
@roles_required('admin')
@swag_from({
    'tags': ['Usuários'],
    'description': 'Obtém um usuário pelo ID.',
    'parameters': [{'in': 'path', 'name': 'user_id', 'type': 'integer', 'required': True}],
    'responses': {
        '200': {'description': 'Usuário retornado', 'schema': {'$ref': '#/definitions/UserResponse'}},
        '401': {'description': 'Não autenticado'},
        '403': {'description': 'Permissão insuficiente'},
        '404': {'description': 'Usuário não encontrado'},
        '500': {'description': 'Erro interno'}
    }
})
def get_user(user_id: int):
    repo = UserRepositoryImpl()
    try:
        user = repo.get_by_id(user_id)
    except SQLAlchemyError as err:
        current_app.logger.exception(f"Erro ao buscar usuário {user_id}: {err}")
        return jsonify({'message': 'Erro interno ao obter usuário'}), 500

    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    return jsonify(_user_resp_schema.dump(user)), 200

@user_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
@roles_required('admin')
@swag_from({
    'tags': ['Usuários'],
    'description': 'Atualiza um usuário existente.',
    'parameters': [
        {'in': 'path', 'name': 'user_id', 'type': 'integer', 'required': True},
        {'in': 'body', 'name': 'body', 'required': True, 'schema': {'$ref': '#/definitions/UserRequest'}}
    ],
    'responses': {
        '200': {'description': 'Usuário atualizado', 'schema': {'$ref': '#/definitions/UserResponse'}},
        '400': {'description': 'Dados inválidos'},
        '401': {'description': 'Não autenticado'},
        '403': {'description': 'Permissão insuficiente'},
        '404': {'description': 'Usuário não encontrado'},
        '500': {'description': 'Erro interno'}
    }
})
def update_user(user_id: int):
    try:
        data = _user_req_schema.load(request.get_json() or {}, partial=True)
    except ValidationError as err:
        return jsonify({'message': 'Erro de validação', 'errors': err.messages}), 400

    repo = UserRepositoryImpl()
    try:
        existing = repo.get_by_id(user_id)
        if not existing:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        updated = repo.update(existing, **data)
        return jsonify(_user_resp_schema.dump(updated)), 200
    except APIError as e:
        current_app.logger.warning(f"APIError ao atualizar usuário {user_id}: {e}")
        return jsonify({'message': e.message}), e.status_code
    except SQLAlchemyError as err:
        current_app.logger.exception(f"Erro interno ao atualizar usuário {user_id}: {err}")
        return jsonify({'message': 'Erro interno ao atualizar usuário'}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
@roles_required('admin')
@swag_from({
    'tags': ['Usuários'],
    'description': 'Exclui um usuário pelo ID.',
    'parameters': [{'in': 'path', 'name': 'user_id', 'type': 'integer', 'required': True}],
    'responses': {
        '204': {'description': 'Usuário excluído'},
        '401': {'description': 'Não autenticado'},
        '403': {'description': 'Permissão insuficiente'},
        '404': {'description': 'Usuário não encontrado'},
        '500': {'description': 'Erro interno'}
    }
})
def delete_user(user_id: int):
    repo = UserRepositoryImpl()
    try:
        existing = repo.get_by_id(user_id)
        if not existing:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        repo.delete(existing)
        return '', 204
    except APIError as e:
        current_app.logger.warning(f"APIError ao excluir usuário {user_id}: {e}")
        return jsonify({'message': e.message}), e.status_code
    except SQLAlchemyError as err:
        current_app.logger.exception(f"Erro interno ao excluir usuário {user_id}: {err}")
        return jsonify({'message': 'Erro interno ao excluir usuário'}), 500
