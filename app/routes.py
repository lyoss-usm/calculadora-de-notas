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


@bp.route('/curso/<course_code>')
def course_detail(course_code):
    """Página de detalle del curso con gráfico y evaluaciones."""
    # Datos de ejemplo - se reemplazarán con datos reales
    course_data = {
        'MAT-101': {
            'name': 'Matemáticas I',
            'code': 'MAT-101',
            'icon_gradient': 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
            'icon_svg': '<svg width="40" height="40" viewBox="0 0 24 24" fill="none"><path d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        },
        'FIS-110': {
            'name': 'Física Mecánica',
            'code': 'FIS-110',
            'icon_gradient': 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            'icon_svg': '<svg width="40" height="40" viewBox="0 0 24 24" fill="none"><path d="M13 10V3L4 14h7v7l9-11h-7z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        }
    }
    
    # Obtener curso o usar el primero por defecto
    course = course_data.get(course_code, course_data['MAT-101'])
    
    return render_template('course_detail.html',
                         course_name=course['name'],
                         course_code=course['code'],
                         icon_gradient=course['icon_gradient'],
                         icon_svg=course['icon_svg'])
