from fastapi import FastAPI, UploadFile, File, Form
from parser import parse_real_resume
from io import BytesIO
import sqlite3
import uuid

app = FastAPI()
DB_FILE = "resumes.db"

def init_db():
    """Creates the physical resumes.db file and table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            years_experience REAL,
            education_level TEXT,
            degree TEXT,
            passing_year TEXT,
            semantic_match_score REAL,
            certificate_skills TEXT,
            online_links TEXT,
            career_objective TEXT,
            internship_count INTEGER,
            achievements_count INTEGER,
            has_online_presence BOOLEAN,
            has_extracurricular BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the server starts
init_db()

@app.get("/candidates/")
async def get_candidates():
    """Fetches all candidates from the physical SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # This tells SQLite to return dictionary-like objects
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to standard Python dictionaries so the frontend can read them
    return [dict(row) for row in rows]

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...), jd_text: str = Form(...)):
    """Extracts data and saves it permanently to resumes.db"""
    content = await file.read()
    data = parse_real_resume(BytesIO(content), str(uuid.uuid4()), jd_text)
    
    # Ensure name fallback
    cand_name = file.filename.replace(".pdf", "").title()
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Safely insert the parsed data into the database
    cursor.execute('''
        INSERT INTO candidates (
            id, name, email, years_experience, education_level, degree, passing_year,
            semantic_match_score, certificate_skills, online_links, career_objective,
            internship_count, achievements_count, has_online_presence, has_extracurricular
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get("id"), cand_name, data.get("email"), data.get("years_experience", 0.0),
        data.get("education_level", "Unknown"), data.get("degree", "Unknown"), data.get("passing_year", "Unknown"),
        data.get("semantic_match_score", 0.0), data.get("certificate_skills", "N/A"),
        data.get("online_links", "N/A"), data.get("career_objective", "N/A"),
        data.get("internship_count", 0), data.get("achievements_count", 0),
        data.get("has_online_presence", False), data.get("has_extracurricular", False)
    ))
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": f"{cand_name} added to database."}

@app.delete("/clear/")
async def clear_db():
    """Wipes the physical database table cleanly."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM candidates")
    conn.commit()
    conn.close()
    return {"status": "Database wiped successfully"}