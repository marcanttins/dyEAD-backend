# application/dtos/pagination_dto.py
from dataclasses import dataclass
from typing import Generic, TypeVar, List

T = TypeVar('T')

@dataclass(frozen=True)
class PaginationMetaDTO:
    """
    DTO para metadados de paginação.

    Attributes:
        page (int): Número da página atual.
        per_page (int): Quantidade de itens por página.
        total (int): Total de itens disponíveis.
        has_next (bool): Indica se existe próxima página.
        has_prev (bool): Indica se existe página anterior.
        total_pages (int): Total de páginas computado.
    """
    page: int
    per_page: int
    total: int
    has_next: bool
    has_prev: bool
    total_pages: int

@dataclass(frozen=True)
class PaginationDTO(Generic[T]):
    """
    DTO para resposta paginada, contendo itens e metadados.

    Attributes:
        meta (PaginationMetaDTO): Metadados de paginação.
        items (List[T]): Lista de itens da página corrente.
    """
    meta: PaginationMetaDTO
    items: List[T]
