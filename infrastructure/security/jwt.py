# backend/infrastructure/security/jwt.py

from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt
from flask_jwt_extended.exceptions import JWTExtendedException
from sqlalchemy.exc import SQLAlchemyError

from domain.exceptions import APIError
from domain.repositories.revoked_token_repository import IRevokedTokenRepository
from infrastructure.repositories.revoked_token_repository_impl import RevokedTokenRepositoryImpl
from infrastructure.extensions import db
from infrastructure.orm.models import User as UserModel

jwt = JWTManager()
token_repo: IRevokedTokenRepository = RevokedTokenRepositoryImpl()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(_jwt_header, jwt_payload):
    return token_repo.is_revoked(jwt_payload.get('jti'))


@jwt.revoked_token_loader
def revoked_token_callback(_jwt_header, _jwt_payload):
    return jsonify({"msg": "Token revogado"}), 401


@jwt.expired_token_loader
def expired_token_callback(_jwt_header, _jwt_payload):
    return jsonify({"msg": "Token expirado"}), 401


@jwt.user_identity_loader
def user_identity_lookup(identity) -> str:
    # Armazena o ID no token (string)
    return str(identity.id) if hasattr(identity, 'id') else str(identity)


@jwt.additional_claims_loader
def add_user_claims(identity) -> dict:
    """
    Insere o papel do usuário ('role') como claim extra no token.
    """
    if hasattr(identity, 'role'):
        role_raw = identity.role
    else:
        try:
            user_obj = db.session.get(UserModel, int(identity))
            role_raw = user_obj.role if user_obj else None
        except (ValueError, SQLAlchemyError) as err:
            current_app.logger.error(f"Erro carregando role para claims: {err}")
            role_raw = None

    role = getattr(role_raw, 'value', role_raw)
    return {'role': str(role) if role is not None else None}


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except JWTExtendedException:
            raise APIError("Token inválido ou ausente", status_code=401)
        return fn(*args, **kwargs)
    return wrapper


def roles_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except JWTExtendedException:
                raise APIError("Token inválido ou ausente", status_code=401)

            claims = get_jwt()
            if claims.get('role') not in allowed_roles:
                raise APIError("Permissão insuficiente", status_code=403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def revoke_token(jti: str):
    """
    Revoga o JWT atual, salvando jti e metadados de IP, User-Agent e device_id.
    """
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    device_id  = request.headers.get('X-Device-Id')
    token_repo.add(
        jti=jti,
        ip_address=ip_address,
        user_agent=user_agent,
        device_id=device_id
    )
