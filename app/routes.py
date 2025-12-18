"""
Web routes for Flask application.
Frontend-only routes for the landing page.
Backend API routes will be added in future iterations.
"""
from flask import Blueprint, render_template, abort, request, jsonify
from core.cursos.repository import load_course
from core.analisis.roots import find_nota_necesaria, fill_empty_evals
import json

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
    '''
    Requests JSON with:
    ```
    {
        "goal": float,
        "grades": [float],
        "filled": [bool]
    }
    ```

    Returns JSON with:
    ```
    {
        "success": bool,
        "message": str,
        "current_grade": float,
        "max_grade": float,
        "needed_grade": float or "--"
    }
    ```
    '''
    data = request.get_json()

    goal = data.get("goal", 55.0)
    grades = data.get("grades", [])
    filled = data.get("filled", [])

    empty_vals = [i for i in range(len(grades)) if not filled[i]]

    try:
        course = load_course(course_code)
    except KeyError:
        return jsonify({"error": "Curso no encontrado"}), 404
    ctx = course["context"]
    ctx["values"] = grades

    out = {
        "success": True,
        "message": "",

        "current_grade": 0.0,
        "max_grade": 0.0,
        "needed_grade": 0.0
    }

    nota_necesaria = find_nota_necesaria(course, empty_vals, goal)

    if nota_necesaria is None or nota_necesaria > 100.0:
        out["message"] = "No es posible alcanzar la nota objetivo con las evaluaciones restantes."
        out["success"] = False
        out["needed_grade"] = "--"
    else:
        out["needed_grade"] = round(nota_necesaria) if 0.0 <= nota_necesaria else 0.0
    current_grade = fill_empty_evals(course, empty_vals, 0.0)
    max_grade = fill_empty_evals(course, empty_vals, 100.0)

    out["current_grade"] = round(current_grade)
    out["max_grade"] = round(max_grade)

    # Print out in JSON format
    print(json.dumps(out, indent=4, ensure_ascii=False))
    
    return jsonify(out)


    



