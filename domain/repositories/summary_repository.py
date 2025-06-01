# backend/domain/repositories/summary_repository.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class ISummaryRepository(ABC):
    """
    Interface para geração de resumos de conteúdo.
    Define o contrato que implementações concretas devem cumprir.
    """

    @abstractmethod
    def generate_summary(self) -> Dict[str, Any]:
        """
        Gera um resumo consolidado dos principais dados da plataforma.

        Returns:
            Dict[str, Any]: Dicionário contendo métricas e estatísticas agregadas,
            por exemplo: total de usuários, total de cursos, progresso médio, etc.
        """
        pass
