# backend/application/services/auth_service.py

from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash
from flask_mail import Message
from flask import current_app, url_for

from infrastructure.extensions import mail
from domain.repositories.user_repository import IUserRepository
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl


def _get_serializer() -> URLSafeTimedSerializer:
    """
    Cria um serializer a partir da SECRET_KEY do Flask,
    garantindo que seja chamado dentro do contexto de app.
    """
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


def send_forgot_password_email(email: str) -> None:
    """
    Envia email de recuperação de senha com link contendo token.
    Se o usuário não existir, falha silenciosamente.
    """
    user_repo: IUserRepository = UserRepositoryImpl()
    user = user_repo.get_by_email(email)
    if not user:
        return

    serializer = _get_serializer()
    token = serializer.dumps(user.email, salt='password-reset-salt')
    reset_url = url_for('auth.reset_password', token=token, _external=True)

    msg = Message(
        subject='Recuperação de senha',
        recipients=[user.email]
    )
    msg.body = (
        f'Olá {user.name},\n\n'
        f'Para redefinir sua senha, acesse:\n{reset_url}\n\n'
        'Este link expira em 1 hora.'
    )
    mail.send(msg)


def reset_user_password(token: str, new_password: str) -> None:
    """
    Valida o token de recuperação e atualiza a senha do usuário.
    Lança ValueError se o token for inválido, expirado ou o usuário não existir.
    """
    serializer = _get_serializer()
    try:
        email = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=3600
        )
    except SignatureExpired:
        raise ValueError('Token expirado')
    except BadSignature:
        raise ValueError('Token inválido')

    user_repo: IUserRepository = UserRepositoryImpl()
    user = user_repo.get_by_email(email)
    if not user:
        raise ValueError('Usuário não encontrado')

    user.password_hash = generate_password_hash(new_password)
    user_repo.update(user)
