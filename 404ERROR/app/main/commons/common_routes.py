from flask import Blueprint, render_template, session, redirect, url_for
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp

#dashboard 클릭시 보이는 페이지
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

    
