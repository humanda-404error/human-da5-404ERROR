from flask import Blueprint, render_template, session, redirect, url_for
from app.main.blueprint import main_bp  # routes가 아닌 blueprint에서 불러옴
from app.auth.routes import get_db_connection 
from app.models import Member  # Member 모델을 가져옵니다

from app.main.commons.common_routes import register_common_routes
from app.main.JSC.JSC_routes import register_JSC_routes
from app.main.SHS.SHS_routes import register_SHS_routes
from app.main.LHK.LHK_routes import register_LHK_routes

# blueprint는 따로 선언되어 있어야 함
from app.main.blueprint import main_bp

# 라우트 등록
register_common_routes(main_bp)
register_JSC_routes(main_bp)
register_SHS_routes(main_bp)
register_LHK_routes(main_bp)


