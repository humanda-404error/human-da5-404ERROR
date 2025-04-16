# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
import os

db = SQLAlchemy()  # db 객체를 전역으로 선언

# 앱 생성 함수
def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'main', 'templates'))
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:1234@localhost:3306/prj_404error'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#    app.config['TEMPLATES_AUTO_RELOAD'] = True
#    app.jinja_env.cache = {}

    db.init_app(app)  # db 초기화

    return app, db
