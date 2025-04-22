from flask import Blueprint, request, redirect, url_for, render_template, session
import mysql.connector
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# MySQL 연결 함수 (로컬 DB)
def get_db_connection():
    connection = mysql.connector.connect(
        host="192.168.0.62",  # 로컬 DB 서버
        user="flaskuser",  # DB 사용자
        password="1234",  # DB 비밀번호
        database="prj_404error",  # DB 이름
        auth_plugin="caching_sha2_password"
    )
    return connection

# 로그인 페이지
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # admin 계정 로그인 처리 (직접 입력된 관리자 계정)
        if email == 'admin' and password == '1234':
            session['user_id'] = 1  # 실제 DB상의 admin id
            session['email'] = 'admin'
            session['nickname'] = '관리자'
            session['grade'] = '관리자'
            session['points'] = 99999
            return redirect(url_for('main.index'))
        
        # 이메일 포맷 검사 (일반 회원의 경우)
        if '@' not in email:
            return render_template('LHK/login.html', error="등록된 사용자가 아닙니다.")
        
        # 일반 회원 로그인 처리
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # dictionary=True로 결과를 딕셔너리 형식으로 받음
        cursor.execute("SELECT * FROM members WHERE email = %s", (email,))  # 이메일로 사용자 조회
        user = cursor.fetchone()  # 하나의 사용자만 가져오기
        cursor.close()
        conn.close()
        
        # 비밀번호 확인 후 로그인 처리
        if user and check_password_hash(user['password'], password):  # 비밀번호 확인
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['grade'] = user['grade']
            session['points'] = user['points']
            session['nickname'] = user['nickname']
            return redirect(url_for('main.index'))  # 로그인 후 메인 페이지로 리디렉션
        else:
            return render_template('LHK/login.html', error="Invalid login credentials!")  # 로그인 실패시 오류 메시지 표시

    # GET 요청 시 로그인 페이지 렌더링
    return render_template('LHK/login.html')


# 로그아웃 처리
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # 세션에서 사용자 정보 제거
    session.clear()
    return redirect(url_for('auth.login'))  # 로그인 페이지로 리디렉션

# @auth_bp.route('/login', methods=['GET', 'POST'])
# def register():
#     return render_template('LHK/register.html')

# @auth_bp.route('/find_account', methods=['GET', 'POST'])
# def register():
#     return render_template('LHK/register.html')

# @auth_bp.route('/find_account')
# def find_account():
#     return render_template('LHK/find_account.html')  # 템플릿 경로는 실제 파일 위치에 맞게 조정
