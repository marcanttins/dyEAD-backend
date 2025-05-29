# backend/infrastructure/repositories/quiz_question_repository_impl.py
from typing import List
from domain.repositories.quiz_question_repository import IQuizQuestionRepository
from domain.entities.quiz import QuizQuestion as QuizQuestionEntity
from infrastructure.extensions import db
from infrastructure.orm.models.quiz_question import QuizQuestion as QuizQuestionModel

class QuizQuestionRepositoryImpl(IQuizQuestionRepository):
    def get_by_quiz(self, quiz_id: int) -> List[QuizQuestionEntity]:
        ms = QuizQuestionModel.query.filter_by(quiz_id=quiz_id).all()
        return [
            QuizQuestionEntity(
                id=m.id,
                quiz_id=m.quiz_id,
                text=m.text,
                options=m.options,
                correct_option=m.correct_option
            ) for m in ms
        ]

    def save_questions(self, quiz_id: int, questions: List[dict]) -> None:
        for q in questions:
            m = QuizQuestionModel(
                quiz_id=quiz_id,
                text=q['text'],
                options=q['options'],
                correct_option=q['correct_option']
            )
            db.session.add(m)
        db.session.commit()
