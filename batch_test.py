import os
import requests
import time

API_URL = "http://127.0.0.1:8000/upload/"
RESUME_DIR = "./test_resumes/" # Put 25 PDFs in this folder

def run_batch_evaluation():
    files = [f for f in os.listdir(RESUME_DIR) if f.endswith(".pdf")]
    if len(files) < 25:
        print(f"Warning: Only {len(files)} resumes found. Need 25 for PS ID: AI-PS-1.")
    
    print(f"🚀 Starting Batch Evaluation for {len(files)} resumes...")
    start_time = time.time()
    
    for filename in files:
        with open(os.path.join(RESUME_DIR, filename), "rb") as f:
            payload = {"jd_text": "Looking for Python developer with Data Science skills."}
            response = requests.post(API_URL, files={"file": f}, data=payload)
            print(f"Processed {filename}: {response.status_code}")

    duration = time.time() - start_time
    print(f"✅ Batch processing complete in {duration:.2f} seconds.")

if __name__ == "__main__":
    run_batch_evaluation()