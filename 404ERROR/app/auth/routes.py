from flask import Blueprint, request, redirect, url_for, render_template, session
import mysql.connector
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# MySQL 연결 함수
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="prj_404error"
    )
    return connection

# 로그인 페이지
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # admin 계정 로그인 처리
        if email == 'admin' and password == '1234':
            session['user_id'] = 'admin'
            return redirect(url_for('main.index'))
        
        # admin이 아닌 경우만 이메일 포맷 검사
        if '@' not in email:
            return render_template('login.html', error="Invalid email format!")
        
        # 일반 회원 로그인 처리
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM members WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('main.index'))
        else:
            return render_template('login.html', error="Invalid login credentials!")

    return render_template('login.html')


# 로그아웃 처리
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # 세션에서 사용자 정보 제거
    return redirect(url_for('auth.login'))  # 로그인 페이지로 리디렉션
