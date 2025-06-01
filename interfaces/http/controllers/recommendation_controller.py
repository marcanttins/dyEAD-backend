# backend/interface/http/controllers/recommendation_controller.py

from flasgger import swag_from
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError

from infrastructure.security.jwt import token_required
from application.schemas.recommendation_schema import (
    RecommendationRequestSchema,
    RecommendationResponseSchema
)
from application.use_cases.recommendation_use_cases import (
    CreateRecommendationUseCase,
    ListRecommendationsUseCase
)
from infrastructure.repositories.recommendation_repository_impl import RecommendationRepositoryImpl
from domain.exceptions import APIError

recommendation_bp = Blueprint('recommendations', __name__, url_prefix='/recommendations')

_req_schema       = RecommendationRequestSchema()
_resp_schema      = RecommendationResponseSchema()
_list_resp_schema = RecommendationResponseSchema(many=True)


@recommendation_bp.route('/', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Recomendações'],
    'description': 'Cria uma nova recomendação para o usuário autenticado.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'in': 'body',
        'name': 'body',
        'required': True,
        'schema': {'$ref': '#/definitions/RecommendationRequest'}
    }],
    'responses': {
        201: {
            'description': 'Recomendação criada com sucesso',
            'schema': {'$ref': '#/definitions/RecommendationResponse'}
        },
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def create_recommendation():
    try:
        data = _req_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Dados inválidos', 'errors': err.messages}), 400

    user_id = get_jwt_identity()
    use_case = CreateRecommendationUseCase(RecommendationRepositoryImpl())
    try:
        recommendation = use_case.execute(user_id, data['recommendation_text'])
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao criar recomendação: %s", e)
        return jsonify({'message': 'Erro interno ao criar recomendação'}), 500

    return jsonify(_resp_schema.dump(recommendation)), 201


@recommendation_bp.route('/', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Recomendações'],
    'description': 'Lista todas as recomendações do usuário autenticado.',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Lista de recomendações',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/RecommendationResponse'}
            }
        },
        401: {'description': 'Token inválido ou ausente'},
        500: {'description': 'Erro interno de servidor'}
    }
})
def list_recommendations():
    user_id = get_jwt_identity()
    use_case = ListRecommendationsUseCase(RecommendationRepositoryImpl())
    try:
        recommendations = use_case.execute(user_id)
    except APIError as e:
        return jsonify({'message': e.message}), e.status_code
    except Exception as e:
        current_app.logger.exception("Erro ao listar recomendações: %s", e)
        return jsonify({'message': 'Erro interno ao listar recomendações'}), 500

    return jsonify(_list_resp_schema.dump(recommendations)), 200
