from .ai_interaction import AIInteraction
from .association import user_course
from .certificate import Certificate
from .course import Course
from .feedback import Feedback
from .forum_post import ForumPost
from .forum_thread import ForumThread
from .material import Material
from .notification import Notification
from .offline_content import OfflineContent
from .progress import Progress
from .quiz import Quiz
from .quiz_question import QuizQuestion
from .recommendation import Recommendation
from .revoked_token import RevokedToken
from .settings import Settings
from .sync_status import SyncStatus
from .user import User

__all__ = [
    "AIInteraction",
    "Certificate",
    "Course",
    "Feedback",
    "ForumPost",
    "ForumThread",
    "Material",
    "Notification",
    "OfflineContent",
    "Progress",
    "Quiz",
    "QuizQuestion",
    "Recommendation",
    "RevokedToken",
    "Settings",
    "SyncStatus",
    "User",
    "user_course"
]