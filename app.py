import streamlit as st
from src.helper import extract_text_from_pdf
from src.helper import ask_groq
from src.job_api import fetch_linkedin_jobs
from src.job_api import fetch_naukri_jobs   
import time

# Helper function to truncate description
def truncate_description(text, max_chars=400):
    """Truncate description to max characters with ellipsis"""
    if not text or len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(' ', 1)[0] + "..."

def get_apply_url(job_url, job_title, company, platform="linkedin"):
    """Generate a safe apply URL with fallback to job search"""
    if job_url and job_url not in ['#', '', None]:
        return job_url
    
    # Fallback: Search on LinkedIn or Naukri
    if platform.lower() == "linkedin":
        search_query = f"{job_title} {company}".replace(" ", "%20")
        return f"https://www.linkedin.com/jobs/search/?keywords={search_query}"
    else:  # Naukri
        search_query = f"{job_title}".replace(" ", "%20")
        return f"https://www.naukri.com/jobs-{search_query}"

# Page Configuration
st.set_page_config(
    page_title="AI Job Recommender",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS for Modern UI with Advanced Animations
st.markdown("""
    <style>
        /* ===== ANIMATIONS ===== */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.6;
            }
        }
        
        @keyframes glow {
            0%, 100% {
                box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
            }
            50% {
                box-shadow: 0 0 40px rgba(16, 185, 129, 0.6);
            }
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-10px);
            }
        }
        
        @keyframes gradientShift {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        
        /* ===== GLOBAL STYLES ===== */
        * {
            margin: 0;
            padding: 0;
        }
        
        body, .main {
            background: linear-gradient(135deg, #0a0e27 0%, #1f1e3f 50%, #16213e 100%);
            min-height: 100vh;
        }
        
        /* ===== HEADER CONTAINER ===== */
        .header-container {
            animation: fadeInDown 0.9s ease-out;
            background: linear-gradient(135deg, #10b981 0%, #047857 50%, #6ee7b7 100%);
            background-size: 200% 200%;
            animation: fadeInDown 0.9s ease-out, gradientShift 15s ease infinite;
            padding: 50px 30px;
            border-radius: 20px;
            margin-bottom: 40px;
            box-shadow: 0 20px 60px rgba(16, 185, 129, 0.3);
            text-align: center;
            border: 2px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .header-container::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: float 6s ease-in-out infinite;
        }
        
        .header-title {
            font-size: 3.5em;
            font-weight: 900;
            color: white;
            margin: 10px 0;
            text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            animation: fadeInDown 1.2s ease-out;
            position: relative;
            z-index: 1;
        }
        
        .header-subtitle {
            font-size: 1.2em;
            color: rgba(255, 255, 255, 0.95);
            margin-top: 15px;
            animation: slideInUp 1.3s ease-out;
            position: relative;
            z-index: 1;
        }
        
        /* ===== UPLOAD SECTION ===== */
        .upload-container {
            animation: slideInUp 1.1s ease-out;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(4, 120, 87, 0.08) 100%);
            padding: 30px;
            border-radius: 15px;
            border: 2px solid rgba(16, 185, 129, 0.4);
            margin-bottom: 40px;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            backdrop-filter: blur(10px);
        }
        
        .upload-container:hover {
            border-color: rgba(16, 185, 129, 0.8);
            box-shadow: 0 10px 40px rgba(16, 185, 129, 0.2);
            transform: translateY(-5px);
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(4, 120, 87, 0.15) 100%);
        }
        
        .upload-title {
            font-size: 1.25em;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 15px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* ===== RESULT BOX ===== */
        .result-box {
            animation: slideInUp 0.7s ease-out;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(4, 120, 87, 0.08) 100%);
            padding: 30px;
            border-radius: 15px;
            border: 1px solid rgba(16, 185, 129, 0.2);
            margin-bottom: 25px;
            backdrop-filter: blur(15px);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        
        .result-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
            transition: left 0.5s;
        }
        
        .result-box:hover::before {
            left: 100%;
        }
        
        .result-box:hover {
            border-color: rgba(16, 185, 129, 0.5);
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(16, 185, 129, 0.15);
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(4, 120, 87, 0.12) 100%);
        }
        
        .result-title {
            font-size: 1.4em;
            font-weight: 800;
            background: linear-gradient(135deg, #10b981, #047857);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .result-content {
            color: rgba(255, 255, 255, 0.85);
            line-height: 1.9;
            font-size: 0.98em;
            letter-spacing: 0.3px;
        }
        
        .result-badge {
            display: inline-block;
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            margin-top: 15px;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        
        /* ===== JOB CARD ===== */
        .job-card {
            animation: slideInUp 0.8s ease-out;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(4, 120, 87, 0.06) 100%);
            padding: 28px;
            border-radius: 15px;
            border-left: 4px solid #10b981;
            margin-bottom: 25px;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        .job-card::after {
            content: '';
            position: absolute;
            top: 0;
            right: -100%;
            width: 200%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
            transition: right 0.6s;
        }
        
        .job-card:hover {
            transform: translateX(15px) translateY(-8px);
            border-left-color: #047857;
            box-shadow: 0 20px 60px rgba(16, 185, 129, 0.2);
            border-left-width: 6px;
        }
        
        .job-card:hover::after {
            right: 100%;
        }
        
        .job-title {
            font-size: 1.4em;
            font-weight: 900;
            background: linear-gradient(135deg, #10b981, #047857);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .job-meta {
            font-size: 0.95em;
            color: rgba(255, 255, 255, 0.75);
            margin-bottom: 18px;
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(16, 185, 129, 0.1);
        }
        
        .job-meta span {
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.3s ease;
        }
        
        .job-meta span:hover {
            color: rgba(255, 255, 255, 0.95);
        }
        
        .job-description {
            color: rgba(255, 255, 255, 0.8);
            line-height: 1.8;
            margin-bottom: 20px;
            font-size: 0.96em;
            letter-spacing: 0.2px;
        }
        
        .apply-btn {
            display: inline-block;
            background: linear-gradient(135deg, #10b981 0%, #047857 100%);
            color: white;
            padding: 12px 28px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1em;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            box-shadow: 0 5px 20px rgba(16, 185, 129, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .apply-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.2);
            transition: left 0.3s;
        }
        
        .apply-btn:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 35px rgba(16, 185, 129, 0.5);
            text-decoration: none;
            color: white;
        }
        
        .apply-btn:hover::before {
            left: 100%;
        }
        
        .apply-btn:active {
            transform: translateY(-1px);
        }
        
        /* ===== BUTTON STYLING ===== */
        .stButton > button {
            background: linear-gradient(135deg, #10b981 0%, #047857 100%);
            color: white;
            border: none;
            padding: 15px 45px;
            font-size: 1.1em;
            font-weight: 800;
            border-radius: 10px;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.35);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .stButton > button:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(16, 185, 129, 0.5);
        }
        
        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .stButton > button:active {
            transform: translateY(-2px);
        }
        
        /* ===== SECTION HEADER ===== */
        .section-header {
            font-size: 2em;
            font-weight: 900;
            color: white;
            margin: 50px 0 30px 0;
            padding-bottom: 20px;
            border-bottom: 3px solid;
            border-image: linear-gradient(90deg, #10b981, #047857) 1;
            display: flex;
            align-items: center;
            gap: 12px;
            animation: slideInUp 0.7s ease-out;
            position: relative;
        }
        
        .section-header::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.3), transparent);
        }
        
        /* ===== SUCCESS MESSAGE ===== */
        .stSuccess {
            animation: slideInUp 0.5s ease-out;
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.2) 0%, rgba(45, 135, 45, 0.1) 100%) !important;
            border-left: 4px solid #4caf50 !important;
            border-radius: 10px !important;
            padding: 15px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* ===== NO RESULTS ===== */
        .no-results {
            text-align: center;
            padding: 60px 30px;
            color: rgba(255, 255, 255, 0.6);
            font-size: 1.2em;
            animation: slideInUp 0.6s ease-out;
        }
        
        /* ===== STATS CONTAINER ===== */
        .stats-container {
            display: flex;
            gap: 20px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .stat-box {
            flex: 1;
            min-width: 150px;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(4, 120, 87, 0.08) 100%);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid rgba(16, 185, 129, 0.2);
            text-align: center;
            animation: slideInUp 0.8s ease-out;
            transition: all 0.3s ease;
        }
        
        .stat-box:hover {
            transform: translateY(-5px);
            border-color: rgba(16, 185, 129, 0.5);
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(4, 120, 87, 0.12) 100%);
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: 900;
            background: linear-gradient(135deg, #10b981, #047857);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-label {
            color: rgba(255, 255, 255, 0.7);
            margin-top: 8px;
            font-weight: 600;
            font-size: 0.95em;
        }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .header-title {
                font-size: 2.2em;
            }
            .header-subtitle {
                font-size: 1em;
            }
            .job-card {
                padding: 20px;
            }
            .section-header {
                font-size: 1.5em;
            }
            .stats-container {
                flex-direction: column;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🚀 AI Job Recommender</h1>
        <p class="header-subtitle">Get personalized job recommendations based on your resume using AI</p>
    </div>
""", unsafe_allow_html=True)

# File Upload Section
st.markdown("""
    <div class="upload-container">
        <p style="font-size: 1.1em; color: rgba(255, 255, 255, 0.8); margin-bottom: 15px;"><strong>📄 Step 1: Upload Your Resume</strong></p>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

if uploaded_file:
    # Extract Text
    with st.spinner("🔍 Extracting text from resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        time.sleep(0.5)

    # Summarize
    with st.spinner("📝 Analyzing your resume..."):
        summary = ask_groq(f"Summarize the following resume in a concise manner, highlighting key skills , education and experience:\n\n{resume_text}", max_tokens=300)
        time.sleep(0.5)

    # Skill Gaps
    with st.spinner("🎯 Identifying skill gaps..."):
        gaps = ask_groq(f"Based on the following resume summary, identify any skill gaps that may exist for a software engineering role:\n\n{summary}", max_tokens=300)
        time.sleep(0.5)

    # Roadmap
    with st.spinner("🗺️ Creating your career roadmap..."):
        road_map = ask_groq(f"Based on the following resume summary and identified skill gaps, create a future roadmap for the candidate to become a successful software engineer:\n\nResume Summary:\n{summary}\n\nIdentified Skill Gaps:\n{gaps}", max_tokens=300)
        time.sleep(0.5)

# Display Results
    st.markdown("<h2 class='section-header'>📊 Your Analysis Results</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='result-box'>
                <div class='result-title'>✨ Resume Summary</div>
                <div class='result-content'>{summary}</div>
                <span class='result-badge'>Summary Ready</span>
            </div>
        """.format(summary=summary), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='result-box'>
                <div class='result-title'>⚠️ Skill Gaps</div>
                <div class='result-content'>{gaps}</div>
                <span class='result-badge'>Areas to Improve</span>
            </div>
        """.format(gaps=gaps), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='result-box'>
                <div class='result-title'>🎓 Learning Path</div>
                <div class='result-content'>{road_map}</div>
                <span class='result-badge'>Career Roadmap</span>
            </div>
        """.format(road_map=road_map), unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Job Recommendations Button
    st.markdown("<h2 class='section-header'>🎯 Ready to Explore Opportunities?</h2>", unsafe_allow_html=True)
    
    col_button = st.columns([1, 2, 1])
    with col_button[1]:
        get_jobs = st.button("🚀 Get Job Recommendations", use_container_width=True, key="get_jobs_btn")
    
    if get_jobs:
        with st.spinner("🤖 Extracting keywords from your resume..."):
            keywords = ask_groq(f"Based on the following resume summary, identify the top 5 keywords that can be used to search for relevant searching jobs .Give a comma -seperated list only, no explaination.:\n\nSummary: {summary}", max_tokens=100)
            search_keywords = keywords.replace("\n","").strip()
            time.sleep(0.5)

        st.success(f"✅ Keywords extracted: **{search_keywords}**")

        with st.spinner("🌐 Fetching job recommendations from LinkedIn and Naukri..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords, row=60)
            naukri_jobs = fetch_naukri_jobs(search_keywords, row=60)
            time.sleep(1)
        
        # Display Stats
        st.markdown("<h2 class='section-header'>📈 Job Search Statistics</h2>", unsafe_allow_html=True)
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            st.markdown(f"""
                <div class='stat-box'>
                    <div class='stat-number'>{len(linkedin_jobs)}</div>
                    <div class='stat-label'>LinkedIn Jobs</div>
                </div>
            """, unsafe_allow_html=True)
        
        with stats_col2:
            st.markdown(f"""
                <div class='stat-box'>
                    <div class='stat-number'>{len(naukri_jobs)}</div>
                    <div class='stat-label'>Naukri Jobs</div>
                </div>
            """, unsafe_allow_html=True)
        
        with stats_col3:
            total_jobs = len(linkedin_jobs) + len(naukri_jobs)
            st.markdown(f"""
                <div class='stat-box'>
                    <div class='stat-number'>{total_jobs}</div>
                    <div class='stat-label'>Total Opportunities</div>
                </div>
            """, unsafe_allow_html=True)

        # LinkedIn Jobs
        if linkedin_jobs:
            st.markdown("<h2 class='section-header'>💼 LinkedIn Opportunities</h2>", unsafe_allow_html=True)
            
            for idx, job in enumerate(linkedin_jobs):
                description = truncate_description(job.get('description', 'No description available'), 400)
                apply_url = get_apply_url(job.get('url', '#'), job.get('title', 'Job'), job.get('company', 'Company'), "linkedin")
                st.markdown(f"""
                    <div class="job-card">
                        <div class="job-title">💼 {job.get('title', 'N/A')}</div>
                        <div class="job-meta">
                            <span>🏢 {job.get('company', 'N/A')}</span>
                            <span>📍 {job.get('location', 'N/A')}</span>
                            <span>#{idx + 1}</span>
                        </div>
                        <div class="job-description">{description}</div>
                        <a href="{apply_url}" target="_blank" rel="noopener noreferrer" class="apply-btn" onclick="window.open('{apply_url}', '_blank'); return false;">Apply Now →</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <h2 class='section-header'>💼 LinkedIn Opportunities</h2>
                <div class="no-results">
                    <p>😔 No LinkedIn jobs found for these keywords</p>
                    <p style='font-size: 0.9em; margin-top: 10px;'>Try different keywords or explore Naukri below</p>
                </div>
            """, unsafe_allow_html=True)

        # Naukri Jobs
        if naukri_jobs:
            st.markdown("<h2 class='section-header'>🎯 Naukri Opportunities</h2>", unsafe_allow_html=True)
            
            for idx, job in enumerate(naukri_jobs):
                description = truncate_description(job.get('description', 'No description available'), 400)
                apply_url = get_apply_url(job.get('url', '#'), job.get('title', 'Job'), job.get('company', 'Company'), "naukri")
                st.markdown(f"""
                    <div class="job-card">
                        <div class="job-title">🚀 {job.get('title', 'N/A')}</div>
                        <div class="job-meta">
                            <span>🏢 {job.get('company', 'N/A')}</span>
                            <span>📍 {job.get('location', 'N/A')}</span>
                            <span>#{idx + 1}</span>
                        </div>
                        <div class="job-description">{description}</div>
                        <a href="{apply_url}" target="_blank" rel="noopener noreferrer" class="apply-btn" onclick="window.open('{apply_url}', '_blank'); return false;">Apply Now →</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <h2 class='section-header'>🎯 Naukri Opportunities</h2>
                <div class="no-results">
                    <p>😔 No Naukri jobs found for these keywords</p>
                    <p style='font-size: 0.9em; margin-top: 10px;'>Check LinkedIn jobs above or try different keywords</p>
                </div>
            """, unsafe_allow_html=True)