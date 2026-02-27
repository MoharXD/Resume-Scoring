import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("resumes.db")

# Use Pandas to read the table and print it beautifully
try:
    df = pd.read_sql("SELECT * FROM candidates", conn)
    print("--- Database Content ---")
    print(df)
except Exception as e:
    print(f"Error: {e}")

conn.close()