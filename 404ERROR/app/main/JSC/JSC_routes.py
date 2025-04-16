from flask import Blueprint, render_template, session, redirect, url_for
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp


def register_JSC_routes(main_bp): 
    @main_bp.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
    @main_bp.route('/district')
    def district():
        return render_template('district.html')
    