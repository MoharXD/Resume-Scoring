import pandas as pd
import re

def normalize_cgpa(cgpa_str):
    """Normalizes CGPA to a 0-1.0 float."""
    try:
        val = float(re.findall(r"[-+]?\d*\.\d+|\d+", str(cgpa_str))[0])
        if val > 10: return val / 100
        elif val > 4: return val / 10
        else: return val / 4
    except:
        return 0.7 # Default safe baseline if missing

def calculate_final_score(df, weights):
    """
    Groups the 12 mandatory AI-PS-1 categories under the 4 interactive UI sliders.
    This allows real-time dynamic re-ranking.
    """
    def score_row(row):
        # --- BUCKET 1: EXPERIENCE (Internships + Work History) ---
        # 1 year exp = 10 pts, 1 internship = 20 pts
        exp_pts = min(float(row.get('years_experience', 0)) * 10, 60)
        intern_pts = min(row.get('internship_count', 0) * 20, 40)
        score_exp = exp_pts + intern_pts
        
        # --- BUCKET 2: EDUCATION (Degree Type + Baseline) ---
        degree = str(row.get('degree', 'B.Sc')).lower()
        if 'phd' in degree: score_edu = 100
        elif 'master' in degree or 'm.tech' in degree: score_edu = 90
        elif 'b.tech' in degree or 'bachelor' in degree: score_edu = 80
        else: score_edu = 70
        
        # --- BUCKET 3: SKILLS MATCH (AI Semantic Match + Portfolio Links) ---
        sem_pts = row.get('semantic_match_score', 0) * 100
        bonus_links = 10 if row.get('online_links', 'None Detected') != 'None Detected' else 0
        score_sem = min(sem_pts + bonus_links, 100)
        
        # --- BUCKET 4: ACHIEVEMENTS (Quantifiable Metrics + Extra-curricular) ---
        ach_pts = min(row.get('achievements_count', 0) * 20, 80)
        extra_pts = 20 if row.get('has_extracurricular', False) else 0
        score_ach = ach_pts + extra_pts
        
        # Save these exact bucket scores so the Radar Chart in app.py is 100% accurate!
        row['score_exp'] = score_exp
        row['score_edu'] = score_edu
        row['score_sem'] = score_sem
        row['score_ach'] = score_ach

        # --- APPLY THE UI SLIDER WEIGHTS ---
        # Multiplies the candidate's bucket score by the recruiter's slider setting
        final_score = (
            (score_exp * weights.get('experience', 0.25)) +
            (score_edu * weights.get('education', 0.25)) +
            (score_sem * weights.get('skills', 0.25)) +
            (score_ach * weights.get('achievements', 0.25))
        )

        # Anti-Overfitting Penalty: Punish keyword stuffing
        if row.get('keyword_density', 0) > 0.15:
            final_score -= 5
            
        row['FINAL_SCORE'] = max(0, min(100, final_score))
        return row

    # Apply math to all candidates
    df = df.apply(score_row, axis=1)
    
    # Deterministic Ranking: Sort by score, use experience as a tie-breaker
    return df.sort_values(by=['FINAL_SCORE', 'years_experience'], ascending=False)