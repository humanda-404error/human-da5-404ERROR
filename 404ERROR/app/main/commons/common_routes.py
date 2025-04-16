from flask import Blueprint, render_template, session, redirect, url_for, request
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp
from app.models import Member, Notice, Update, Weather, Population, Train, Bus

def register_common_routes(main_bp):  
    @main_bp.route('/')
    def index():
            if 'user_id' not in session:
                return redirect(url_for('auth.login'))  # 로그인 안했으면 로그인으로 보내기
            return render_template('main.html', logged_in=True)
    
    @main_bp.route('/members')
    def members():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('members.html', members=members)


    @main_bp.route('/db_train')
    def db_train():
        page = request.args.get('page', 1, type=int)
        per_page = 100  # 한 페이지에 보여줄 데이터 수

        trains = Train.query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('DB_train.html', trains=trains)
    
    @main_bp.route('/db_bus')
    def db_bus():
        page = request.args.get('page', 1, type=int)
        per_page = 100  # 한 페이지에 보여줄 데이터 수

        buses = Bus.query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('DB_bus.html', buses=buses)

    @main_bp.route('/db_weather')
    def db_weather():
        page = request.args.get('page', 1, type=int)
        per_page = 100  # 한 페이지에 보여줄 데이터 수

        weather_data = Weather.query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('DB_weather.html', weather_data=weather_data)

    @main_bp.route('/db_population')
    def db_population():
        page = request.args.get('page', 1, type=int)
        per_page = 100  # 한 페이지에 보여줄 데이터 수

        populations = Population.query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template('DB_population.html', populations=populations)

