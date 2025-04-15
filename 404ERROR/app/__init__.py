from flask import Flask
from flask import render_template

from flask_login import LoginManager # install
from flask_migrate import Migrate # DB 관리
from flask_sqlalchemy import SQLAlchemy # SQL Query 관리

from .main.routes import main_bp
import secrets
import os


# 앱 생성 함수
def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'main', 'templates'))  
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.register_blueprint(main_bp)

    return app