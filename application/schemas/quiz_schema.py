# backend/application/schemas/quiz_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE

class QuizRequestSchema(Schema):
    course_id = fields.Int(
        required=True,
        error_messages={'required': 'course_id é obrigatório'}
    )
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={'required': 'title é obrigatório'}
    )

    class Meta:
        unknown = EXCLUDE

class QuizResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    course_id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE

class QuizQuestionRequestSchema(Schema):
    text = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=500),
        error_messages={'required': 'text é obrigatório'}
    )
    options = fields.List(
        fields.Str(validate=validate.Length(min=1, max=255)),
        required=True,
        validate=validate.Length(min=2),
        error_messages={'required': 'options é obrigatório', 'validator_failed': 'options inválidas'}
    )
    correct_option = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        error_messages={'required': 'correct_option é obrigatório'}
    )

    class Meta:
        unknown = EXCLUDE

class QuizQuestionResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    quiz_id = fields.Int(dump_only=True)
    text = fields.Str(dump_only=True)
    options = fields.List(fields.Str(), dump_only=True)
    correct_option = fields.Int(dump_only=True)

    class Meta:
        unknown = EXCLUDE