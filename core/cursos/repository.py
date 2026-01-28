import os
from pymongo import MongoClient

try:
    from core.cursos.search import search, normalize
except:
    import search

try:
    from scraping import main as scraping_main
except:
    from core.cursos.scraping import main as scraping_main

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

def search_courses(query: str, limit: int = 10) -> list[dict]:
    """
    Busca cursos que coincidan con la query usando índice de texto.
    Ordena por relevancia (textScore).
    """
    if not query:
        return []

    return search(query, limit, collection)

def clear_database():
    """
    Elimina todos los cursos de la base de datos.
    Usar con precaución.
    """
    collection.delete_many({})


if __name__ == "__main__":
    collection.delete_many({})

    ans = input("¿Desea descargar cursos y generar modelos JSON? (s/n): ").strip().lower()
    while ans == 's':
        scraping_main(collection)
        ans = input("¿Desea descargar más cursos? (s/n): ").strip().lower()

    collection.drop_indexes()
    collection.create_index([("meta.norm_name", "text")], default_language="spanish")
    
    courses = list_courses(5)
    for course in courses:
        print(f"{course['meta']['code']}: {course['meta']['name']}")
