import streamlit as st
import io
import time
from utils.extractor import extract_text_from_pdf
from utils.analyzer import analyze_resume, extract_skills
from samples.sample_data import SAMPLE_JOB_DESCRIPTIONS

# Set page configuration
st.set_page_config(
    page_title="HireSense AI - Intelligent Resume Analyzer & ATS Scorer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.3);
    }
    
    .main-header h1 {
        color: #FFFFFF;
        font-weight: 800;
        font-size: 2.4rem;
        margin-bottom: 0.4rem;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        color: #C7D2FE;
        font-size: 1.05rem;
        max-width: 800px;
        margin: 0;
    }
    
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.4rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    
    .metric-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        line-height: 1.1;
    }
    
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-top: 0.4rem;
    }
    
    .score-badge {
        display: inline-block;
        padding: 0.35rem 1rem;
        border-radius: 9999px;
        font-size: 0.9rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }
    
    .badge-match {
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
        padding: 0.35rem 0.75rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem 0.25rem;
    }
    
    .badge-missing {
        background-color: #FEF2F2;
        color: #991B1B;
        border: 1px solid #FECACA;
        padding: 0.35rem 0.75rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem 0.25rem;
    }
    
    .badge-bonus {
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
        padding: 0.35rem 0.75rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem 0.25rem;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .recommendation-box {
        background-color: #F8FAFC;
        border-left: 4px solid #4F46E5;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400&auto=format&fit=crop&q=60", use_container_width=True)
    st.title("🎯 HireSense AI")
    st.caption("AI-Powered Resume & ATS Compatibility Analyzer")
    
    st.markdown("---")
    st.markdown("### 📌 How It Works")
    st.markdown("""
    1. **Upload Resume**: Upload candidate resume in **PDF** format.
    2. **Job Description**: Paste or choose a target role description.
    3. **AI Analysis**: Computes **TF-IDF & Cosine Similarity** + categorizes matching & missing skills.
    4. **ATS Insights**: Receive instant compatibility rating & optimization tips.
    """)
    
    st.markdown("---")
    st.markdown("### 🧪 Quick Test Mode")
    st.info("No resume PDF at hand? Use one of our pre-generated sample resumes below!")
    
    sample_choice = st.selectbox(
        "Choose sample resume to download/inspect:",
        ["None", "Senior Python Full Stack Resume", "Data Scientist & AI Engineer Resume"]
    )
    
    if sample_choice == "Senior Python Full Stack Resume":
        with open("samples/sample_resume_python_dev.pdf", "rb") as f:
            st.download_button(
                label="📥 Download Python Dev Resume (PDF)",
                data=f.read(),
                file_name="sample_resume_python_dev.pdf",
                mime="application/pdf"
            )
    elif sample_choice == "Data Scientist & AI Engineer Resume":
        with open("samples/sample_resume_data_scientist.pdf", "rb") as f:
            st.download_button(
                label="📥 Download Data Scientist Resume (PDF)",
                data=f.read(),
                file_name="sample_resume_data_scientist.pdf",
                mime="application/pdf"
            )

    st.markdown("---")
    st.caption("HireSense AI v1.0 • Built with Streamlit, scikit-learn & pypdf")

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🎯 HireSense AI — Resume Analyzer</h1>
    <p>Analyze resume fit against specific job descriptions, identify critical skill gaps, and compute ATS compatibility using Machine Learning text similarity.</p>
</div>
""", unsafe_allow_html=True)

# Main Grid: Inputs
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-title">📄 Step 1: Upload Resume (PDF)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload candidate resume in PDF format."
    )
    
    resume_text = ""
    page_count = 0
    if uploaded_file is not None:
        try:
            with st.spinner("Extracting text from PDF..."):
                resume_text, page_count = extract_text_from_pdf(uploaded_file)
            
            if resume_text:
                st.success(f"✅ Successfully extracted text from **{uploaded_file.name}** ({page_count} page{'s' if page_count > 1 else ''}, {len(resume_text):,} characters).")
                with st.expander("👁️ Preview Extracted Resume Text"):
                    st.text_area("Extracted Text", resume_text, height=220, disabled=True)
            else:
                st.warning("⚠️ The uploaded PDF seems empty or contains only scanned images without extractable text.")
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")

with col_right:
    st.markdown('<div class="section-title">💼 Step 2: Job Description</div>', unsafe_allow_html=True)
    
    preset_col, clear_col = st.columns([3, 1])
    with preset_col:
        preset_jd = st.selectbox(
            "Load a sample Job Description (Optional):",
            ["Custom (Paste your own)"] + list(SAMPLE_JOB_DESCRIPTIONS.keys())
        )
    
    initial_jd_text = ""
    if preset_jd != "Custom (Paste your own)":
        initial_jd_text = SAMPLE_JOB_DESCRIPTIONS[preset_jd]
        
    job_description = st.text_area(
        "Paste the Job Description (JD) here:",
        value=initial_jd_text,
        height=280,
        placeholder="Paste role requirements, required skills, responsibilities..."
    )

# Analyze Button
st.markdown("<br>", unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    analyze_clicked = st.button("✨ Analyze Compatibility & Skills", use_container_width=True, type="primary")

# Execution & Results
if analyze_clicked:
    if not resume_text:
        st.error("⚠️ Please upload a valid PDF resume first.")
    elif not job_description or len(job_description.strip()) < 30:
        st.error("⚠️ Please provide a detailed Job Description (minimum 30 characters).")
    else:
        with st.spinner("🔍 Analyzing resume with TF-IDF Vectorization and Skill Extraction..."):
            time.sleep(0.5) # Smooth visual feedback
            results = analyze_resume(resume_text, job_description)

        st.markdown("---")
        st.markdown("## 📊 Analysis Results & Compatibility")
        
        # Metric Cards Row
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: {results['rating_color']};">{results['overall_score']}%</div>
                <div class="metric-label">ATS Compatibility</div>
                <div class="score-badge" style="background-color: {results['rating_color']}20; color: {results['rating_color']};">
                    {results['rating']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: #4F46E5;">{results['skill_match_percentage']}%</div>
                <div class="metric-label">Skill Match Rate</div>
                <div class="score-badge" style="background-color: #EEF2FF; color: #4338CA;">
                    {len(results['matching_skills'])} of {results['total_jd_skills_count']} Required
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: #0284C7;">{results['tfidf_score']}%</div>
                <div class="metric-label">Semantic Similarity</div>
                <div class="score-badge" style="background-color: #F0F9FF; color: #0369A1;">
                    TF-IDF Cosine
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-val" style="color: #059669;">{results['total_resume_skills_count']}</div>
                <div class="metric-label">Total Resume Skills</div>
                <div class="score-badge" style="background-color: #ECFDF5; color: #065F46;">
                    Detected in Profile
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"💡 **Evaluation Summary:** {results['rating_desc']}")
        
        # Skill Breakdown Columns
        s_col1, s_col2, s_col3 = st.columns(3, gap="medium")
        
        with s_col1:
            st.markdown(f"### 🟢 Matching Skills ({len(results['matching_skills'])})")
            st.caption("Skills found in both the resume and the job description.")
            if results['matching_skills']:
                badges_html = "".join([f'<span class="badge-match">✓ {skill}</span>' for skill in results['matching_skills']])
                st.markdown(f'<div style="line-height: 2;">{badges_html}</div>', unsafe_allow_html=True)
            else:
                st.warning("No direct matching skills detected.")
                
        with s_col2:
            st.markdown(f"### 🔴 Missing Skills ({len(results['missing_skills'])})")
            st.caption("Key job requirements absent from candidate resume.")
            if results['missing_skills']:
                badges_html = "".join([f'<span class="badge-missing">✕ {skill}</span>' for skill in results['missing_skills']])
                st.markdown(f'<div style="line-height: 2;">{badges_html}</div>', unsafe_allow_html=True)
            else:
                st.success("🎉 Outstanding! No critical skills missing from JD.")
                
        with s_col3:
            st.markdown(f"### 🔵 Bonus Profile Skills ({len(results['bonus_skills'])})")
            st.caption("Additional relevant strengths present in the resume.")
            if results['bonus_skills']:
                badges_html = "".join([f'<span class="badge-bonus">+ {skill}</span>' for skill in results['bonus_skills']])
                st.markdown(f'<div style="line-height: 2;">{badges_html}</div>', unsafe_allow_html=True)
            else:
                st.write("No additional standalone skills.")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recommendations & Actionable Insights
        st.markdown("### 💡 ATS Optimization & Recommendations")
        for rec in results['recommendations']:
            st.markdown(f"""
            <div class="recommendation-box">
                {rec}
            </div>
            """, unsafe_allow_html=True)
            
        # Downloadable Summary Report
        report_content = f"""=======================================================
HIRESENSE AI — RESUME ANALYSIS REPORT
=======================================================
Overall ATS Compatibility Score: {results['overall_score']}% ({results['rating']})
Skill Match Rate: {results['skill_match_percentage']}% ({len(results['matching_skills'])} of {results['total_jd_skills_count']})
TF-IDF Semantic Similarity: {results['tfidf_score']}%
Total Resume Skills Identified: {results['total_resume_skills_count']}

-------------------------------------------------------
MATCHING SKILLS ({len(results['matching_skills'])}):
{', '.join(results['matching_skills']) if results['matching_skills'] else 'None'}

-------------------------------------------------------
MISSING SKILLS ({len(results['missing_skills'])}):
{', '.join(results['missing_skills']) if results['missing_skills'] else 'None'}

-------------------------------------------------------
ADDITIONAL CANDIDATE SKILLS:
{', '.join(results['bonus_skills']) if results['bonus_skills'] else 'None'}

-------------------------------------------------------
ACTIONABLE RECOMMENDATIONS:
"""
        for idx, rec in enumerate(results['recommendations'], 1):
            report_content += f"{idx}. {rec}\n"
            
        report_content += "\nGenerated by HireSense AI\n"

        st.download_button(
            label="📥 Download Analysis Report (.txt)",
            data=report_content,
            file_name="HireSense_AI_Resume_Report.txt",
            mime="text/plain"
        )
