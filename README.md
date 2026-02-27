# 🚀 AI Resume Screener & Ranker (Hackathon Edition)

An enterprise-grade, full-stack AI hiring platform designed to eliminate recruiter bias, automate candidate scoring, and predict long-term hiring success using Machine Learning.

## 🌟 Key Features
* **🧠 Explainable AI:** Doesn't just score candidates; it generates a "Skill Symmetry Radar Map" and AI commentary explaining exactly *why* they got that score.
* **⚖️ Ethical & Unbiased:** Built-in **Blind Hiring Mode** instantly masks candidate names and emails to prevent unconscious bias.
* **🎛️ Human-in-the-Loop:** Recruiters can use dynamic sliders to adjust scoring weights (Experience, Education, Skills) in real-time.
* **🔮 Predictive ML Engine:** Uses a Random Forest Regressor to predict the statistical probability of a candidate's long-term success.
* **💾 Persistent Database:** Fast API backend coupled with an SQLite database ensures zero data loss between sessions.

## 🛠️ Tech Stack
* **Frontend:** Streamlit, Plotly (Data Visualization)
* **Backend:** FastAPI, Python, SQLite
* **Machine Learning:** Scikit-Learn (Random Forest)

## 🚀 How to Run Locally
Open two terminals:
1. **Start the Backend (Database):** `python -m uvicorn api:app --reload`
2. **Start the Frontend (UI):** `python -m streamlit run app.py`