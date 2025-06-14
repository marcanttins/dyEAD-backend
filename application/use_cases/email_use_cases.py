# backend/application/use_cases/email_use_cases.py
from application.dtos.email_dto import EmailDTO
from domain.repositories.email_repository import IEmailRepository

class SendEmailUseCase:
    def __init__(self, email_repo: IEmailRepository):
        self.email_repo = email_repo

    def execute(self, to: str, subject: str, body: str) -> EmailDTO:
        return self.email_repo.send(to, subject, body)
