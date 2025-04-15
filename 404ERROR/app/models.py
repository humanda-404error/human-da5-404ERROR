# app/models.py

from flask_sqlalchemy import SQLAlchemy

# db 객체는 app/__init__.py에서 전달된 db를 사용합니다.
# 이 코드에서는 db 객체가 이미 존재한다고 가정하고, 이를 이용하여 모델을 정의합니다.
db = SQLAlchemy()

class Member(db.Model):
    __tablename__ = 'members'  # 실제 테이블 이름
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Member {self.username}>'
