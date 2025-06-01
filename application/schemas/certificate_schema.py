# application/schemas/certificate_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE

class CertificateRequestSchema(Schema):
    """
    Validação dos dados de criação de um certificado.
    """
    user_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={'required': 'user_id é obrigatório', 'invalid': 'user_id deve ser um inteiro válido'}
    )
    course_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={'required': 'course_id é obrigatório', 'invalid': 'course_id deve ser um inteiro válido'}
    )
    file_url = fields.Url(
        required=True,
        error_messages={'required': 'file_url é obrigatório', 'invalid': 'URL inválida'}
    )

    class Meta:
        unknown = EXCLUDE


class CertificateResponseSchema(Schema):
    """
    Serialização do certificado retornado pela API.
    """
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    course_id = fields.Int(dump_only=True)
    file_url = fields.Url(dump_only=True)
    issue_date = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE
