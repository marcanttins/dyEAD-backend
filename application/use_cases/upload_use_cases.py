# backend/application/use_cases/upload_use_cases.py
from domain.repositories.material_repository import IMaterialRepository
from typing import Any

class UploadUseCase:
    def __init__(self, repo: IMaterialRepository):
        self.repo = repo

    def execute(self, course_id: int, file_data: Any) -> Any:
        url = self._store_file(file_data)
        return self.repo.create(course_id, file_data.filename, url, 'file')

    @staticmethod
    def _store_file(file_data: Any) -> str:
        return f"/uploads/{file_data.filename}"
