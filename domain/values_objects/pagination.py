# backend/domain/value_objects/pagination_dto.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Pagination:
    """
    Value Object que representa metadados de paginação.

    Attributes:
        page (int): Página atual.
        per_page (int): Número de itens por página.
        total (int): Total de itens disponíveis.
        has_next (bool): Se há próxima página.
        has_prev (bool): Se há página anterior.
    """
    page: int
    per_page: int
    total: int
    has_next: bool
    has_prev: bool

    @property
    def total_pages(self) -> int:
        """
        Calcula a quantidade total de páginas.
        """
        if self.per_page == 0:
            return 0
        return (self.total + self.per_page - 1) // self.per_page
