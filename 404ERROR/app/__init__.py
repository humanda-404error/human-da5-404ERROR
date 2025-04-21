# app/__init__.py

from flask import Flask
from app.extensions import db
import secrets
import os
from app.models import Member, Notice, Update, Weather, Population, Train, Bus  # 모델 불러오기

# 앱 생성 함수
def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'main', 'templates'))
    app.config['SECRET_KEY'] = secrets.token_hex(16) #'my_secret_key_404' #secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flaskuser:1234@192.168.0.62:3306/prj_404error'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
#    app.config['TEMPLATES_AUTO_RELOAD'] = True
#    app.jinja_env.cache = {}
    from app.main.blueprint import main_bp
    from app.main import routes  # 라우트 등록 시 이 import 꼭 필요
    from app.main.commons import common_routes  # 라우트 포함한 모듈들 import만 해도 OK

    db.init_app(app)  # db 초기화

    @app.context_processor
    def inject_user_info():
        from flask import session
        from app.models import Member
        if 'user_id' in session:
            user = Member.query.filter_by(id=session['user_id']).first()
            if user:
                return dict(current_user=user)
        return dict(current_user=None)

    return app, db
