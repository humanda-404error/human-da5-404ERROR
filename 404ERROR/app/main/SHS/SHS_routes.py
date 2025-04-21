from flask import Blueprint, render_template, session, redirect, url_for
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp
from app.models import Member, Notice, Update, Weather, Population, Train

def register_SHS_routes(main_bp):
    #-직접적(대중교통+인구)
    #코로나19 전후 교통 및 유동인구 변화 분석 (2020년 기준)
    #분석 예시: 연령대별 생활 인구 감소율 비교
    #활용 예시: 비상상황 시 교통 이용률 변화 예측을 통한 대응 계획 수립, 상권 변화 분석 등
    @main_bp.route('/compare')
    def compare():
        return render_template('SHS/compare.html')
    
    @main_bp.route('/chat')
    def chat():
        return render_template('SHS/chat.html')

    @main_bp.route('/support')
    def support():
        return render_template('SHS/support.html')
    
    @main_bp.route('/outlier')
    def outlier():
        return render_template('outlier.html')

    @main_bp.route('/explorer')
    def explorer():
        return render_template('explorer.html') 

    #@main_bp.route('/tables')
    #@main_bp.route('/tables')
    #@main_bp.route('/tables')

