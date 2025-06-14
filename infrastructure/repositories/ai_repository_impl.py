# backend/infrastructure/repositories/ai_repository_impl.py
from typing import Optional, List
from domain.repositories.ai_repository import IAiRepository
from domain.entities.ai_interaction import AIInteraction as AIInteractionEntity
from infrastructure.extensions import db
from infrastructure.orm.models.ai_interaction import AIInteraction as AIInteractionModel

class AiRepositoryImpl(IAiRepository):
    """
    Implementação concreta de IARepository usando SQLAlchemy.
    """

    def create(self, user_id: Optional[int], request_text: str) -> AIInteractionEntity:
        """
        Persiste uma nova interação com IA no banco.

        Args:
            user_id (Optional[int]): ID do usuário ou None.
            request_text (str): Texto enviado ao modelo de IA.

        Returns:
            AIInteractionEntity: Entidade de domínio criada.
        """
        model = AIInteractionModel(
            user_id=user_id,
            request_text=request_text,
            # O response_text deve ser preenchido após chamar o serviço externo
            response_text=""
        )
        db.session.add(model)
        db.session.commit()

        # Aqui você poderia chamar o serviço de IA e atualizar o response_text:
        # from backend.infrastructure.services.ai_service_impl import AIServiceImpl
        # response = AIServiceImpl().chatbot_response(request_text)
        # model.response_text = response
        # db.session.commit()

        return AIInteractionEntity(
            id=model.id,
            user_id=model.user_id,
            request_text=model.request_text,
            response_text=model.response_text,
            created_at=model.created_at
        )

    def list_by_user(self, user_id: int) -> List[AIInteractionEntity]:
        """
        Recupera todas as interações de IA de um usuário.

        Args:
            user_id (int): ID do usuário.

        Returns:
            List[AIInteractionEntity]: Lista ordenada por data.
        """
        models = (
            AIInteractionModel.query
            .filter_by(user_id=user_id)
            .order_by(AIInteractionModel.created_at.asc())
            .all()
        )
        return [
            AIInteractionEntity(
                id=m.id,
                user_id=m.user_id,
                request_text=m.request_text,
                response_text=m.response_text,
                created_at=m.created_at
            )
            for m in models
        ]
