import os
from pymongo import MongoClient
import sys

MONGO_URI = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/calculadora_notas"

def create_indexes():
    print(f"Connecting to {MONGO_URI}...")
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client.get_default_database()
        courses = db.courses
        
        # Check connection
        client.server_info()
        
        print("Creating text index on meta.code...")
        # Dictionary of fields to index with weights
        # Heavily weight the name and code
        courses.create_index(
            [
                ("meta.code", "text")
            ],
            name="course_text_index",
            weights={
                "meta.code": 10
            },
            default_language="spanish"
        )
        print("Index created successfully.")
        
    except Exception as e:
        print(f"Error creating index: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_indexes()
