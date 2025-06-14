# backend/interface/http/app.py
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from infrastructure.config import config_by_name, make_celery, make_limiter, setup_swagger
from infrastructure.extensions import db, ma, mail
from infrastructure.logger import setup_logging
from infrastructure.security.jwt import jwt
# Import dos Blueprints
from interfaces.http.controllers.auth_controller import auth_bp
from interfaces.http.controllers.course_controller import courses_bp
from interfaces.http.controllers.feedback_controller import feedback_bp
from interfaces.http.controllers.forum_controller import forum_bp
from interfaces.http.controllers.material_controller import material_bp
from interfaces.http.controllers.email_notification_controller import notifications_bp
from interfaces.http.controllers.offline_content_controller import offline_bp
from interfaces.http.controllers.progress_controller import progress_bp
from interfaces.http.controllers.quiz_controller import quiz_bp
from interfaces.http.controllers.recommendation_controller import recommendation_bp
from interfaces.http.controllers.report_controller import report_bp
from interfaces.http.controllers.settings_controller import settings_bp
from interfaces.http.controllers.summary_controller import summary_bp
from interfaces.http.controllers.sync_status_controller import sync_status_bp
from interfaces.http.controllers.test_controller import test_bp
from interfaces.http.controllers.tutorbot_controller import tutorbot_bp
from interfaces.http.controllers.upload_controller import upload_bp
from interfaces.http.controllers.user_controller import user_bp
from interfaces.http.controllers.lesson_controller import lessons_bp
from interfaces.http.error_handlers import register_error_handlers

migrate = Migrate()

def create_app(config_name: str = 'dev') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Desabilita redirect por slash em todas as rotas
    app.url_map.strict_slashes = False

    # configura logging antes de qualquer log acontecer
    setup_logging(app)

    # Inicializa extensões
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173"], "methods": ["GET", "POST", "PUT", "DELETE"]}},
         expose_headers=["Authorization"],
         supports_credentials=True
         )

    make_celery(app)
    make_limiter(app)
    setup_swagger(app)
    register_error_handlers(app)

    # Registra blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
    app.register_blueprint(forum_bp, url_prefix='/api/forum')
    app.register_blueprint(material_bp, url_prefix='/api/material')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    app.register_blueprint(offline_bp, url_prefix='/api/offline')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')
    app.register_blueprint(quiz_bp, url_prefix='/api/quizzes')
    app.register_blueprint(recommendation_bp, url_prefix='/api/recommendations')
    app.register_blueprint(report_bp, url_prefix='/api/reports')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    app.register_blueprint(summary_bp, url_prefix='/api/summary')
    app.register_blueprint(sync_status_bp, url_prefix='/api/sync')
    app.register_blueprint(test_bp, url_prefix='/api/test')
    app.register_blueprint(tutorbot_bp, url_prefix='/api/tutorbot')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(lessons_bp, url_prefix='/api/lessons')

    # … registre aqui os demais blueprints …

    return app
