from typing import Dict, Any, List
from domain.repositories.lesson_repository import ILessonRepository
from domain.entities.lesson import Lesson

class CreateLessonUseCase:
    def __init__(self, lesson_repo: ILessonRepository):
        self.lesson_repo = lesson_repo

    def execute(self, course_id: int, data: Dict[str, Any]) -> Lesson:
        return self.lesson_repo.create(course_id, data)

class GetLessonUseCase:
    def __init__(self, lesson_repo: ILessonRepository):
        self.lesson_repo = lesson_repo

    def execute(self, lesson_id: int) -> Lesson:
        return self.lesson_repo.get_or_404(lesson_id)

class UpdateLessonUseCase:
    def __init__(self, lesson_repo: ILessonRepository):
        self.lesson_repo = lesson_repo

    def execute(self, lesson_id: int, data: Dict[str, Any]) -> Lesson:
        lesson = self.lesson_repo.get_or_404(lesson_id)
        return self.lesson_repo.update(lesson, data)

class DeleteLessonUseCase:
    def __init__(self, lesson_repo: ILessonRepository):
        self.lesson_repo = lesson_repo

    def execute(self, lesson_id: int) -> None:
        lesson = self.lesson_repo.get_or_404(lesson_id)
        self.lesson_repo.delete(lesson)

class ListLessonsUseCase:
    def __init__(self, lesson_repo: ILessonRepository):
        self.lesson_repo = lesson_repo

    def execute(self, course_id: int) -> List[Lesson]:
        return self.lesson_repo.list_by_course(course_id)
