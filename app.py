"""
AI Resume Reviewer - Streamlit Application
Run with: streamlit run app.py
"""
 
import streamlit as st
from utils import extract_text_from_pdf, validate_resume_text
from ai_engine import analyze_resume


def generate_report_text(result: dict) -> str:
    """Generate a plain-text report from analysis results."""
    lines = []
    lines.append("=" * 50)
    lines.append("AI RESUME ANALYSIS REPORT")
    lines.append("=" * 50)
    lines.append(f"\nMatch Score: {result['match_score']}/100")
    if "score_explanation" in result:
        lines.append(f"Explanation: {result['score_explanation']}")
    lines.append(f"\n--- STRENGTHS ---")
    for s in result["strengths"]:
        lines.append(f"  + {s}")
    lines.append(f"\n--- IMPROVEMENTS ---")
    for imp in result["improvements"]:
        lines.append(f"  - {imp}")
    lines.append(f"\n--- MISSING KEYWORDS ---")
    for kw in result["missing_keywords"]:
        lines.append(f"  * {kw}")
    lines.append(f"\n--- REWRITTEN SUMMARY ---")
    lines.append(result["rewritten_summary"])
    return "\n".join(lines)

# ─── Example Data Constants (for "Try Example" feature) ───

EXAMPLE_RESUME = """
PRIYA SHARMA
Mumbai, Maharashtra | priya.sharma@email.com | +91-98765-43210
LinkedIn: linkedin.com/in/priyasharma | GitHub: github.com/priyasharma

PROFESSIONAL SUMMARY
Full-stack developer with 3 years of experience building web
applications using Python, JavaScript, and cloud services. Led a
team of 4 to deliver an e-commerce platform serving 10,000+ users.
Passionate about clean code, test-driven development, and DevOps.

TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, SQL
Frameworks: Django, Flask, React, Next.js
Databases: PostgreSQL, MongoDB, Redis
Cloud & DevOps: AWS (EC2, S3, Lambda), Docker, GitHub Actions
Tools: Git, Jira, Figma, Postman

WORK EXPERIENCE

Software Developer | TechNova Solutions, Mumbai
June 2022 - Present
- Built RESTful APIs in Django serving 50,000+ daily requests
  with 99.9% uptime
- Migrated monolith to microservices, reducing deployment time
  by 60%
- Implemented CI/CD pipeline with GitHub Actions, cutting
  release cycles from 2 weeks to 2 days
- Mentored 2 junior developers through code reviews and pair
  programming sessions

Junior Developer | WebCraft Studios, Pune
January 2021 - May 2022
- Developed responsive front-end components using React and
  Tailwind CSS
- Integrated Stripe payment gateway processing INR 5M+
  monthly transactions
- Wrote unit tests achieving 85% code coverage across the
  application

EDUCATION
B.Tech in Computer Science | VIT University, Vellore
Graduated: May 2020 | CGPA: 8.6/10

CERTIFICATIONS
- AWS Certified Cloud Practitioner (2023)
- Meta Front-End Developer Professional Certificate (2022)

PROJECTS
ShopEasy - E-commerce Platform
- Full-stack Django + React app with real-time inventory
  tracking and Razorpay integration
- Deployed on AWS with auto-scaling, handling 500+ concurrent
  users
"""

EXAMPLE_JOB_DESCRIPTION = """
Senior Full-Stack Developer - FinTech Startup

About the Role:
We are looking for a Senior Full-Stack Developer to join our
growing engineering team. You will design and build scalable
web applications for our digital payments platform serving
millions of users across India.

Requirements:
- 3+ years of experience in full-stack web development
- Strong proficiency in Python (Django/FastAPI) and
  JavaScript (React/Next.js)
- Experience with PostgreSQL, Redis, and message queues
  (RabbitMQ/Kafka)
- Hands-on experience with AWS or GCP cloud services
- Familiarity with Docker, Kubernetes, and CI/CD pipelines
- Experience with payment gateway integrations (Razorpay,
  Stripe, UPI)
- Strong understanding of RESTful API design and
  microservices architecture

Nice to Have:
- Experience with FastAPI or GraphQL
- Knowledge of Kafka or RabbitMQ for event-driven
  architecture
- Familiarity with Kubernetes orchestration
- Contributions to open-source projects

What We Offer:
- Competitive salary: INR 18-28 LPA
- ESOPs and performance bonuses
- Flexible remote work policy
- Learning budget of INR 50,000/year
"""
 
# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Reviewer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# --- Custom CSS for better styling ---
st.markdown("""
<style>
.score-high { color: #27ae60; font-size: 48px; font-weight: bold; }
.score-mid { color: #f39c12; font-size: 48px; font-weight: bold; }
.score-low { color: #e74c3c; font-size: 48px; font-weight: bold; }
@media (max-width: 768px) {
    button[kind="header"],
    [data-testid="collapsedControl"] {
        width: 48px  !important;
        height: 48px !important;
        background-color: #ff4b4b !important;
        border-radius: 50% !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25) !important;
    }
}
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        min-width: 85vw !important;
        max-width: 85vw !important;
    }
}
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
if "example_mode" not in st.session_state:
    st.session_state.example_mode = False
 
# --- Sidebar: Inputs ---
with st.sidebar:
    if st.button("🎯 Try with Example Data", use_container_width=True):
        st.session_state.resume_text = EXAMPLE_RESUME
        st.session_state.example_mode = True
        st.rerun()

    st.divider()

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

            # Show errors (red, blocking)
            for err in validation.get("errors", []):
                st.error(err)

            # If errors exist, block analysis
            if validation.get("errors"):
                st.session_state.resume_text = None

            # Show warnings (yellow, non-blocking)
            for warning in validation["warnings"]:
                st.warning(warning)
        else:
            st.error(
                "❌ Could not extract any text from this PDF. "
                "It may be a scanned (image-only) file. "
                "Please upload a text-based PDF instead."
            )
    # Show example mode indicator  ← NEW BLOCK
    elif st.session_state.get("example_mode"):
        st.info("📋 Using example resume data")

    st.divider()
 
    # Job description input  ← UPDATED with example pre-fill
    job_description = st.text_area(
        "Paste the job description",
        value=EXAMPLE_JOB_DESCRIPTION if st.session_state.get("example_mode") else "",
        height=300,
        placeholder="Paste the full job description here..."
    )

 
    st.divider()

    # Analyze button
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
        st.error(f"⚠️ Analysis failed: {result['error']}")

        # Show raw AI response when JSON parsing failed
        if "raw" in result:
            st.markdown("---")
            st.markdown(
                "**Sorry — the AI returned a response we couldn't "
                "parse.** Here is the raw output for reference:"
            )
            with st.expander("Show raw AI response", expanded=False):
                st.code(result["raw"], language="json")

        st.info(
            "💡 **Tip:** Click **Analyze Resume** again to retry. "
            "If the problem persists, try shortening your resume "
            "or simplifying the job description."
        )
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
        input_tok = result.get("input_tokens", 0)
        output_tok = result.get("output_tokens", 0)
        total_tok = result.get("total_tokens", 0)
        input_cost = result.get("input_cost", 0)
        output_cost = result.get("output_cost", 0)
        total_cost = result.get("total_cost", 0)

        st.caption(
            f"**Model:** {result.get('model', 'N/A')}  \n"
            f"**Tokens:** {input_tok:,} input + {output_tok:,} output "
            f"= {total_tok:,} total  \n"
            f"**Est. cost:** ${input_cost:.4f} (input) + "
            f"${output_cost:.4f} (output) = **${total_cost:.4f}**"
        )
        # Download report
        report_text = generate_report_text(result)
        st.download_button(
            label="📥 Download Report",
            data=report_text,
            file_name="resume_analysis_report.txt",
            mime="text/plain",
            use_container_width=True
    )
else:
    st.markdown("### 👈 Upload a resume and paste a job description to get started")
    st.markdown("")
    st.markdown("**How it works:**")
    st.markdown("1. Upload your resume as a PDF")
    st.markdown("2. Paste the target job description")
    st.markdown("3. Click Analyze — get a match score, missing keywords, strengths, improvements, and a rewritten summary")

    
