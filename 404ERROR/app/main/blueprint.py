from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__, url_prefix='/')