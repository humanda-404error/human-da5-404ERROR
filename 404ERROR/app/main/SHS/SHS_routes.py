from flask import Blueprint, render_template, session, redirect, url_for
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp


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
        

# @main_bp.route('/tables')
# @main_bp.route('/tables')
# @main_bp.route('/tables')

