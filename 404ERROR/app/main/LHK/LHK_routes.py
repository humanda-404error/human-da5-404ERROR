from flask import Blueprint, render_template, session, redirect, url_for
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp
from app.models import Member, Notice, Update, Weather, Population, Train

def register_LHK_routes(main_bp):
    @main_bp.route('/weather')
    def weather():
        return render_template('LHK/weather.html')
    
    @main_bp.route('/profile_edit')
    def profile_edit():
        return render_template('LHK/profile_edit.html') 
    
    #@...
    