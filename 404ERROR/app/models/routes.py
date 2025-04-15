from flask import Blueprint, render_template
from models import Member  # 경로 맞게 수정

main_bp = Blueprint('main', __name__)

@main_bp.route('/members')
def show_members():
    members = Member.query.all()
    return render_template('members.html', members=members)