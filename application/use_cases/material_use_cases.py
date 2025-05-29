# backend/application/use_cases/material_use_cases.py
from typing import List
from domain.repositories.material_repository import IMaterialRepository
from domain.entities.material import Material

class UploadMaterialUseCase:
    def __init__(self, material_repo: IMaterialRepository):
        self.material_repo = material_repo

    def execute(self, course_id: int, name: str, url: str, material_type: str) -> Material:
        return self.material_repo.create(course_id, name, url, material_type)

class GetMaterialsUseCase:
    def __init__(self, material_repo: IMaterialRepository):
        self.material_repo = material_repo

    def execute(self, course_id: int) -> List[Material]:
        return self.material_repo.get_by_course(course_id)

class DeleteMaterialUseCase:
    def __init__(self, material_repo: IMaterialRepository):
        self.material_repo = material_repo

    def execute(self, material_id: int) -> None:
        materials = self.material_repo.get_by_course(material_id)
        for m in materials:
            if m.id == material_id:
                self.material_repo.delete(m)
                return
        raise ValueError("Material não encontrado")
