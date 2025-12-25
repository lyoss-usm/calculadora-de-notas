import unicodedata
import re

def normalize(s: str) -> str:
    s = s.lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9\s]", "", s)
    return s.strip()

def levenshtein_distance(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a

    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            insert = current[j - 1] + 1
            delete = previous[j] + 1
            replace = previous[j - 1] + (ca != cb)
            current.append(min(insert, delete, replace))
        previous = current

    return previous[-1]

def search(query: str, limit: int = 10, collection = None) -> list[dict]:
    query = normalize(query)

    # Get all courses names and codes from the database
    cursor = collection.find({}, {"meta.name": 1, "meta.code": 1})
    COURSES = list(cursor)

    print(COURSES)

    results = []
    for course in COURSES:
        print(f"Comparando {query} con {course['meta']['name']}")
        normalized_name = normalize(course["meta"]["name"])
        print(f"Normalizado: {normalized_name}")
        distance = levenshtein_distance(query, normalized_name)
        print(f"Distancia: {distance}")

        len_diff = len(normalized_name) - len(query)

        # Only include candidates that have some similarity
        results.append((distance - len_diff, course))

    # Sort by distance (lower is better) and return the top results
    results.sort(key=lambda x: x[0])

    for r in results:
        print(f"Distancia: {r[0]}, Curso: {r[1]['meta']['name']}")
    return [r[1] for r in results[:limit]]

    
