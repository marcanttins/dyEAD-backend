# application/schemas/feedback_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE

class FeedbackRequestSchema(Schema):
    """
    Validação de feedback para criação de um novo registro.
    """
    course_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={
            'required': 'course_id é obrigatório',
            'invalid': 'course_id inválido'
        }
    )
    message = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=2000),
        error_messages={
            'required': 'message é obrigatório',
            'validator_failed': 'message deve ter entre 1 e 2000 caracteres'
        }
    )

    class Meta:
        unknown = EXCLUDE

class FeedbackResponseSchema(Schema):
    """
    Serialização do feedback criado/listado.
    """
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    course_id = fields.Int(dump_only=True)
    message = fields.Str(dump_only=True)
    sentiment = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE
