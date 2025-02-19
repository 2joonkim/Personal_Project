from config import db
from flask import Flask
from flask_migrate import Migrate


# API 블루프린트 임포트
from app.views.users import users_bp
from app.views.questions import questions_bp
from app.views.images import images_bp
from app.views.choices import choices_bp
from app.views.answers import answers_bp
from app.views.stats_routes import stats_routes
from app.views.connect import connect_bp
from app.views.questions_1 import questions_1_bp

import app.models

migrate = Migrate()

def create_app():
    application = Flask(__name__)

    # 애플리케이션 설정
    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    # 데이터베이스 및 마이그레이션 초기화
    db.init_app(application)
    migrate.init_app(application, db)

    # 블루프린트 등록
    application.register_blueprint(users_bp)
    application.register_blueprint(questions_bp)
    application.register_blueprint(images_bp)
    application.register_blueprint(choices_bp)
    application.register_blueprint(answers_bp)
    application.register_blueprint(stats_routes)
    application.register_blueprint(connect_bp)
    application.register_blueprint(questions_1_bp)

    return application
