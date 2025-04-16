# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
import os

db = SQLAlchemy()  # db 객체를 전역으로 선언

# 앱 생성 함수
def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'main', 'templates'))
    app.config['SECRET_KEY'] = secrets.token_hex(16) #'my_secret_key_404' #secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:1234@localhost:3306/prj_404error'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#    app.config['TEMPLATES_AUTO_RELOAD'] = True
#    app.jinja_env.cache = {}
    from app.main.blueprint import main_bp
    from app.main import routes  # 라우트 등록 시 이 import 꼭 필요
    from app.main.commons import common_routes  # 라우트 포함한 모듈들 import만 해도 OK

    db.init_app(app)  # db 초기화

    return app, db
