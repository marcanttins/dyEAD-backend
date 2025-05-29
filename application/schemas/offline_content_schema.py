# backend/application/schemas/offline_content_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE

class OfflineContentRequestSchema(Schema):
    """
    Validação de criação de conteúdo offline.
    """
    content_type = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={'required': 'content_type é obrigatório'}
    )
    content_url = fields.Url(
        required=True,
        error_messages={'required': 'content_url é obrigatório', 'invalid': 'URL inválida'}
    )

    class Meta:
        unknown = EXCLUDE

class OfflineContentResponseSchema(Schema):
    """
    Serialização de conteúdo offline.
    """
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    content_type = fields.Str(dump_only=True)
    content_url = fields.Url(dump_only=True)
    downloaded_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE