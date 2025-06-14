# backend/application/schemas/material_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE

class MaterialRequestSchema(Schema):
    """
    Validação para upload de material.
    """
    course_id = fields.Int(
        required=True,
        error_messages={'required': 'course_id é obrigatório'}
    )
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={'required': 'name é obrigatório'}
    )
    url = fields.Url(
        required=True,
        error_messages={'required': 'url é obrigatória', 'invalid': 'url inválida'}
    )
    material_type = fields.Str(
        required=True,
        validate=validate.OneOf(['video', 'pdf', 'link', 'file']),
        error_messages={'required': 'material_type é obrigatório', 'validator_failed': 'material_type inválido'}
    )

    class Meta:
        unknown = EXCLUDE


class MaterialResponseSchema(Schema):
    """
    Serialização de material.
    """
    id = fields.Int(dump_only=True)
    course_id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    url = fields.Url(dump_only=True)
    material_type = fields.Str(dump_only=True)
    uploaded_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE
