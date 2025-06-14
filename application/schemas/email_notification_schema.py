from marshmallow import Schema, fields, validate, EXCLUDE

class EmailNotificationRequestSchema(Schema):
    subject = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255),
        error_messages={'required': 'subject é obrigatório', 'validator_failed': 'subject inválido'}
    )
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=10000),
        error_messages={'required': 'content é obrigatório', 'validator_failed': 'content inválido'}
    )
    recipients = fields.List(
        fields.Str(validate=validate.Email()),
        required=True,
        validate=validate.Length(min=1),
        error_messages={'required': 'recipients é obrigatório', 'validator_failed': 'recipients inválido'}
    )
    template_type = fields.Str(
        required=True,
        validate=validate.OneOf(['new_request', 'approval', 'rejection', 'status_change']),
        error_messages={'required': 'template_type é obrigatório', 'validator_failed': 'template_type inválido'}
    )

    class Meta:
        unknown = EXCLUDE

class EmailNotificationResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    subject = fields.Str(dump_only=True)
    content = fields.Str(dump_only=True)
    template_type = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format='iso')
    updated_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE
