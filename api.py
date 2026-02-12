from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import load_model, generate_analysis

app = FastAPI()

llm = load_model()

class ResumeRequest(BaseModel):
    resume_text: str
    jd_text: str


@app.post("/analyze")
def analyze_resume(data: ResumeRequest):
    result = generate_analysis(llm, data.resume_text, data.jd_text)
    return {"analysis": result}
