import PyPDF2
import re
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text: text += page_text + " "
    return text

def parse_real_resume(uploaded_file, candidate_id, jd_text):
    text = extract_text_from_pdf(uploaded_file)
    text_low = text.lower()
    
    # 1. Career Objective Extraction
    obj_match = re.search(r'(objective|summary|profile)[:\n](.*?)(?=\n\n|\n[A-Z])', text, re.IGNORECASE | re.DOTALL)
    career_objective = obj_match.group(2).strip() if obj_match else "Not Found"

    # 2. Online Links (GitHub, LinkedIn, Portfolio)
    online_links = re.findall(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', text)
    
    # 3. Education & Degree
    degree_patterns = r'(B\.?Tech|M\.?Tech|B\.?Sc|M\.?Sc|PhD|Bachelor|Master|B\.?E)'
    degree = (re.findall(degree_patterns, text) + ["Not Found"])[0]
    
    # 4. Passing Year (Looks for 4-digit years between 1990 and 2030)
    passing_years = re.findall(r'\b(199\d|20[0-2]\d|2030)\b', text)
    passing_year = passing_years[-1] if passing_years else "N/A" # Usually the last year is the graduation year

    # 5. Skills & Certificate Skills
    # Extracting words near the "Certifications" or "Skills" heading
    cert_match = re.search(r'(certifications|certificates|skills)[:\n](.*?)(?=\n\n|\n[A-Z])', text, re.IGNORECASE | re.DOTALL)
    certificate_skills = cert_match.group(2).strip() if cert_match else "N/A"

    # AI Semantic Match
    res_emb = model.encode(text_low, convert_to_tensor=True)
    jd_emb = model.encode(jd_text.lower(), convert_to_tensor=True)
    similarity = util.cos_sim(res_emb, jd_emb).item()

    return {
        "id": candidate_id,
        "name": "Candidate",
        "career_objective": career_objective,
        "degree": degree,
        "passing_year": passing_year,
        "online_links": ", ".join(online_links[:3]), # Get top 3 links
        "certificate_skills": certificate_skills,
        "years_experience": float(text_low.count('year')),
        "semantic_match_score": similarity,
        "education_level": degree # For the ranking logic
    }