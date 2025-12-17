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
