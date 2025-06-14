# backend/interface/http/controllers/upload_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from werkzeug.utils import secure_filename

from infrastructure.security.jwt import token_required, roles_required
from application.schemas.upload_schema import UploadRequestSchema
from application.schemas.material_schema import MaterialResponseSchema
from application.use_cases.upload_use_cases import UploadUseCase
from infrastructure.repositories.material_repository_impl import MaterialRepositoryImpl
from domain.exceptions import APIError

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

_req_schema  = UploadRequestSchema()
_resp_schema = MaterialResponseSchema()


@upload_bp.route('/', methods=['POST'])
@token_required
@roles_required('instrutor', 'admin')
@swag_from({
    'tags': ['Upload'],
    'description': 'Faz upload de um arquivo e cria um material associado a um curso.',
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Arquivo a ser enviado'
        },
        {
            'name': 'course_id',
            'in': 'formData',
            'type': 'integer',
            'required': True,
            'description': 'ID do curso'
        }
    ],
    'responses': {
        201: {
            'description': 'Arquivo enviado e material criado com sucesso',
            'schema': {'$ref': '#/definitions/MaterialResponse'}
        },
        400: {'description': 'Arquivo ou dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        403: {'description': 'Permissão insuficiente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def upload_file():
    # Verifica presença do arquivo
    if 'file' not in request.files:
        return jsonify({'message': 'Campo file é obrigatório'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    file.filename = filename  # assegura nome seguro

    # Valida outros campos (course_id etc.) no form-data
    try:
        data = _req_schema.load(request.form)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    use_case = UploadUseCase(MaterialRepositoryImpl())
    try:
        material = use_case.execute(
            course_id=data['course_id'],
            file_data=file
        )
    except APIError as e:
        current_app.logger.warning("UploadUseCase APIError: %s", e)
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro interno ao enviar arquivo: %s", e)
        return jsonify({'message': 'Erro interno ao enviar arquivo'}), 500

    return jsonify(_resp_schema.dump(material)), 201
