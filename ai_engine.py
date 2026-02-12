from transformers import pipeline
import re
def load_model():
    return pipeline(
        "text-generation",
        model="google/flan-t5-base"
    )



COMMON_SKILLS = [
    "python", "java", "c++", "sql", "machine learning",
    "deep learning", "nlp", "tensorflow", "pytorch",
    "pandas", "numpy", "scikit-learn",
    "streamlit", "fastapi", "flask",
    "aws", "azure", "gcp",
    "git", "docker", "kubernetes"
]

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in COMMON_SKILLS:
        if skill in text:
            found.append(skill)
    return list(set(found))

def calculate_match(resume_skills, jd_skills):
    if not jd_skills:
        return 0

    matched = set(resume_skills) & set(jd_skills)
    score = int((len(matched) / len(jd_skills)) * 100)
    return min(score, 100), list(matched)



def generate_analysis(llm, resume_text, jd_text):

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    score, matched_skills = calculate_match(resume_skills, jd_skills)

    prompt = f"""
You are a professional AI Hiring Consultant.

Candidate Skills:
{resume_skills}

Job Required Skills:
{jd_skills}

Matched Skills:
{matched_skills}

Base Skill Match Score: {score}%

Now provide:

1. Refined Final Match Score (consider overall alignment)
2. Strengths
3. Skill Gaps
4. Resume Improvement Suggestions

Be concise and professional.
"""

    response = llm(prompt, max_length=400)
    result = response[0]["generated_text"]

    return result


    
