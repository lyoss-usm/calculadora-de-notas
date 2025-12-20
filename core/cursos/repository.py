import json
from pathlib import Path

MODELS_PATH = Path(__file__).parent / "models"
CACHE = {}

def load_course(course_code: str) -> dict:
    code = course_code.replace("-", "").upper()
    if code in CACHE:
        return CACHE[code]

    path = MODELS_PATH / f"{code}.json"
    if not path.exists():
        raise KeyError(f"Curso {course_code} no existe")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    CACHE[code] = data
    return data

def list_courses(n: int | None = None) -> list[dict]:
    """
    Devuelve hasta n cursos. Si n es None devuelve todos.
    Si n <= 0 devuelve lista vacía.
    """
    courses = []

    if n is not None and n <= 0:
        return courses

    count = 0
    for file in MODELS_PATH.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            courses.append(data)
            count += 1
            if n is not None and count >= n:
                break

    return courses
