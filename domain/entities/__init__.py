# backend/domain/entities/__init__.py

from .ai_interaction import AIInteraction
from .certificate import Certificate
from .course import Course, CourseStatus
from .feedback import Feedback, FeedbackSentiment
from .forum_post import ForumPost
from .forum_thread import ForumThread
from .material import Material
from .notification import Notification
from .user_course import UserCourse
from .offline_content import OfflineContent
from .progress import Progress
from .quiz import Quiz, QuizQuestion
from .recommendation import Recommendation
from .revoked_token import RevokedToken
from .settings import Settings
from .sync_status import SyncStatus
from .user import User, UserRole

__all__ = [
    "AIInteraction",
    "Certificate",
    "Course",
    "CourseStatus",
    "Feedback",
    "FeedbackSentiment",
    "ForumPost",
    "ForumThread",
    "Material",
    "Notification",
    "UserCourse",
    "OfflineContent",
    "Progress",
    "Quiz",
    "QuizQuestion",
    "Recommendation",
    "RevokedToken",
    "Settings",
    "SyncStatus",
    "User",
    "UserRole"
]
