# backend/application/schemas/recommendation_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE

class RecommendationRequestSchema(Schema):
    """
    Validação para envio de recomendação.
    """
    recommendation_text = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=2000),
        error_messages={
            'required': 'recommendation_text é obrigatório',
            'validator_failed': 'recommendation_text inválido'
        }
    )

    class Meta:
        unknown = EXCLUDE

class RecommendationResponseSchema(Schema):
    """
    Serialização de recomendação.
    """
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    recommendation_text = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format='iso')
    updated_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE