
import streamlit as st
import PyPDF2
import docx
import re
from ai_engine import load_model, generate_analysis


st.set_page_config(page_title="AI Resume Advisor", layout="wide")

llm = load_model()

st.title("🤖 AI Resume Advisor")
st.markdown("### Upload your Resume and Job Description to get AI-powered feedback")
st.markdown("""
<div style='background-color:#E0E7FF;padding:20px;border-radius:15px;text-align:center;'>
<h3>🚀 Get Instant Resume Feedback Powered by AI</h3>
<p>Upload your resume and job description to see how well you match!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.main {
    background-color: #f5f7ff;
}

h1 {
    color: #4A4AFF;
    text-align: center;
}

.stButton>button {
    background-color: #4A4AFF;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

.stButton>button:hover {
    background-color: #3737d6;
    color: white;
}
</style>
""", unsafe_allow_html=True)
st.image(
    "https://cdn-icons-png.flaticon.com/512/4712/4712100.png",
    width=150
)



col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("📄 Upload Resume (pdf, txt, docx)", type=["pdf", "txt", "docx"])

with col2:
    jd_text_input = st.text_area(
        "📋 Paste Job Description Here",
        height=300,
        placeholder="Copy and paste the job description here..."
    )

st.markdown("<br>", unsafe_allow_html=True)
analyze_button = st.button("🔍 Analyze Resume Now")



def read_file(uploaded_file):
    if uploaded_file is not None:

        file_name = uploaded_file.name

        if file_name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8")

        elif file_name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                if page.extract_text():
                    text += page.extract_text()
            return text

        elif file_name.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text

    return ""


if analyze_button:

    resume_text = read_file(resume_file)
    jd_text = jd_text_input


    if resume_text and jd_text_input:


        st.success("Files uploaded successfully!")
        with st.spinner("Analyzing with AI..."):
            result = generate_analysis(llm, resume_text, jd_text)

        match = re.search(r"Match Score[:\s]*([0-9]{1,3})", result, re.IGNORECASE)


        if match:
            score = int(match.group(1))
            score = min(score, 100)  # safety cap
        else:
            score = 50  # default if not detected

        st.subheader("📊 Resume–JD Match Score")

        if score >= 75:
            st.success(f"🟢 Strong Match: {score}%")
        elif score >= 50:
            st.warning(f"🟡 Moderate Match: {score}%")
        else:
            st.error(f"🔴 Weak Match: {score}%")

        st.progress(score / 100)

        st.subheader("AI Analysis")
        st.write(result)


    else:
        st.error("Please upload both Resume and Job Description.")
