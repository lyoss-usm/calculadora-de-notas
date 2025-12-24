import json
import os
from pathlib import Path
from pymongo import MongoClient

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_PATH = BASE_DIR / "core" / "cursos" / "models"
MONGO_URI = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/calculadora_notas"

def migrate():
    print(f"Connecting to MongoDB at {MONGO_URI}...")
    client = MongoClient(MONGO_URI)
    db = client.get_default_database()
    collection = db.courses

    print(f"Reading files from {MODELS_PATH}...")
    
    count = 0
    if not MODELS_PATH.exists():
        print(f"Error: {MODELS_PATH} does not exist.")
        return

    for file_path in MODELS_PATH.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            code = data.get("meta", {}).get("code")
            if not code:
                code = file_path.stem
                print(f"Warning: No code in meta for {file_path.name}, skipping.")
                continue

            result = collection.update_one(
                {"meta.code": code},
                {"$set": data},
                upsert=True
            )
            
            if result.upserted_id:
                print(f"Inserted {code}")
            else:
                print(f"Updated {code}")
                
            count += 1
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    print(f"Migration completed. Processed {count} files.")
    client.close()

if __name__ == "__main__":
    migrate()
