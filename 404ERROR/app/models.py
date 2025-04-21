# app/models.py

from app.extensions import db

# db 객체는 app/__init__.py에서 전달된 db를 사용합니다.
# 이 코드에서는 db 객체가 이미 존재한다고 가정하고, 이를 이용하여 모델을 정의합니다.

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(50))
    grade = db.Column(db.String(50))
    points = db.Column(db.Integer)

    def __repr__(self):
        return f'<Member {self.username}>'
    
class Notice(db.Model):
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Notice {self.title}>'

class Update(db.Model):
    __tablename__ = 'updates'
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Update {self.version}>'
    
class Weather(db.Model):
    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column('일시', db.String(20), nullable=False)
    avg_temperature = db.Column('평균기온', db.Float, nullable=False)
    min_temperature = db.Column('최저기온', db.Float, nullable=False)
    max_temperature = db.Column('최고기온', db.Float, nullable=False)
    rainfall_duration = db.Column('강수_계속시간', db.Float, nullable=False)
    daily_rainfall = db.Column('일강수량', db.Float, nullable=False)

    def __repr__(self):
        return f'<Weather {self.date}>'

class Population(db.Model):
    __tablename__ = 'population'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column('일시', db.String(20), nullable=False)
    time_segment = db.Column('시간대구분', db.String(10), nullable=False)
    district = db.Column('자치구', db.String(20), nullable=False)
    total_population = db.Column('총생활인구수', db.Float, nullable=False)
    male_minors = db.Column('남자미성년자', db.Float, nullable=False)
    male_youth = db.Column('남자청년', db.Float, nullable=False)
    male_middle_age = db.Column('남자중년', db.Float, nullable=False)
    male_senior = db.Column('남자노년', db.Float, nullable=False)
    female_minors = db.Column('여자미성년자', db.Float, nullable=False)
    female_youth = db.Column('여자청년', db.Float, nullable=False)
    female_middle_age = db.Column('여자중년', db.Float, nullable=False)
    female_senior = db.Column('여자노년', db.Float, nullable=False)

    def __repr__(self):
        return f'<Population {self.date} {self.district}>'
    
class Train(db.Model):
    __tablename__ = 'train'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column('일시', db.String(20), nullable=False)
    district = db.Column('자치구', db.String(20), nullable=False)
    total_boarding_passengers = db.Column('승차총승객수', db.Float, nullable=False)
    total_dropping_passengers = db.Column('하차총승객수', db.Float, nullable=False)

    def __repr__(self):
        return f'<Train {self.date} {self.district}>'

class Bus(db.Model):
    __tablename__ = 'bus'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column('일시', db.String(20), nullable=False)
    district = db.Column('자치구', db.String(20), nullable=False)
    total_boarding_passengers = db.Column('승차총승객수', db.Float, nullable=False)
    total_dropping_passengers = db.Column('하차총승객수', db.Float, nullable=False)

    def __repr__(self):
        return f'<Bus {self.date} {self.district}>'