# backend/application/schemas/progress_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE

class ProgressCreateRequestSchema(Schema):
    course_id = fields.Int(
        required=True,
        error_messages={'required': 'course_id é obrigatório'}
    )

    class Meta:
        unknown = EXCLUDE

class ProgressUpdateRequestSchema(Schema):
    course_id = fields.Int(
        required=True,
        error_messages={'required': 'course_id é obrigatório'}
    )
    percentage = fields.Float(
        required=True,
        validate=validate.Range(min=0, max=100),
        error_messages={
            'required': 'percentage é obrigatório',
            'validator_failed': 'percentage deve estar entre 0 e 100'
        }
    )

    class Meta:
        unknown = EXCLUDE

class ProgressResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    course_id = fields.Int(dump_only=True)
    percentage = fields.Float(dump_only=True)
    last_updated = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE