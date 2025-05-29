# backend/domain/exceptions.py

class APIError(Exception):
    """
    Exceção genérica para erros de aplicação que podem ser capturados pelos handlers HTTP.
    """
    def __init__(self, message: str, status_code: int = 400, errors: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or {}
