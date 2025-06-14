# backend/application/schemas/summary_schema.py
from marshmallow import Schema, fields, EXCLUDE

class SummarySchema(Schema):
    """
    Serialização do resumo de métricas da plataforma.
    """
    total_users = fields.Int(dump_only=True)
    total_courses = fields.Int(dump_only=True)
    average_progress_global = fields.Float(dump_only=True)

    class Meta:
        unknown = EXCLUDE
