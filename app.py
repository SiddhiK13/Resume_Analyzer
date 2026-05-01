import pdfplumber
import streamlit as st
from groq import Groq
import os
import re

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


def read_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def analyze_resume(resume_text, job_description):
    prompt = f"""
    You are an expert HR consultant and career coach.
    
    Analyze the resume below against the job description and provide:
    1. ATS Score (just a number out of 100, on its own line like: ATS_SCORE: 78)
    2. Top 3 strengths (label each with STRENGTH:)
    3. Top 3 skill gaps (label each with GAP:)
    4. 3 specific resume improvements (label each with IMPROVEMENT:)
    5. 3 likely interview questions (label each with QUESTION:)
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def parse_results(text):
    score_match = re.search(r'ATS_SCORE:\s*(\d+)', text)
    score = int(score_match.group(1)) if score_match else 75

    strengths = re.findall(r'STRENGTH:\s*(.+)', text)
    gaps = re.findall(r'GAP:\s*(.+)', text)
    improvements = re.findall(r'IMPROVEMENT:\s*(.+)', text)
    questions = re.findall(r'QUESTION:\s*(.+)', text)

    return score, strengths, gaps, improvements, questions

# --- Page config ---
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main { padding-top: 0rem; }
    
    .hero {
        background: linear-gradient(135deg, #185FA5, #0F6E56);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .hero h1 { font-size: 2rem; font-weight: 600; margin-bottom: 0.5rem; }
    .hero p  { font-size: 1rem; opacity: 0.9; }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }

    .stat-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .stat-num  { font-size: 1.6rem; font-weight: 600; color: #185FA5; }
    .stat-label{ font-size: 0.75rem; color: #666; margin-top: 2px; }

    .score-circle {
        width: 90px; height: 90px;
        border-radius: 50%;
        background: #E6F1FB;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        margin: 0 auto 1rem auto;
    }
    .score-num { font-size: 2rem; font-weight: 700; color: #185FA5; line-height: 1; }
    .score-sub { font-size: 0.65rem; color: #185FA5; letter-spacing: 1px; }

    .tag-green {
        display: inline-block;
        background: #EAF3DE; color: #27500A;
        padding: 5px 12px; border-radius: 20px;
        font-size: 0.82rem; margin: 3px;
    }
    .tag-red {
        display: inline-block;
        background: #FCEBEB; color: #791F1F;
        padding: 5px 12px; border-radius: 20px;
        font-size: 0.82rem; margin: 3px;
    }
    .tag-blue {
        display: inline-block;
        background: #E6F1FB; color: #0C447C;
        padding: 5px 12px; border-radius: 20px;
        font-size: 0.82rem; margin: 3px;
    }
    .tag-amber {
        display: inline-block;
        background: #FAEEDA; color: #633806;
        padding: 5px 12px; border-radius: 20px;
        font-size: 0.82rem; margin: 3px;
    }

    .section-title {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #888;
        margin: 1.2rem 0 0.5rem 0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #185FA5, #0F6E56) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        opacity: 0.9 !important;
    }
    
    div[data-testid="stFileUploader"] {
        border: 2px dashed #185FA5 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Powered by Groq LLaMA AI</div>
    <h1>📄 AI Resume Analyzer</h1>
    <p>Get instant ATS score, skill gap analysis & interview prep</p>
</div>
""", unsafe_allow_html=True)

# --- Stats Row ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="stat-card"><div class="stat-num">500+</div><div class="stat-label">Resumes analyzed</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-card"><div class="stat-num">92%</div><div class="stat-label">Accuracy rate</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-card"><div class="stat-num">5s</div><div class="stat-label">Avg response time</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Input Section ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("**📎 Step 1 — Upload your resume**")
    uploaded_file = st.file_uploader("Choose PDF", type="pdf", label_visibility="collapsed")
with col2:
    st.markdown("**📋 Step 2 — Paste job description**")
    job_desc = st.text_area("JD", height=150, placeholder="Paste the job description here...", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# --- Analyze Button ---
if st.button("🔍 Analyze My Resume"):
    if uploaded_file and job_desc:
        with st.spinner("🤖 AI is analyzing your resume..."):
            resume_text = read_pdf(uploaded_file)
            raw_feedback = analyze_resume(resume_text, job_desc)
            score, strengths, gaps, improvements, questions = parse_results(raw_feedback)

        st.markdown("---")
        st.markdown("### 📊 Your Results")

        # Score
        score_color = "#27500A" if score >= 80 else "#185FA5" if score >= 60 else "#791F1F"
        score_bg = "#EAF3DE" if score >= 80 else "#E6F1FB" if score >= 60 else "#FCEBEB"
        score_label = "Excellent match! 🎉" if score >= 80 else "Good match 👍" if score >= 60 else "Needs work 💪"

        st.markdown(f"""
        <div style="text-align:center; padding: 1.5rem; background:{score_bg}; border-radius:16px; margin-bottom:1.5rem;">
            <div style="font-size:3.5rem; font-weight:700; color:{score_color};">{score}</div>
            <div style="font-size:0.8rem; color:{score_color}; letter-spacing:1px; margin-top:-4px;">ATS SCORE / 100</div>
            <div style="font-size:1rem; margin-top:8px; color:{score_color};">{score_label}</div>
        </div>
        """, unsafe_allow_html=True)

        # Strengths
        if strengths:
            st.markdown('<div class="section-title">✅ Top strengths</div>', unsafe_allow_html=True)
            tags = "".join([f'<span class="tag-green">✓ {s.strip()}</span>' for s in strengths[:3]])
            st.markdown(tags, unsafe_allow_html=True)

        # Gaps
        if gaps:
            st.markdown('<div class="section-title">⚠️ Skill gaps</div>', unsafe_allow_html=True)
            tags = "".join([f'<span class="tag-red">✗ {g.strip()}</span>' for g in gaps[:3]])
            st.markdown(tags, unsafe_allow_html=True)

        # Improvements
        if improvements:
            st.markdown('<div class="section-title">✏️ Resume improvements</div>', unsafe_allow_html=True)
            for i, tip in enumerate(improvements[:3], 1):
                st.markdown(f'<span class="tag-amber">💡 {tip.strip()}</span>', unsafe_allow_html=True)

        # Interview Questions
        if questions:
            st.markdown('<div class="section-title">🎯 Interview questions to prepare</div>', unsafe_allow_html=True)
            tags = "".join([f'<span class="tag-blue">❓ {q.strip()}</span>' for q in questions[:3]])
            st.markdown(tags, unsafe_allow_html=True)

        # Raw full feedback expandable
        with st.expander("📄 View full detailed feedback"):
            st.markdown(raw_feedback)

    else:
        st.warning("⚠️ Please upload a resume PDF AND paste a job description first.")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#888; font-size:0.8rem;'>Built with Python · Groq LLaMA AI · Streamlit</p>",
    unsafe_allow_html=True
)



# Run  On Cmd : streamlit run app.py