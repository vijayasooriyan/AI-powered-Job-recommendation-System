import streamlit as st
from src.helper import extract_text_from_pdf
from src.helper import ask_groq
from src.job_api import fetch_linkedin_jobs
from src.job_api import fetch_naukri_jobs   

st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("🧑🏽‍💻 AI Job Recommender")
st.markdown("Upload your resume and get personalized job recommendations based on your skills and experience using the power of AI.")

uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing your resume..."):
        summary = ask_groq(f"Summarize the following resume in a concise manner, highlighting key skills , education and experience:\n\n{resume_text}", max_tokens=500)

    with st.spinner("Finding skill gaps..."):
        gaps = ask_groq(f"Based on the following resume summary, identify any skill gaps that may exist for a software engineering role:\n\n{summary}", max_tokens=500)

    with st.spinner("Creating future roadmap..."):
        road_map = ask_groq(f"Based on the following resume summary and identified skill gaps, create a future roadmap for the candidate to become a successful software engineer:\n\nResume Summary:\n{summary}\n\nIdentified Skill Gaps:\n{summary}", max_tokens=500)

    #Display nicely formatted results
    st.header("Resume Summary")
    st.markdown(f"<div style='background-color:#080707 ; padding: 10px; border-radius: 5px;'>{summary}</div>", unsafe_allow_html=True)

    st.header("Identified Skill Gaps")
    st.markdown(f"<div style='background-color: #080707; padding: 10px; border-radius: 5px;'>{gaps}</div>", unsafe_allow_html=True)     

    
    st.header("Future Roadmap")
    st.markdown(f"<div style='background-color: #080707; padding: 10px; border-radius: 5px;'>{road_map}</div>", unsafe_allow_html=True)

    st.success("Analysis complete! Please review the results above and use them to guide your job search and career development.")

    if st.button("Get Job Recommendations"):
        with st.spinner("Fetching job recommendations"):
            keywords = ask_groq(f"Based on the following resume summary, identify the top 5 keywords that can be used to search for relevant searching jobs .Give a comma -seperated list only, no explaination.:\n\nSummary: {summary}", max_tokens=100)

            search_keywords = keywords.replace("\n","").strip()

        st.success(f"Extracted Job keywords: {search_keywords}")

        with st.spinner("Fetching job recommendations from LinkedIn and Naukri"):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords,row=60)
            naukri_jobs = fetch_naukri_jobs(search_keywords,row=60)


        st.markdown("### LinkedIn Job Recommendations")

        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job['title']}** at **{job['company']}** in **{job['location']}**")
                st.markdown(f"{job['description']}")
                st.markdown(f"[Apply Here]({job['url']})")
                st.markdown("---")
        else:
            st.markdown("No job recommendations found on LinkedIn.")    

        st.markdown("### Naukri Job Recommendations")  
        if naukri_jobs:
            for job in naukri_jobs:
                st.markdown(f"**{job['title']}** at **{job['company']}** in **{job['location']}**")
                st.markdown(f"{job['description']}")
                st.markdown(f"[Apply Here]({job['url']})")
                st.markdown("---")
        else:
            st.markdown("No job recommendations found on Naukri.")