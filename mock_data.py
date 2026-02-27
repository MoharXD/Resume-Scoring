import pandas as pd
import random

def get_dummy_candidates(count=25):
    # This generates 25 fake candidates so you can build the UI today
    data = []
    names = ["Aarav", "Bianca", "Charlie", "Diya", "Ethan", "Fatima", "Gourav"]
    degrees = ["B.Tech", "M.Tech", "PhD", "B.Sc"]
    
    for i in range(count):
        data.append({
            "id": i,
            "name": f"{random.choice(names)} {i}",
            "email": f"candidate{i}@example.com",  # <-- ADDED FAKE EMAIL
            "phone": "555-010-9999",               # <-- ADDED FAKE PHONE
            "years_experience": round(random.uniform(0, 10), 1),
            "education_level": random.choice(degrees),
            "semantic_match_score": round(random.uniform(0.5, 0.99), 2),
            "achievements_count": random.randint(0, 5)
        })
    return pd.DataFrame(data)