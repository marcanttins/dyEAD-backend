# backend/domain/repositories/__init__.py

from .ai_repository import IAiRepository
from .certificate_repository import ICertificateRepository
from .course_repository import ICourseRepository
from .email_repository import IEmailRepository
from .feedback_repository import IFeedbackRepository
from .forum_post_repository import IForumPostRepository
from .forum_thread_repository import IForumThreadRepository
from .leaderboard_repository import ILeaderboardRepository
from .material_repository import IMaterialRepository
from .notification_repository import INotificationRepository
from .offline_content_repository import IOfflineContentRepository
from .progress_repository import IProgressRepository
from .quiz_question_repository import IQuizQuestionRepository
from .quiz_repository import IQuizRepository
from .recommendation_repository import IRecommendationRepository
from .report_repository import IReportRepository
from .revoked_token_repository import IRevokedTokenRepository
from .settings_repository import ISettingsRepository
from .summary_repository import ISummaryRepository
from .sync_status_repository import ISyncStatusRepository
from .token_repository import ITokenRepository
from .user_repository import IUserRepository

__all__ = [
    "IAiRepository",
    "ICertificateRepository",
    "ICourseRepository",
    "IFeedbackRepository",
    "IForumPostRepository",
    "IForumThreadRepository",
    "ILeaderboardRepository",
    "IMaterialRepository",
    "INotificationRepository",
    "IOfflineContentRepository",
    "IProgressRepository",
    "IQuizQuestionRepository",
    "IQuizRepository",
    "IRecommendationRepository",
    "IReportRepository",
    "IRevokedTokenRepository",
    "ISettingsRepository",
    "ISyncStatusRepository",
    "ITokenRepository",
    "IUserRepository",
    "IEmailRepository",
    "ISummaryRepository"
]
