# app/schemas/forum_schema.py
from marshmallow import Schema, fields, validate, EXCLUDE

class ForumThreadRequestSchema(Schema):
    """
    Validação de criação de thread: apenas o título.
    """
    title = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=200),
        error_messages={
            'required': 'Título é obrigatório',
            'validator_failed': 'Título deve ter entre 3 e 200 caracteres'
        }
    )

    class Meta:
        unknown = EXCLUDE


class ForumPostRequestSchema(Schema):
    """
    Validação de criação de post: apenas o conteúdo.
    """
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=2000),
        error_messages={
            'required': 'Conteúdo é obrigatório',
            'validator_failed': 'Conteúdo não pode exceder 2000 caracteres'
        }
    )

    class Meta:
        unknown = EXCLUDE


class ForumThreadResponseSchema(Schema):
    """
    Serialização de thread: usado em respostas GET /threads.
    """
    id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format='iso')
    updated_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE


class ForumPostResponseSchema(Schema):
    """
    Serialização de post: usado em respostas GET /threads/<id>/posts.
    """
    id = fields.Int(dump_only=True)
    thread_id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    content = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE
