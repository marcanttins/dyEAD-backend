# application/schemas/revoked_token_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE

class RevokedTokenRequestSchema(Schema):
    """
    Validação para revogação de token.
    """
    jti = fields.Str(
        required=True,
        validate=validate.Length(equal=36),  # UUID4 length
        error_messages={
            'required': 'jti é obrigatório',
            'invalid': 'jti deve ser uma string válida',
            'validator_failed': 'jti deve ter 36 caracteres UUID4'
        }
    )

    class Meta:
        unknown = EXCLUDE

class RevokedTokenResponseSchema(Schema):
    """
    Serialização de token revogado.
    """
    id = fields.Int(dump_only=True)
    jti = fields.Str(dump_only=True)
    revoked_at = fields.DateTime(dump_only=True, format='iso')
    ip_address = fields.Str(dump_only=True)
    user_agent = fields.Str(dump_only=True)

    class Meta:
        unknown = EXCLUDE
