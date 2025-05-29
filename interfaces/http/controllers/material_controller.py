# backend/interface/http/controllers/material_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from infrastructure.security.jwt import token_required, roles_required
from marshmallow import ValidationError

from application.schemas.material_schema import MaterialRequestSchema, MaterialResponseSchema
from application.use_cases.material_use_cases import (
    UploadMaterialUseCase,
    GetMaterialsUseCase,
    DeleteMaterialUseCase
)
from infrastructure.repositories.material_repository_impl import MaterialRepositoryImpl
from domain.exceptions import APIError

material_bp = Blueprint('materials', __name__, url_prefix='/materials')

_req_schema       = MaterialRequestSchema()
_resp_schema      = MaterialResponseSchema()
_list_resp_schema = MaterialResponseSchema(many=True)


@material_bp.route('/', methods=['POST'])
@token_required
@roles_required('instrutor', 'admin')
@swag_from({
    'tags': ['Material'],
    'description': 'Envia um novo material para um curso.',
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/MaterialRequest'}
    }],
    'responses': {
        201: {
            'description': 'Material enviado com sucesso',
            'schema': {'$ref': '#/definitions/MaterialResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def upload_material():
    try:
        data = _req_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Erro de validação', 'errors': err.messages}), 400

    use_case = UploadMaterialUseCase(MaterialRepositoryImpl())
    try:
        material = use_case.execute(
            course_id     = data['course_id'],
            name          = data['name'],
            url           = data['url'],
            material_type = data['material_type']
        )
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao enviar material: %s", e)
        return jsonify({'message': 'Erro interno ao enviar material'}), 500

    return jsonify(_resp_schema.dump(material)), 201


@material_bp.route('/course/<int:course_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Material'],
    'description': 'Lista todos os materiais de um curso.',
    'parameters': [{
        'in': 'path',
        'name': 'course_id',
        'required': True,
        'schema': {'type': 'integer', 'example': 123}
    }],
    'responses': {
        200: {
            'description': 'Lista de materiais',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/MaterialResponse'}
            }
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def list_materials(course_id: int):
    use_case = GetMaterialsUseCase(MaterialRepositoryImpl())
    try:
        materials = use_case.execute(course_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao listar materiais do curso %s: %s", course_id, e)
        return jsonify({'message': 'Erro interno ao listar materiais'}), 500

    return jsonify(_list_resp_schema.dump(materials)), 200


@material_bp.route('/<int:material_id>', methods=['DELETE'])
@token_required
@roles_required('instrutor', 'admin')
@swag_from({
    'tags': ['Material'],
    'description': 'Remove um material pelo seu ID.',
    'parameters': [{
        'in': 'path',
        'name': 'material_id',
        'required': True,
        'schema': {'type': 'integer', 'example': 456}
    }],
    'responses': {
        204: {'description': 'Material excluído com sucesso'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        404: {'description': 'Material não encontrado'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def delete_material(material_id: int):
    use_case = DeleteMaterialUseCase(MaterialRepositoryImpl())
    try:
        use_case.execute(material_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao excluir material %s: %s", material_id, e)
        return jsonify({'message': 'Erro interno ao excluir material'}), 500

    return '', 204
