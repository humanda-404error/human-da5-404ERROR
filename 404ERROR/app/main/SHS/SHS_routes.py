from flask import Blueprint, render_template, session, redirect, url_for
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp
from app.models import Member, Notice, Update, Weather, Population, Train

def register_SHS_routes(main_bp):
    @main_bp.route('/compare')
    def compare():
        return render_template('compare.html')
    
    @main_bp.route('/outlier')
    def outlier():
        return render_template('outlier.html')

    @main_bp.route('/explorer')
    def explorer():
        return render_template('explorer.html') 
    @main_bp.route('/chat')
    def chat():
        return render_template('chat.html')
    @main_bp.route('/profile_edit')
    def profile_edit():
        return render_template('profile_edit.html')
    @main_bp.route('/support')
    def support():
        return render_template('support.html')

    #@main_bp.route('/tables')
    #@main_bp.route('/tables')
    #@main_bp.route('/tables')

