import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core.cursos.repository import load_course, list_courses

try:
    print("Testing list_courses...")
    courses = list_courses(n=5)
    print(f"Found {len(courses)} courses.")
    for c in courses:
        print(f" - {c.get('meta', {}).get('code')}")

    if not courses:
        print("No courses found. Migration might have failed.")
        sys.exit(1)

    first_code = courses[0].get('meta', {}).get('code')
    print(f"\nTesting load_course('{first_code}')...")
    course = load_course(first_code)
    print("Success loading course via meta code.")
    
    # Test case insensitivity/normalization if logic exists
    normalized = first_code.replace("-", "").lower()
    print(f"Testing load_course('{normalized}') (normalized/lowercase)...")
    try:
        course2 = load_course(normalized)
        print("Success loading course via normalized code.")
    except KeyError:
        print("Failed loading via normalized code (Expected if exact match only).")

    print("\nVerification passed.")

except Exception as e:
    print(f"Verification failed: {e}")
    sys.exit(1)
