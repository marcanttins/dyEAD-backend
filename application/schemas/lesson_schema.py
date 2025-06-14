from marshmallow import Schema, fields, validate, EXCLUDE
from domain.entities.lesson import LessonType, LessonStatus

class LessonRequestSchema(Schema):
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
    type = fields.Str(
        required=True,
        validate=validate.OneOf([s.value for s in LessonType]),
        error_messages={'required': 'type é obrigatório', 'validator_failed': 'type inválido'}
    )
    status = fields.Str(
        validate=validate.OneOf([s.value for s in LessonStatus]),
        load_default=LessonStatus.DRAFT.value,
        error_messages={'validator_failed': 'status inválido'}
    )
    duration = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={'required': 'duration é obrigatório', 'validator_failed': 'duration inválido'}
    )
    video_url = fields.Str(
        load_default=None,
        validate=validate.URL(require_tld=True),
        error_messages={'validator_failed': 'video_url inválido'}
    )
    material_url = fields.Str(
        load_default=None,
        validate=validate.URL(require_tld=True),
        error_messages={'validator_failed': 'material_url inválido'}
    )
    questions = fields.List(
        fields.Dict(),
        load_default=[],
        error_messages={'validator_failed': 'questions inválido'}
    )

    class Meta:
        unknown = EXCLUDE

class LessonResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    description = fields.Str(dump_only=True)
    type = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    duration = fields.Int(dump_only=True)
    video_url = fields.Str(dump_only=True)
    material_url = fields.Str(dump_only=True)
    progress = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format='iso')
    updated_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE
