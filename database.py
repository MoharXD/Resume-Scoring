# database.py
import sqlite3
import pandas as pd

DB_NAME = "resumes.db"

def init_db():
    # Creates the database and table if it doesn't exist
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            years_experience REAL,
            education_level TEXT,
            semantic_match_score REAL,
            achievements_count INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_candidate(candidate_dict):
    conn = sqlite3.connect(DB_NAME)
    df = pd.DataFrame([candidate_dict])
    # Append the new candidate to the database
    df.to_sql('candidates', conn, if_exists='append', index=False)
    conn.close()

def get_all_candidates():
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql('SELECT * FROM candidates', conn)
    except:
        df = pd.DataFrame() # Return empty if no table yet
    conn.close()
    return df