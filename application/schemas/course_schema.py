# application/schemas/course_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE
from domain.entities.course import CourseStatus

class CourseRequestSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={'required': 'title é obrigatório', 'validator_failed': 'title inválido'}
    )
    description = fields.Str(
        load_default=None,
        validate=validate.Length(max=1000),
        error_messages={'validator_failed': 'description inválida'}
    )
    category = fields.Str(
        load_default=None,
        validate=validate.Length(max=100),
        error_messages={'validator_failed': 'category inválida'}
    )
    status = fields.Str(
        validate=validate.OneOf([s.value for s in CourseStatus]),
        load_default=CourseStatus.DRAFT.value,
        error_messages={'validator_failed': 'status inválido'}
    )
    instructor_id = fields.Int(
        required=True,
        error_messages={'required': 'instructor_id é obrigatório'}
    )

    class Meta:
        unknown = EXCLUDE

class CourseResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    category = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    instructor_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format='iso')
    updated_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE
