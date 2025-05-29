# backend/application/dtos/email_dto.py
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

@dataclass
class EmailDTO:
    """
    DTO para transação de envio de e-mail.

    Attributes:
        to (str): Endereço de e-mail do destinatário.
        subject (str): Assunto da mensagem.
        body (str): Conteúdo da mensagem.
        sent_at (datetime): Timestamp de quando o e-mail foi enviado.
        message_id (Optional[str]): Identificador retornado pelo serviço de envio, se aplicável.
        metadata (Optional[Dict[str, Any]]): Informações adicionais do envio (status, filas, etc.).
    """
    to: str
    subject: str
    body: str
    sent_at: datetime
    message_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
