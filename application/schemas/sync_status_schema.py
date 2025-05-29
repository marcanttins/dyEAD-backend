# backend/application/schemas/sync_status_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE

class SyncStatusRequestSchema(Schema):
    """
    Validação de criação/atualização de status de sincronização.
    """
    status = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'status é obrigatório', 'validator_failed': 'status inválido'}
    )

    class Meta:
        unknown = EXCLUDE

class SyncStatusResponseSchema(Schema):
    """
    Serialização de status de sincronização.
    """
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    status = fields.Str(dump_only=True)
    last_sync = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE