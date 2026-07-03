import streamlit as st
import PyPDF2
from docx import Document
import ollama

# ----------------------------
# Resume Extractor
# ----------------------------

def extract_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text


def extract_docx(file):
    doc = Document(file)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# ----------------------------
# UI
# ----------------------------

st.title("🤖 AI Resume Analyzer (FREE AI Version)")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

job_description = st.text_area("Paste Job Description")

# ✅ ENTER BUTTON (Analyze Button)
analyze = st.button("🚀 Analyze Resume")

# ----------------------------
# Main Logic
# ----------------------------

if uploaded_file and job_description and analyze:

    # Extract resume
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_pdf(uploaded_file)
    else:
        resume_text = extract_docx(uploaded_file)

    st.subheader("📄 Resume Extracted")
    st.write(resume_text[:1000])

    # AI Prompt
    prompt = f"""
You are a professional HR AI assistant.

Compare the resume with the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Give:
1. Match Score out of 100
2. Strengths
3. Weaknesses
4. Missing Skills
5. Suggestions

Be clear and structured.
"""

    with st.spinner("AI is analyzing... 🤖"):

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response["message"]["content"]

    st.subheader("📊 AI Analysis Result")
    st.write(result)