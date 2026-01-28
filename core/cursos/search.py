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

    cursor = (
        collection.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}, "meta": 1}
        )
        .sort([("score", {"$meta": "textScore"})])
        .limit(limit)
    )

    results = list(cursor)

    if len(results) > 0:
        return results

    return list(
        collection.find(
            {"meta.norm_code": {"$regex": f"^{query}"}},
            {"meta": 1}
        ).limit(limit)
    )
    
