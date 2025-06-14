from typing import Dict, Any, List
from domain.entities.lesson import Lesson

class ILessonRepository:
    def create(self, course_id: int, data: Dict[str, Any]) -> Lesson:
        """Cria uma nova aula para um curso específico."""
        pass

    def get_or_404(self, lesson_id: int) -> Lesson:
        """Obtém uma aula específica ou levanta erro 404."""
        pass

    def update(self, lesson: Lesson, data: Dict[str, Any]) -> Lesson:
        """Atualiza uma aula existente."""
        pass

    def delete(self, lesson: Lesson) -> None:
        """Deleta uma aula existente."""
        pass

    def list_by_course(self, course_id: int) -> List[Lesson]:
        """Lista todas as aulas de um curso específico."""
        pass
