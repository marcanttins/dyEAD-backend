# backend/domain/entities/course.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class CourseStatus(Enum):
    """
    Representa o estado de um curso no sistema.

    - DRAFT: rascunho ainda não publicado.
    - ACTIVE: curso disponível para matrícula e acesso.
    - COMPLETED: curso concluído (apenas leitura).
    - ARCHIVED: curso arquivado/desativado.
    """
    DRAFT = 'draft'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    ARCHIVED = 'archived'

@dataclass
class Course:
    """
    Entidade de domínio representando um curso.

    Attributes:
        id (int): Identificador único do curso.
        title (str): Título do curso.
        description (Optional[str]): Descrição detalhada do curso.
        category (Optional[str]): Categoria ou área de conhecimento.
        status (CourseStatus): Estado atual do curso.
        instructor_id (int): ID do usuário instrutor.
        created_at (datetime): Timestamp de criação.
        updated_at (datetime): Timestamp de última atualização.
    """
    id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    status: CourseStatus
    instructor_id: int
    created_at: datetime
    updated_at: datetime
