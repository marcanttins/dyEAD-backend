# backend/infrastructure/tasks/generate_certificate.py
from celery import shared_task
from datetime import datetime, timezone
from uuid import uuid4
from infrastructure.repositories.certificate_repository_impl import CertificateRepositoryImpl

certificate_repo = CertificateRepositoryImpl()

@shared_task(name='generate_certificate_task')
def generate_certificate_task(user_id: int, course_id: int, file_url: str = None) -> dict:
    """
    Gera e persiste um certificado para um usuário em um curso.
    Se `file_url` não for fornecido, gera um nome de arquivo padrão.

    Args:
        user_id (int): ID do usuário.
        course_id (int): ID do curso.
        file_url (str, optional): URL ou caminho do arquivo de certificado.

    Returns:
        dict: Detalhes do certificado gerado.
    """
    # Gera URL padrão se não fornecida
    if not file_url:
        file_name = f"{user_id}_{course_id}_{uuid4().hex}.pdf"
        file_url = f"/certificates/{file_name}"

    # Mantém idempotência: evita duplicação de certificados
    existing = certificate_repo.get_by_user_and_course(user_id, course_id)
    if existing:
        certificate = existing
    else:
        certificate = certificate_repo.create(
            user_id=user_id,
            course_id=course_id,
            file_url=file_url,
            issue_date=datetime.now(timezone.utc)
        )

    return {
        'certificate_id': certificate.id,
        'user_id': certificate.user_id,
        'course_id': certificate.course_id,
        'file_url': certificate.file_url,
        'issue_date': certificate.issue_date.isoformat()
    }