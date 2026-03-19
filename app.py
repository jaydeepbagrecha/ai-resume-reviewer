"""
AI Resume Reviewer - Streamlit Application
Run with: streamlit run app.py
"""
 
import streamlit as st
from utils import extract_text_from_pdf, validate_resume_text
from ai_engine import analyze_resume
 
# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="📄",
    layout="wide",
)
 
# --- Custom CSS for better styling ---
st.markdown("""
<style>
.score-high { color: #27ae60; font-size: 48px; font-weight: bold; }
.score-mid { color: #f39c12; font-size: 48px; font-weight: bold; }
.score-low { color: #e74c3c; font-size: 48px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)
 
# --- Header ---
st.title("📄 AI Resume Reviewer")
st.markdown("Upload your resume and paste a job description to get AI-powered feedback.")
st.divider()
 
# --- Initialize Session State ---
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
 
# --- Sidebar: Inputs ---
with st.sidebar:
    st.header("📤 Upload & Configure")
 
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)",
        type=["pdf"],
        help="Upload a PDF version of your resume"
    )
 
    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        resume_text = extract_text_from_pdf(uploaded_file)
        if resume_text:
            st.session_state.resume_text = resume_text
            validation = validate_resume_text(resume_text)
            st.info(f"📊 {validation['word_count']} words extracted")
            for warning in validation["warnings"]:
                st.warning(warning)
        else:
            st.error("❌ Could not extract text. Try a different PDF.")
 
    st.divider()
 
    job_description = st.text_area(
        "Paste the job description",
        height=300,
        placeholder="Paste the full job description here..."
    )
 
    st.divider()
 
    can_analyze = (
        st.session_state.resume_text is not None
        and len(job_description.strip()) > 50
    )
 
    if st.button("🔍 Analyze Resume", disabled=not can_analyze, use_container_width=True):
        with st.spinner("🤖 AI is analyzing your resume..."):
            result = analyze_resume(st.session_state.resume_text, job_description)
            st.session_state.analysis_result = result
 
    if not can_analyze:
        if st.session_state.resume_text is None:
            st.caption("⬆️ Upload a resume PDF to begin")
        elif len(job_description.strip()) <= 50:
            st.caption("✏️ Paste a job description (50+ characters)")
 
# --- Main Area: Results ---
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
 
    if "error" in result:
        st.error(f"Analysis failed: {result['error']}")
    else:
        col1, col2, col3 = st.columns([1, 1, 1])
 
        with col1:
            score = result["match_score"]
            if score >= 75:
                score_class = "score-high"
            elif score >= 50:
                score_class = "score-mid"
            else:
                score_class = "score-low"
            st.markdown(f'<p class="{score_class}">{score}/100</p>',
                        unsafe_allow_html=True)
            st.caption("Match Score")
 
        with col2:
            st.metric("Strengths Found", len(result["strengths"]))
 
        with col3:
            st.metric("Improvements", len(result["improvements"]))
 
        if "score_explanation" in result:
            st.info(result["score_explanation"])
 
        st.divider()
 
        tab1, tab2, tab3, tab4 = st.tabs([
            "💪 Strengths", "🔧 Improvements",
            "🔑 Missing Keywords", "✍️ Rewritten Summary"
        ])
 
        with tab1:
            for s in result["strengths"]:
                st.success(f"✅ {s}")
 
        with tab2:
            for imp in result["improvements"]:
                st.warning(f"💡 {imp}")
 
        with tab3:
            if result["missing_keywords"]:
                cols = st.columns(3)
                for i, kw in enumerate(result["missing_keywords"]):
                    with cols[i % 3]:
                        st.error(f"❌ {kw}")
            else:
                st.success("Great! No critical keywords missing.")
 
        with tab4:
            st.markdown("**Suggested professional summary tailored to this role:**")
            st.text_area(
                "Copy this summary",
                value=result["rewritten_summary"],
                height=150,
                label_visibility="collapsed"
            )
 
        st.divider()
        st.caption(
            f"Model: {result.get('model', 'N/A')} | "
            f"Tokens: {result.get('total_tokens', 'N/A')} | "
            f"Est. cost: ${result.get('total_tokens', 0) * 0.000005:.4f}"
        )
 
else:
    st.markdown("### 👈 Upload a resume and paste a job description to get started")
    st.markdown("")
    st.markdown("**How it works:**")
    st.markdown("1. Upload your resume as a PDF")
    st.markdown("2. Paste the target job description")
    st.markdown("3. Click Analyze — get a match score, missing keywords, strengths, improvements, and a rewritten summary")
