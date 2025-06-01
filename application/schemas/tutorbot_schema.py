# backend/application/schemas/tutorbot_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE


class TutorBotRequestSchema(Schema):
    """
    Validação de prompt enviado ao TutorBot.
    """
    prompt = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={'required': 'prompt é obrigatório'}
    )

    class Meta:
        unknown = EXCLUDE


class TutorBotResponseSchema(Schema):
    """
    Serialização de interação com o TutorBot.
    """
    id = fields.Int(dump_only=True)
    request_text = fields.Str(dump_only=True)
    response_text = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE