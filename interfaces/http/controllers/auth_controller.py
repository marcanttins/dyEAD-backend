# backend/interface/http/controllers/auth_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, make_response, current_app
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.repositories.token_repository_impl import TokenRepositoryImpl
from infrastructure.repositories.revoked_token_repository_impl import RevokedTokenRepositoryImpl
from application.use_cases.authenticate_user_use_case import AuthenticateUserUseCase
from application.use_cases.refresh_token_use_case import RefreshTokenUseCase
from application.use_cases.revoked_token_use_case import RevokedTokenUseCase
from application.dtos.auth_dto import AuthTokensDTO
from infrastructure.config import config_by_name
from application.schemas.user_login_schema import LoginRequestSchema, LoginResponseSchema
from application.schemas.user_schema import UserRequestSchema, UserResponseSchema
from application.services.auth_service import send_forgot_password_email, reset_user_password
from domain.exceptions import APIError

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

_login_req_schema  = LoginRequestSchema()
_login_resp_schema = LoginResponseSchema()
_user_req_schema   = UserRequestSchema()
_user_resp_schema  = UserResponseSchema()


@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'description': 'Registra um novo usuário (aluno por padrão).',
    'parameters': [{
        'in': 'body', 'name': 'body', 'required': True,
        'schema': {'$ref': '#/definitions/UserRequest'}
    }],
    'responses': {
        '201': {'description': 'Usuário criado com sucesso', 'schema': {'$ref': '#/definitions/UserResponse'}},
        '400': {'description': 'Dados inválidos ou email já cadastrado'},
        '500': {'description': 'Erro interno ao criar usuário'}
    }
})
def register():
    try:
        data = _user_req_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'message': 'Erro de validação', 'errors': err.messages}), 400

    repo = UserRepositoryImpl()
    if repo.get_by_email(data['email']):
        return jsonify({'message': 'Email já cadastrado'}), 400

    try:
        hashed = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = repo.create(
            name          = data['name'],
            email         = data['email'],
            password_hash = hashed,
            role          = data.get('role', 'aluno')
        )
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'data': _user_resp_schema.dump(new_user)
        }), 201

    except APIError as e:
        current_app.logger.warning(f"APIError ao criar usuário: {e}")
        return jsonify({'message': e.message}), e.status_code

    except SQLAlchemyError as err:
        current_app.logger.exception(f"Erro de banco ao criar usuário: {err}")
        return jsonify({'message': 'Erro interno ao criar usuário'}), 500


@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'description': 'Realiza login com email e senha, emitindo access e refresh tokens.',
    'parameters': [{
        'in': 'body', 'name': 'body', 'required': True,
        'schema': {'$ref': '#/definitions/UserLoginRequest'}
    }],
    'responses': {
        '200': {'description': 'Login bem-sucedido', 'schema': {'$ref': '#/definitions/UserLoginResponse'}},
        '400': {'description': 'Erro de validação'},
        '401': {'description': 'Credenciais inválidas'},
        '500': {'description': 'Erro interno ao processar login'}
    }
})
def login():
    # 1) Valida payload
    try:
        data = _login_req_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'message': 'Erro de validação', 'errors': err.messages}), 400

    # 2) Seleciona configuração por ambiente
    env_key = current_app.config.get('ENV', 'development').lower()
    cfg     = config_by_name.get(env_key, config_by_name['development'])

    repo = UserRepositoryImpl()
    auth_uc = AuthenticateUserUseCase(
        user_repo       = repo,
        access_expires  = cfg.JWT_ACCESS_TOKEN_EXPIRES,
        refresh_expires = cfg.JWT_REFRESH_TOKEN_EXPIRES
    )

    # 3) Executa a autenticação
    try:
        tokens: AuthTokensDTO = auth_uc.execute(
            email    = data['email'],
            password = data['password']
        )
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as err:
        # import traceback
        # tb = traceback.format_exc()
        # current_app.logger.error(f"Traceback completo: {tb}")
        current_app.logger.exception(f"Erro interno no AuthenticateUserUseCase: {err}")
        return jsonify({'message': 'Erro interno ao processar login'}), 500

    # 4) Recupera usuário para resposta
    try:
        user = repo.get_by_email(data['email'])
    except SQLAlchemyError as err:
        current_app.logger.exception(f"Erro ao buscar usuário pós-login: {err}")
        user = None

    # 5) Monta objeto cru e serializa via Marshmallow
    response_obj = {
        'user'          : user,
        'access_token'  : tokens.access_token,
        'refresh_token' : tokens.refresh_token
    }
    result = _login_resp_schema.dump(response_obj)

    # 6) Retorna com cookie HTTP-only do refresh token
    resp = make_response(jsonify(result), 200)
    resp.set_cookie(
        'refresh_token',
        tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=int(cfg.JWT_REFRESH_TOKEN_EXPIRES.total_seconds())
    )
    return resp


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@swag_from({
    'tags': ['Autenticação'],
    'description': 'Renova access token usando refresh token em cookie.',
    'security': [{'Bearer': []}],
    'responses': {
        '200': {'description': 'Novo access token gerado', 'schema': {'type': 'object', 'properties': {'access_token': {'type': 'string'}}}},
        '401': {'description': 'Refresh token inválido ou ausente'},
        '500': {'description': 'Erro interno ao renovar token'}
    }
})
def refresh():
    old_jti = get_jwt().get('jti')
    # revoga o refresh token antigo
    RevokedTokenUseCase(RevokedTokenRepositoryImpl()).execute(
        jti        = old_jti,
        ip_address = request.remote_addr,
        user_agent = request.headers.get('User-Agent'),
        device_id  = request.headers.get('X-Device-Id')
    )

    env_key = current_app.config.get('ENV', 'development').lower()
    cfg     = config_by_name.get(env_key, config_by_name['development'])

    refresh_uc = RefreshTokenUseCase(
        token_repo     = TokenRepositoryImpl(),
        access_expires = cfg.JWT_ACCESS_TOKEN_EXPIRES
    )

    try:
        tokens = refresh_uc.execute(old_jti)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as err:
        current_app.logger.exception(f"Erro interno no RefreshTokenUseCase: {err}")
        return jsonify({'message': 'Erro interno ao renovar token'}), 500

    resp = make_response(jsonify({'access_token': tokens.access_token}), 200)
    resp.set_cookie(
        'refresh_token',
        tokens.refresh_token,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=int(cfg.JWT_REFRESH_TOKEN_EXPIRES.total_seconds())
    )
    return resp


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Autenticação'],
    'description': 'Revoga o access token atual e limpa cookie.',
    'security': [{'Bearer': []}],
    'responses': {
        '200': {'description': 'Logout realizado com sucesso'},
        '401': {'description': 'Access token inválido ou ausente'}
    }
})
def logout():
    jti = get_jwt().get('jti')
    RevokedTokenUseCase(RevokedTokenRepositoryImpl()).execute(
        jti        = jti,
        ip_address = request.remote_addr,
        user_agent = request.headers.get('User-Agent'),
        device_id  = request.headers.get('X-Device-Id')
    )
    resp = make_response(jsonify({'message': 'Logout realizado com sucesso'}), 200)
    resp.delete_cookie('refresh_token')
    return resp


