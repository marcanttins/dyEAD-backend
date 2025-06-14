# backend/application/use_cases/course_use_cases.py
from typing import Dict, Any, List
from domain.repositories.course_repository import ICourseRepository
from domain.entities.course import Course

class CreateCourseUseCase:
    def __init__(self, course_repo: ICourseRepository):
        self.course_repo = course_repo

    def execute(self, data: Dict[str, Any], instructor_id: int) -> Course:
        return self.course_repo.create(data, instructor_id)

class GetCourseUseCase:
    def __init__(self, course_repo: ICourseRepository):
        self.course_repo = course_repo

    def execute(self, course_id: int) -> Course:
        return self.course_repo.get_or_404(course_id)

class UpdateCourseUseCase:
    def __init__(self, course_repo: ICourseRepository):
        self.course_repo = course_repo

    def execute(self, course_id: int, data: Dict[str, Any]) -> Course:
        course = self.course_repo.get_or_404(course_id)
        return self.course_repo.update(course, data)

class DeleteCourseUseCase:
    def __init__(self, course_repo: ICourseRepository):
        self.course_repo = course_repo

    def execute(self, course_id: int) -> None:
        course = self.course_repo.get_or_404(course_id)
        self.course_repo.delete(course)

class ListCoursesUseCase:
    def __init__(self, course_repo: ICourseRepository):
        self.course_repo = course_repo

    def execute(self) -> List[Course]:
        return self.course_repo.list_all()

class ListFeaturedCoursesUseCase:
    def __init__(self, course_repo: ICourseRepository):
        self.course_repo = course_repo

    def execute(self, limit: int = 5) -> List[Course]:
        return self.course_repo.list_featured(limit)
