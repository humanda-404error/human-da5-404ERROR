from flask import Blueprint, render_template, session, redirect, url_for
from app.main.blueprint import main_bp  # routes가 아닌 blueprint에서 불러옴
from app.auth.routes import get_db_connection 
from app.models import Member  # Member 모델을 가져옵니다

from app.main.commons import common_routes
from app.main.JSC import JSC_routes
from app.main.LHK import LHK_routes
from app.main.SHS import SHS_routes