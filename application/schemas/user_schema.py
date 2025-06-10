# backend/application/schemas/user_schema.py

from marshmallow import Schema, fields, validate, EXCLUDE

class UserRequestSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'name é obrigatório', 'validator_failed': 'name inválido'}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': 'email é obrigatório', 'invalid': 'email inválido'}
    )
    password = fields.Str(
#        load_only=True,                    # usado apenas para ler no request
#        required=False,                    # talvez não seja obrigatório em edição
#        validate=validate.Length(min=6),    # mínimo de 6 caracteres, por exemplo
        required=True,
        error_messages={'required': 'password é obrigatório'}
    )
    role = fields.Str(
        validate=validate.OneOf(['aluno', 'instrutor', 'admin']),
        load_default='aluno',
        error_messages={'validator_failed': 'role inválido'}
    )

    class Meta:
        unknown = EXCLUDE


class UserResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    role = fields.Function(
        lambda obj: obj.role.value if hasattr(obj.role, 'value') else obj.role,
        dump_only=True
    )
    created_at = fields.DateTime(dump_only=True, format='iso')
    updated_at = fields.DateTime(dump_only=True, format='iso')

    class Meta:
        unknown = EXCLUDE
