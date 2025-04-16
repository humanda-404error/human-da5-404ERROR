from flask import Blueprint, render_template, session, redirect, url_for, request
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp
from app.models import Member, Notice, Update, Weather, Population, Train, Bus

import requests
from bs4 import BeautifulSoup

def register_common_routes(main_bp):
    @main_bp.route('/main')
    @main_bp.route('/main')
    def main():
        notices = Notice.query.order_by(Notice.created_at.desc()).limit(5).all()
        updates = Update.query.order_by(Update.release_date.desc()).limit(5).all()
        member_count = Member.query.count()

        # 크롤링된 hot issue 데이터
        hot_issues = get_hot_issues()  # ["이슈1", "이슈2", ...] 형태 리스트여야 함

        return render_template(
            'common/main.html',
            notices=notices if notices else [],
            updates=updates if updates else [],
            member_count=member_count if member_count > 0 else [],
            hot_issues=hot_issues if hot_issues else []  # None 대신 빈 리스트로 기본값 설정
        )

    def get_hot_issues():
        try:
            url = "https://www.bigkinds.or.kr/"
            res = requests.get(url)
            res.raise_for_status()  # 요청에 실패하면 예외 발생

            soup = BeautifulSoup(res.text, 'html.parser')

            # <a> 태그에서 'data-topic' 속성 값을 추출
            issue_elements = soup.find_all('a', class_='issupop-btn')

            # 'data-topic' 속성에서 이슈 제목만 추출
            issues = [element.get('data-topic') for element in issue_elements if element.get('data-topic')]

            return issues[:5]  # 첫 5개 이슈만 반환

        except requests.exceptions.RequestException as e:
            print(f"크롤링 중 오류 발생: {e}")
            return []  # 예외 발생 시 빈 리스트 반환
        
    @main_bp.route('/')
    def index():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))

        notices = Notice.query.order_by(Notice.created_at.desc()).limit(5).all()
        updates = Update.query.order_by(Update.release_date.desc()).limit(5).all()
        member_count = Member.query.count()
        hot_issues = get_hot_issues()

        return render_template(
            'common/main.html',
            logged_in=True,
            notices=notices if notices else [],
            updates=updates if updates else [],
            member_count=member_count if member_count > 0 else [],
            hot_issues=hot_issues if hot_issues else []
        )

    @main_bp.route('/members')
    def members():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('DB_static/DB_members.html', members=members)


    @main_bp.route('/db_train')
    def db_train():
        page = request.args.get('page', 1, type=int)
        per_page = 100  # 한 페이지에 보여줄 데이터 수

        trains = Train.query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('DB_static/DB_train.html', trains=trains)
    
    @main_bp.route('/db_bus')
    def db_bus():
        page = request.args.get('page', 1, type=int)
        per_page = 100  # 한 페이지에 보여줄 데이터 수

        buses = Bus.query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('DB_static/DB_bus.html', buses=buses)

    @main_bp.route('/db_weather')
    def db_weather():
        page = request.args.get('page', 1, type=int)
        per_page = 100  # 한 페이지에 보여줄 데이터 수

        weather_data = Weather.query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('DB_static/DB_weather.html', weather_data=weather_data)

    @main_bp.route('/db_population')
    def db_population():
        page = request.args.get('page', 1, type=int)
        per_page = 100  # 한 페이지에 보여줄 데이터 수

        populations = Population.query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('DB_static/DB_population.html', populations=populations)

