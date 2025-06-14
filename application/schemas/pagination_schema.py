# application/schemas/pagination_schema.py
from marshmallow import Schema, fields
from application.schemas.user_schema import UserResponseSchema

class PaginationSchema(Schema):
    items = fields.List(
        fields.Nested(UserResponseSchema),
        required=True
    )
    page  = fields.Int(required=True)
    pages = fields.Int(required=True)
    total = fields.Int(required=True)
