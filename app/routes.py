"""
Web routes for Flask application.
Frontend-only routes for the landing page.
Backend API routes will be added in future iterations.
"""
from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Landing page with hero section and popular courses."""
    return render_template('index.html')
