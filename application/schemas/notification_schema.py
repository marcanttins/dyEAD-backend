# backend/application/schemas/notification_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE

class NotificationRequestSchema(Schema):
    """
    Validação para criação de notificação.
    """
    user_id = fields.Int(
        required=True,
        error_messages={'required': 'user_id é obrigatório'}
    )
    message = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={'required': 'message é obrigatório', 'validator_failed': 'message inválida'}
    )

    class Meta:
        unknown = EXCLUDE

class NotificationResponseSchema(Schema):
    """
    Serialização de notificação.
    """
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    message = fields.Str(dump_only=True)
    read_status = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE
