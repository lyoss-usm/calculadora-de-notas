"""
Web routes for Flask application.
Frontend-only routes for the landing page.
Backend API routes will be added in future iterations.
"""
from flask import Blueprint, render_template, abort, request, jsonify
from core.cursos.repository import load_course
from core.cursos.evaluator import eval_node

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Landing page with hero section and popular courses."""
    return render_template('index.html')

@bp.route("/curso/<course_code>")
def course_detail(course_code):
    try:
        course = load_course(course_code)
    except KeyError:
        abort(404)

    meta = course["meta"]

    return render_template(
        "course_detail.html",
        course_name=meta["name"],
        course_code=meta["code"],
        icon_gradient=meta["icon"]["gradient"],
        icon_svg=meta["icon"]["svg"],
        model=course
    )


@bp.route("/api/grades/<course_code>", methods=["POST"])
def save_grades(course_code):
    data = request.get_json()
    grades = data.get("grades", [])
    
    try:
        course = load_course(course_code)
    except KeyError:
        return jsonify({"status": "error", "message": "Curso no encontrado"}), 404
    
    current_grades = [g if g is not None else 0 for g in grades]
    context_current = {"notas": current_grades}
    current_grade = eval_node(course["formula"], context_current)
    
    max_grades = [g if g is not None else 100 for g in grades]
    context_max = {"notas": max_grades}
    max_achievable = eval_node(course["formula"], context_max)
    
    min_grades = [g if g is not None else 0 for g in grades]
    context_min = {"notas": min_grades}
    min_achievable = eval_node(course["formula"], context_min)
    
    return jsonify({
        "status": "success",
        "current": round(current_grade, 1),
        "max_achievable": round(max_achievable, 1),
        "min_achievable": round(min_achievable, 1)
    })