@auth_bp.route('/logout/refresh', methods=['DELETE'])
@jwt_required(refresh=True)
@swag_from({
    'tags': ['Autenticação'],
    'description': 'Revoga o refresh token atual e limpa cookie.',
    'security': [{'Bearer': []}],
    'responses': {
        '200': {'description': 'Refresh token revogado com sucesso'},
        '401': {'description': 'Refresh token inválido ou ausente'}
    }
})
def logout_refresh():
    jti = get_jwt().get('jti')
    RevokedTokenUseCase(RevokedTokenRepositoryImpl()).execute(
        jti        = jti,
        ip_address = request.remote_addr,
        user_agent = request.headers.get('User-Agent'),
        device_id  = request.headers.get('X-Device-Id')
    )
    resp = make_response(jsonify({'message': 'Logout refresh realizado'}), 200)
    resp.delete_cookie('refresh_token')
    return resp


@auth_bp.route('/forgot-password', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'description': 'Inicia fluxo de recuperação de senha via email.',
    'parameters': [{
        'in': 'body', 'name': 'body', 'required': True,
        'schema': {'$ref': '#/definitions/ForgotPasswordRequest'}
    }],
    'responses': {
        '200': {'description': 'Link de recuperação enviado'},
        '400': {'description': 'Email não informado'},
        '500': {'description': 'Erro interno ao enviar link'}
    }
})
def forgot_password():
    data  = request.get_json() or {}
    email = data.get('email')
    if not email:
        return jsonify({'message': 'Email é obrigatório'}), 400

    try:
        send_forgot_password_email(email)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as err:
        current_app.logger.exception(f"Erro ao enviar link de recuperação: {err}")
        return jsonify({'message': 'Erro interno ao enviar link'}), 500

    return jsonify({'message': 'Se o email existir, link será enviado'}), 200


@auth_bp.route('/reset-password', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'description': 'Redefine a senha usando token de recuperação.',
    'parameters': [{
        'in': 'body', 'name': 'body', 'required': True,
        'schema': {'$ref': '#/definitions/ResetPasswordRequest'}
    }],
    'responses': {
        '200': {'description': 'Senha redefinida com sucesso'},
        '400': {'description': 'Token ou senha inválido'},
        '500': {'description': 'Erro interno ao redefinir senha'}
    }
})
def reset_password():
    data         = request.get_json() or {}
    token        = data.get('token')
    new_password = data.get('password')
    if not token or not new_password:
        return jsonify({'message': 'Token e nova senha obrigatórios'}), 400

    try:
        reset_user_password(token, new_password)
        return jsonify({'message': 'Senha redefinida com sucesso'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as err:
        current_app.logger.exception(f"Erro ao redefinir senha: {err}")
        return jsonify({'message': 'Erro interno ao redefinir senha'}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Autenticação'],
    'description': 'Retorna perfil do usuário autenticado.',
    'security': [{'Bearer': []}],
    'responses': {
        '200': {'description': 'Perfil obtido com sucesso', 'schema': {'$ref': '#/definitions/UserResponse'}},
        '401': {'description': 'Access token inválido ou ausente'},
        '404': {'description': 'Usuário não encontrado'},
        '500': {'description': 'Erro interno ao obter perfil'}
    }
})
def get_profile():
    user_id = get_jwt_identity()
    try:
        user = UserRepositoryImpl().get_by_id(user_id)
    except SQLAlchemyError as err:
        current_app.logger.exception(f"Erro ao buscar perfil: {err}")
        return jsonify({'message': 'Erro interno ao obter perfil'}), 500

    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    return jsonify({
        'message': 'Perfil encontrado',
        'data': _user_resp_schema.dump(user)
    }), 200
