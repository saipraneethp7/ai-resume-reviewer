import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import PyPDF2
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Resume Reviewer", page_icon="📄", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding: 2rem 3rem; }
    .header-container {
        background: linear-gradient(135deg, #1a1f2e, #2d3561);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        border: 1px solid #3d4475;
    }
    .header-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }
    .header-subtitle {
        font-size: 1rem;
        color: #8b92b8;
        margin-top: 0.4rem;
    }
    .section-card {
        background-color: #1a1f2e;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #2d3561;
    }
    .score-card {
        background: linear-gradient(135deg, #1a1f2e, #2d3561);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #3d4475;
        text-align: center;
    }
    .score-number {
        font-size: 3.5rem;
        font-weight: 800;
        color: #7c83f5;
    }
    .score-label {
        font-size: 0.9rem;
        color: #8b92b8;
        margin-top: 0.2rem;
    }
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #2d3561;
    }
    .strength-title { color: #4ade80; }
    .gap-title { color: #f87171; }
    .fix-title { color: #fbbf24; }
    .stTextArea textarea {
        background-color: #1a1f2e;
        border: 1px solid #2d3561;
        border-radius: 10px;
        color: #e0e0e0;
        font-size: 0.9rem;
    }
    .stButton button {
        background: linear-gradient(135deg, #7c83f5, #5b63d3);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton button:hover { opacity: 0.9; }
    .stTabs [data-baseweb="tab"] { color: #8b92b8; }
    .stTabs [aria-selected="true"] { color: #7c83f5; }
    label, .stSubheader { color: #c0c4e0 !important; }
    h3 { color: #c0c4e0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="header-title">📄 AI Resume Reviewer</div>
    <div class="header-subtitle">Paste or upload your resume and a job description to get instant AI-powered feedback tailored to the role.</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Your Resume")
    upload_tab, paste_tab = st.tabs(["Upload PDF", "Paste Text"])
    resume_text = ""

    with upload_tab:
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
        if uploaded_file is not None:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
            st.success("Resume uploaded successfully!")

    with paste_tab:
        resume_text_pasted = st.text_area(
            "Resume",
            height=300,
            label_visibility="collapsed",
            placeholder="Paste your resume text here..."
        )
        if resume_text_pasted.strip() != "":
            resume_text = resume_text_pasted

with col2:
    st.subheader("Job Description")
    job_text = st.text_area(
        "Job Description",
        height=350,
        label_visibility="collapsed",
        placeholder="Paste the job description here..."
    )

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Analyze Resume", use_container_width=True):
    if resume_text.strip() == "" or job_text.strip() == "":
        st.warning("Please provide both a resume and a job description.")
    else:
        with st.spinner("Analyzing your resume..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert career coach and resume reviewer. Always respond in exactly the format requested with clear section headers."
                    },
                    {
                        "role": "user",
                        "content": f"""
Analyze this resume against the job description. Respond in exactly this format:

SCORE: [number out of 10]
SCORE_REASON: [one sentence explanation]

STRENGTHS:
- [strength 1]
- [strength 2]
- [strength 3]

GAPS:
- [gap 1]
- [gap 2]
- [gap 3]

QUICK_FIXES:
- [fix 1]
- [fix 2]
- [fix 3]

Resume:
{resume_text}

Job Description:
{job_text}
"""
                    }
                ]
            )

        raw = response.choices[0].message.content
        lines = raw.split("\n")

        score = ""
        score_reason = ""
        strengths = []
        gaps = []
        fixes = []
        current = None

        for line in lines:
            line = line.strip()
            if line.startswith("SCORE:"):
                score = line.replace("SCORE:", "").strip()
            elif line.startswith("SCORE_REASON:"):
                score_reason = line.replace("SCORE_REASON:", "").strip()
            elif line.startswith("STRENGTHS:"):
                current = "strengths"
            elif line.startswith("GAPS:"):
                current = "gaps"
            elif line.startswith("QUICK_FIXES:"):
                current = "fixes"
            elif line.startswith("-"):
                item = line[1:].strip()
                if current == "strengths":
                    strengths.append(item)
                elif current == "gaps":
                    gaps.append(item)
                elif current == "fixes":
                    fixes.append(item)

        st.markdown("<br>", unsafe_allow_html=True)

        score_col, rest_col = st.columns([1, 3], gap="large")

        with score_col:
            st.markdown(f"""
            <div class="score-card">
                <div class="score-number">{score}<span style="font-size:1.5rem;color:#8b92b8">/10</span></div>
                <div class="score-label">Match Score</div>
                <div style="font-size:0.8rem;color:#8b92b8;margin-top:0.8rem">{score_reason}</div>
            </div>
            """, unsafe_allow_html=True)

        with rest_col:
            st.markdown(f"""
            <div class="section-card">
                <div class="card-title strength-title">✅ Strengths</div>
                {"".join(f"<p style='color:#c0c4e0;margin:0.4rem 0'>• {s}</p>" for s in strengths)}
            </div>
            <div class="section-card">
                <div class="card-title gap-title">❌ Gaps</div>
                {"".join(f"<p style='color:#c0c4e0;margin:0.4rem 0'>• {g}</p>" for g in gaps)}
            </div>
            <div class="section-card">
                <div class="card-title fix-title">⚡ Quick Fixes</div>
                {"".join(f"<p style='color:#c0c4e0;margin:0.4rem 0'>• {f}</p>" for f in fixes)}
            </div>
            """, unsafe_allow_html=True)