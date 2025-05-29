# backend/application/use_cases/quiz_use_cases.py
from typing import List
from domain.repositories.quiz_question_repository import IQuizQuestionRepository
from domain.entities.quiz import Quiz, QuizQuestion
from domain.repositories.quiz_repository import IQuizRepository

class CreateQuizUseCase:
    def __init__(self, repo: IQuizRepository):
        self.repo = repo

    def execute(self, course_id: int, title: str) -> Quiz:
        return self.repo.create(course_id, title)

class ListQuizQuestionsUseCase:
    def __init__(self, repo: IQuizQuestionRepository):
        self.repo = repo

    def execute(self, quiz_id: int) -> List[QuizQuestion]:
        return self.repo.get_by_quiz(quiz_id)

class SaveQuizQuestionsUseCase:
    def __init__(self, repo: IQuizQuestionRepository):
        self.repo = repo

    def execute(self, quiz_id: int, questions: List[dict]) -> None:
        self.repo.save_questions(quiz_id, questions)
