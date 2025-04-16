from flask import Blueprint, render_template, session, redirect, url_for
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp


def register_LHK_routes(main_bp):
    @main_bp.route('/weather')
    def weather():
        return render_template('weather.html') 
    