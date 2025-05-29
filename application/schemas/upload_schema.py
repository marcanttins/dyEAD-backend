# backend/application/schemas/upload_schema.py
from marshmallow import Schema, fields, EXCLUDE

class UploadRequestSchema(Schema):
    """
    Validação do form-data para upload de arquivo.
    Espera um campo 'course_id' em form-data junto com o arquivo.
    """
    course_id = fields.Int(
        required=True,
        error_messages={'required': 'course_id é obrigatório'}
    )

    class Meta:
        unknown = EXCLUDE