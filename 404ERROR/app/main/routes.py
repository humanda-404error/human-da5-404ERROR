from flask import Blueprint, render_template, session, redirect, url_for
import pandas as pd
from app.models import Member  # Member 모델을 가져옵니다
from app.auth.routes import get_db_connection 

main_bp = Blueprint('main', __name__, url_prefix='/')

# 메인 페이지
@main_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # 로그인 안했으면 로그인으로 보내기

    return render_template('main.html', logged_in=True)

#dashboard 클릭시 보이는 페이지
@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/district')
def district():
    return render_template('district.html')

@main_bp.route('/weather')
def weather():
    return render_template('weather.html')

@main_bp.route('/compare')
def compare():
    return render_template('compare.html')

@main_bp.route('/outlier')
def outlier():
    return render_template('outlier.html')

@main_bp.route('/explorer')
def explorer():
    return render_template('explorer.html')

@main_bp.route('/members')
def members():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('members.html', members=members)


# @main_bp.route('/tables')
# @main_bp.route('/tables')
# @main_bp.route('/tables')