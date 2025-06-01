# backend/domain/repositories/ai_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.ai_interaction import AIInteraction

class IAiRepository(ABC):
    """
    Interface para persistência de interações com inteligência artificial.
    Define o contrato que implementações concretas devem seguir.
    """

    @abstractmethod
    def create(
        self,
        user_id: Optional[int],
        request_text: str
    ) -> AIInteraction:
        """
        Cria e persiste uma nova interação com o modelo de IA.

        Args:
            user_id (Optional[int]): Identificador do usuário que originou a interação, ou None para interações anônimas.
            request_text (str): Texto da requisição enviada ao modelo de IA.

        Returns:
            AIInteraction: Entidade representando a interação completa, incluindo resposta e timestamp.
        """
        pass

    @abstractmethod
    def list_by_user(
        self,
        user_id: int
    ) -> List[AIInteraction]:
        """
        Recupera o histórico de interações de um usuário.

        Args:
            user_id (int): Identificador do usuário.

        Returns:
            List[AIInteraction]: Lista de interações do usuário, ordenadas cronologicamente.
        """
        pass