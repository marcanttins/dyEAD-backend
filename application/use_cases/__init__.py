# backend/application/use_cases/__init__.py

from .authenticate_user_use_case import AuthenticateUserUseCase
from .refresh_token_use_case import RefreshTokenUseCase
from .user_use_cases import (
    CreateUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
    GetUserByIdUseCase,
    PaginateUsersUseCase,
)
from .course_use_cases import (
    CreateCourseUseCase,
    GetCourseUseCase,
    UpdateCourseUseCase,
    DeleteCourseUseCase,
    ListCoursesUseCase,
    ListFeaturedCoursesUseCase,
)
from .feedback_use_cases import (
    CreateFeedbackUseCase,
    ListFeedbackByCourseUseCase,
    ListFeedbackByUserUseCase,
)
from .forum_use_cases import (
    CreateThreadUseCase,
    ListThreadsUseCase,
    DeleteThreadUseCase,
    CreatePostUseCase,
    ListPostsUseCase,
)
from .material_use_cases import (
    UploadMaterialUseCase,
    GetMaterialsUseCase,
    DeleteMaterialUseCase,
)
from .notification_use_cases import (
    SendNotificationUseCase,
    ListNotificationsUseCase,
    ListUnreadNotificationsUseCase,
    MarkNotificationReadUseCase,
)
from .offline_content_use_cases import (
    CreateOfflineContentUseCase,
    GetOfflineContentUseCase,
)
from .progress_use_cases import (
    CreateProgressUseCase,
    UpdateProgressUseCase,
    GetProgressUseCase,
    AverageProgressUseCase,
)
from .quiz_use_cases import (
    CreateQuizUseCase,
    ListQuizQuestionsUseCase,
    SaveQuizQuestionsUseCase,
)
from .recommendation_use_cases import (
    CreateRecommendationUseCase,
    ListRecommendationsUseCase,
)
from .report_use_cases import CountUsersUseCase
from .settings_use_cases import (
    GetSettingsUseCase,
    CreateSettingsUseCase,
    UpdateSettingsUseCase,
)
from .revoked_token_use_case import RevokedTokenUseCase
from .sync_status_use_cases import (
    GetSyncStatusUseCase,
    CreateSyncStatusUseCase,
    UpdateSyncStatusUseCase,
)
from .upload_use_cases import UploadUseCase
from .ai_use_cases import SendAiInteractionUseCase
from .email_use_cases import SendEmailUseCase
from .dashboard_use_cases import GetDashboardStatsUseCase
from .summary_use_cases import GetSummaryUseCase
from .tutorbot_use_cases import TutorBotUseCase

__all__ = [
    "AuthenticateUserUseCase",
    "RefreshTokenUseCase",
    "CreateUserUseCase", "UpdateUserUseCase", "DeleteUserUseCase", "GetUserByIdUseCase", "PaginateUsersUseCase",
    "CreateCourseUseCase", "GetCourseUseCase", "UpdateCourseUseCase", "DeleteCourseUseCase", "ListCoursesUseCase", "ListFeaturedCoursesUseCase",
    "CreateFeedbackUseCase", "ListFeedbackByCourseUseCase", "ListFeedbackByUserUseCase",
    "CreateThreadUseCase", "ListThreadsUseCase", "DeleteThreadUseCase", "CreatePostUseCase", "ListPostsUseCase",
    "UploadMaterialUseCase", "GetMaterialsUseCase", "DeleteMaterialUseCase",
    "SendNotificationUseCase", "ListNotificationsUseCase", "ListUnreadNotificationsUseCase", "MarkNotificationReadUseCase",
    "CreateOfflineContentUseCase", "GetOfflineContentUseCase",
    "CreateProgressUseCase", "UpdateProgressUseCase", "GetProgressUseCase", "AverageProgressUseCase",
    "CreateQuizUseCase", "ListQuizQuestionsUseCase", "SaveQuizQuestionsUseCase",
    "CreateRecommendationUseCase", "ListRecommendationsUseCase",
    "CountUsersUseCase",
    "GetSettingsUseCase", "CreateSettingsUseCase", "UpdateSettingsUseCase",
    "GetSyncStatusUseCase", "CreateSyncStatusUseCase", "UpdateSyncStatusUseCase",
    "UploadUseCase",
    "SendAiInteractionUseCase",
    "SendEmailUseCase",
    "GetDashboardStatsUseCase",
    "GetSummaryUseCase",
    "TutorBotUseCase",
    "RevokedTokenUseCase"
]
