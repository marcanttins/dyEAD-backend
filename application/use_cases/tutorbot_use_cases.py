# backend/application/use_cases/tutorbot_use_cases.py

from domain.repositories.ai_repository import IAiRepository
from domain.entities.ai_interaction import AIInteraction
from domain.exceptions import APIError


class TutorBotUseCase:
    """
    Caso de uso para interagir com o TutorBot (IA).
    """

    def __init__(self, ai_repo: IAiRepository):
        self.ai_repo = ai_repo

    def execute(self, *, user_id: int, prompt: str) -> AIInteraction:
        """
        Envia o prompt para o repositório de IA e retorna a interação.

        :param user_id: ID do usuário que faz a requisição
        :param prompt: texto a ser enviado ao TutorBot
        :raises APIError: se a chamada à IA falhar
        """
        try:
            return self.ai_repo.create(user_id=user_id, request_text=prompt)
        except Exception as e:
            raise APIError(f"Falha na interação com TutorBot: {e}")

    def list_history(self, *, user_id: int) -> list[AIInteraction]:
        """
        Recupera o histórico de interações do usuário.

        :param user_id: ID do usuário
        :raises APIError: se a recuperação falhar
        """
        try:
            return self.ai_repo.list_by_user(user_id=user_id)
        except Exception as e:
            raise APIError(f"Falha ao recuperar histórico do TutorBot: {e}")
