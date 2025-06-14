# backend/application/use_cases/ai_use_cases.py
from typing import Optional
from domain.repositories.ai_repository import IAiRepository
from domain.entities.ai_interaction import AIInteraction

class SendAiInteractionUseCase:
    def __init__(self, repo: IAiRepository):
        self.repo = repo

    def execute(self, user_id: Optional[int], request_text: str) -> AIInteraction:
        return self.repo.create(user_id, request_text)
