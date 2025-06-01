# backend/application/schemas/reports_schema.py
from marshmallow import Schema, fields, EXCLUDE

class UserCountReportSchema(Schema):
    """
    Serialização para relatório de total de usuários.
    """
    total_users = fields.Int(dump_only=True)

    class Meta:
        unknown = EXCLUDE
