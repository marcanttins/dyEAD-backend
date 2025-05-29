# application/schemas/user_login_schema.py

from marshmallow import Schema, fields, EXCLUDE

class LoginRequestSchema(Schema):
    """
    Validação dos dados de login: email e senha.
    """
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'email é obrigatório',
            'invalid': 'email inválido'
        }
    )
    password = fields.Str(
        required=True,
        error_messages={'required': 'password é obrigatório'}
    )

    class Meta:
        unknown = EXCLUDE


class LoginResponseSchema(Schema):
    """
    Serialização da resposta de login, contendo usuário e tokens.
    """
    user = fields.Nested('UserResponseSchema', dump_only=True)
    access_token  = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)

    class Meta:
        unknown = EXCLUDE
