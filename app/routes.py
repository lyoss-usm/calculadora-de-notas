"""
Web routes for Flask application.
Frontend-only routes for the landing page.
Backend API routes will be added in future iterations.
"""
from flask import Blueprint, render_template, abort, request, jsonify
from core.cursos.repository import load_course, list_courses
from core.analisis.roots import find_nota_necesaria, fill_empty_evals
import json
import typing

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Landing page with hero section and courses list."""
    raw = list_courses(n=10)

    courses = []
    for c in raw:
        meta = c.get("meta", {}) or {}
        title = meta.get("name") or c.get("name") or "Sin nombre"
        code = meta.get("code") or "XXX-000"
        icon = meta.get("icon", {}) or {}
        icon_gradient = icon.get("gradient", "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)")
        icon_file = icon.get("svg", "book")

        # Load SVG content from static files
        try:
            with open(f"app/static/svg/{icon_file}.svg", "r", encoding="utf-8") as f:
                icon_svg = f.read()
        except FileNotFoundError:
            with open(f"app/static/svg/book.svg", "r", encoding="utf-8") as f:
                icon_svg = f.read()

        evals = c.get("evaluations", []) or []

        # Heurísticas simples para detectar tipos de evaluación
        evals_l = [str(e).strip().lower() for e in evals]
        certamenes = any("certamen" in e or (len(e) > 0 and e[0] == "c") for e in evals_l)
        controles = any("control" in e or e.startswith("q") or e.startswith("ca") for e in evals_l)
        tareas = any("tarea" in e or e.startswith("t") for e in evals_l)
        proyecto = any("proyecto" in e or e.startswith("p") for e in evals_l)
        laboratorio = any("laboratorio" in e or e.startswith("l") for e in evals_l)

        courses.append({
            "title": title,
            "code": code,
            "icon_gradient": icon_gradient,
            "icon_svg": icon_svg,
            "certamenes": certamenes,
            "controles": controles,
            "tareas": tareas,
            "proyecto": proyecto,
            "laboratorio": laboratorio,
        })

    return render_template("index.html", courses=courses)


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






