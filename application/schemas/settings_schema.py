# backend/application/schemas/settings_schema.py
from marshmallow import Schema, fields, EXCLUDE

class SettingsSchema(Schema):
    """
    Validação e serialização de preferências do usuário.
    """
    preferences = fields.Dict(
        keys=fields.Str(),
        values=fields.Raw(),
        required=True,
        error_messages={'required': 'preferences é obrigatório'}
    )
    updated_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE
