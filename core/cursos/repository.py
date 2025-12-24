import os
from pymongo import MongoClient

# Use the same URI as in config or migration script
MONGO_URI = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/calculadora_notas"

# Initialize global client (lazy connection)
client = MongoClient(MONGO_URI)
db = client.get_default_database()
collection = db.courses

def load_course(course_code: str) -> dict:
    data = collection.find_one({"meta.code": course_code.upper()})

    if not data:
        # Try normalized
        code = (course_code[:3] + '-' + course_code[3:]).upper()
        data = collection.find_one({"meta.code": code})

    if not data:
        raise KeyError(f"Curso {course_code} no existe")
    return data

def list_courses(n: int | None = None) -> list[dict]:
    """
    Devuelve hasta n cursos. Si n es None devuelve todos.
    Si n <= 0 devuelve lista vacía.
    """
    if n is not None and n <= 0:
        return []

    cursor = collection.find(limit=n if n else 0)
    return list(cursor)
