from .auth_controller import auth_bp
from .user_controller import user_bp
from .course_controller import courses_bp
from .feedback_controller import feedback_bp
from .forum_controller import forum_bp
from .material_controller import material_bp
from .notification_controller import notification_bp
from .offline_content_controller import offline_bp
from .progress_controller import progress_bp
from .quiz_controller import quiz_bp
from .recommendation_controller import recommendation_bp
from .report_controller import report_bp
from .settings_controller import settings_bp
from .summary_controller import summary_bp
from .sync_status_controller import sync_status_bp
from .test_controller import test_bp
from .tutorbot_controller import tutorbot_bp
from .upload_controller import upload_bp

__all__ = [
    'auth_bp',
    'user_bp',
    'courses_bp',
    'feedback_bp',
    'forum_bp',
    'material_bp',
    'notification_bp',
    'offline_bp',
    'progress_bp',
    'quiz_bp',
    'recommendation_bp',
    'report_bp',
    'settings_bp',
    'sync_status_bp',
    'summary_bp',
    'test_bp',
    'tutorbot_bp',
    'upload_bp'
]