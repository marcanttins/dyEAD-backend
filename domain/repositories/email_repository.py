# backend/domain/repositories/email_repository.py
from abc import ABC, abstractmethod
from application.dtos.email_dto import EmailDTO

class IEmailRepository(ABC):
    """
    Interface para envio de e-mail na camada de domínio.
    Define o contrato que implementações concretas devem seguir.
    """

    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> EmailDTO:
        """
        Envia um e-mail (pode ser de forma assíncrona) e retorna um DTO com o resultado.

        Args:
            to (str): Endereço de e-mail do destinatário.
            subject (str): Assunto da mensagem.
            body (str): Conteúdo da mensagem.

        Returns:
            EmailDTO: DTO contendo detalhes do envio (timestamp, message_id, metadados).
        """
        pass
