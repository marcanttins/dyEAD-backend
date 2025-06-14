# backend/interface/http/error_handlers.py

from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
from domain.exceptions import APIError

def register_error_handlers(app):
    """
    Registra handlers globais de erro na aplicação Flask.
    Captura tanto exceções de negócio (APIError) quanto erros HTTP e
    exceções não tratadas, retornando JSON consistente.
    """
    @app.errorhandler(APIError)
    def handle_api_error(error: APIError):
        payload = {"message": error.message}
        if error.errors:
            payload["errors"] = error.errors
        return jsonify(payload), error.status_code

    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({
            "message": "Requisição inválida",
            "error": str(e)
        }), 400

    @app.errorhandler(401)
    def handle_unauthorized(e):
        return jsonify({
            "message": "Não autorizado",
            "error": str(e)
        }), 401

    @app.errorhandler(403)
    def handle_forbidden(e):
        return jsonify({
            "message": "Acesso negado",
            "error": str(e)
        }), 403

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            "message": "Recurso não encontrado",
            "error": str(e)
        }), 404

    @app.errorhandler(Exception)
    def handle_uncaught_exception(e):
        # Erros HTTP padrão são repassados com sua descrição e código
        if isinstance(e, HTTPException):
            return jsonify({"message": e.description}), e.code

        # Qualquer outra exceção é registrada e retorna 500
        current_app.logger.error(f"Erro interno não tratado: {e}", exc_info=True)
        return jsonify({
            "message": "Erro interno do servidor",
            "error": str(e)
        }), 500
