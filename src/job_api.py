import os
import requests
from dotenv import load_dotenv
from html.parser import HTMLParser
load_dotenv()

# The Muse API - No authentication needed, unlimited free requests
MUSE_BASE_URL = "https://www.themuse.com/api/public/jobs"

# Keyword relevance mapping - maps resume keywords to relevant job search terms
KEYWORD_RELEVANCE_MAP = {
    # Programming languages - look for tech/developer roles
    "Python": ["python", "developer", "engineer", "backend", "senior engineer", "software engineer", "data scientist", "ml engineer"],
    "JavaScript": ["javascript", "frontend", "react", "nodejs", "developer", "engineer"],
    "Java": ["java", "developer", "engineer", "backend", "software engineer"],
    "SQL": ["sql", "database", "data", "engineer", "developer"],
    
    # ML/AI keywords - look for data science and ML roles
    "Machine Learning": ["machine learning", "ml", "ai", "artificial intelligence", "data scientist"],
    "AI": ["ai", "artificial intelligence", "machine learning", "deep learning"],
    "TensorFlow": ["tensorflow", "deep learning", "engineer", "scientist"],
    "Keras": ["keras", "deep learning", "neural"],
    
    # Data analysis keywords
    "Data Analysis": ["data", "analyst", "data science", "analytics"],
    "Data Science": ["data scientist", "data science", "machine learning"],
    
    # Full-stack keywords
    "Full-stack": ["full stack", "fullstack", "mern", "stack", "react", "node"],
    "React": ["react", "frontend", "developer"],
    "Node": ["node", "nodejs", "backend"],
}

# Jobs to filter out - common false positives
EXCLUDED_JOB_TYPES = [
    "nurse", "nursing", "healthcare", "medical", "physician", "doctor", 
    "sales", "retail", "merchandiser", "restaurant", "hospitality", "lpn"
]

# Helper class to strip HTML tags
class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
    
    def handle_data(self, data):
        self.text.append(data)
    
    def get_text(self):
        return ''.join(self.text).strip()

def strip_html(html_text):
    """Remove HTML tags from text"""
    if not html_text:
        return ""
    stripper = HTMLStripper()
    try:
        stripper.feed(html_text)
        return stripper.get_text()
    except:
        return html_text

def calculate_relevance_score(job_title, job_description, keyword):
    """
    Calculate relevance score for a job based on how well it matches a keyword
    Higher score = more relevant to the keyword
    """
    search_text = (job_title + " " + job_description).lower()
    score = 0
    
    # Get relevant search terms for this keyword
    relevant_terms = KEYWORD_RELEVANCE_MAP.get(keyword, [keyword.lower()])
    
    # Check how many relevant terms appear in the job
    for term in relevant_terms:
        if term.lower() in search_text:
            # Title matches count more than description
            if term.lower() in job_title.lower():
                score += 3
            else:
                score += 1
    
    return score

def filter_jobs_by_relevance(jobs, keywords, min_relevance_threshold=2):
    """
    Filter jobs to only show those relevant to the keywords
    Excludes healthcare, retail, and non-tech positions
    Returns jobs scored and sorted by relevance
    """
    keyword_list = [kw.strip() for kw in keywords.split(",")]
    
    scored_jobs = []
    
    for job in jobs:
        job_title = job.get("title", "").lower()
        job_description = job.get("description", "").lower()
        
        # Exclude non-tech job types
        is_excluded = any(excluded_type in job_title for excluded_type in EXCLUDED_JOB_TYPES)
        if is_excluded:
            continue
        
        # Calculate relevance for this job against all keywords
        total_score = 0
        matched_keywords = []
        
        for keyword in keyword_list:
            relevance = calculate_relevance_score(job_title, job_description, keyword)
            if relevance > 0:
                matched_keywords.append(keyword)
                total_score += relevance
        
        # Only keep jobs that match at least one keyword with good relevance
        if total_score >= min_relevance_threshold and len(matched_keywords) > 0:
            job["relevance_score"] = total_score
            job["matched_keywords"] = matched_keywords
            scored_jobs.append(job)
    
    # Sort by relevance score (highest first)
    scored_jobs.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return scored_jobs    

#fetch jobs using The Muse API (free alternative, no auth needed)
def fetch_linkedin_jobs(search_query, location="", row=10):
    """
    Fetch jobs using The Muse API and filter by relevance to resume keywords
    Only returns jobs that match the keywords from the resume
    Free tier: Unlimited requests, no authentication required
    """
    try:
        # Split keywords by comma and clean them up
        keywords = [kw.strip() for kw in search_query.split(",")]
        all_jobs = []
        seen_urls = set()  # To avoid duplicates
        
        # Fetch jobs for each keyword
        for keyword in keywords:
            if not keyword:
                continue
                
            params = {
                "page": 0,
                "page_size": min(row * 3, 50)  # Fetch more to filter
            }
            
            params["search"] = keyword
            
            if location:
                params["location"] = location
            
            try:
                response = requests.get(MUSE_BASE_URL, params=params, timeout=10)
                
                if response.status_code != 200:
                    continue
                
                raw_jobs = response.json().get('results', [])
                
                # Normalize and add jobs
                for job in raw_jobs:
                    try:
                        job_url = job.get("refs", {}).get("landing_page", "#")
                        
                        # Skip duplicates
                        if job_url in seen_urls:
                            continue
                        
                        seen_urls.add(job_url)
                        
                        # Clean up description if it contains HTML
                        description = job.get("contents", "N/A")
                        if description != "N/A":
                            description = strip_html(description)[:500] + "..."
                        
                        normalized_job = {
                            "title": job.get("name", "N/A"),
                            "company": job.get("company", {}).get("name", "N/A"),
                            "location": job.get("locations", [{}])[0].get("name", "Remote") if job.get("locations") else "Remote",
                            "description": description,
                            "url": job_url,
                            "keyword_matched": keyword  # Track which keyword matched
                        }
                        all_jobs.append(normalized_job)
                    except Exception as e:
                        print(f"Error processing job: {e}")
                        continue
            except Exception as e:
                print(f"Error fetching jobs for keyword '{keyword}': {e}")
                continue
        
        # Filter jobs by relevance to resume skills
        filtered_jobs = filter_jobs_by_relevance(all_jobs, search_query, min_relevance_threshold=1)
        
        # Return top 'row' most relevant jobs
        return filtered_jobs[:row]
    
    except Exception as e:
        print(f"Error fetching LinkedIn jobs: {e}")
        return []


def fetch_naukri_jobs(search_query, location="", row=10):
    """
    Fetch jobs using The Muse API and filter by relevance to resume keywords
    Same as fetch_linkedin_jobs - filters to show only relevant jobs
    Free tier: Unlimited requests, no authentication required
    """
    try:
        # Split keywords by comma and clean them up
        keywords = [kw.strip() for kw in search_query.split(",")]
        all_jobs = []
        seen_urls = set()  # To avoid duplicates
        
        # Fetch jobs for each keyword
        for keyword in keywords:
            if not keyword:
                continue
                
            params = {
                "page": 0,
                "page_size": min(row * 3, 50)  # Fetch more to filter
            }
            
            params["search"] = keyword
            
            if location:
                params["location"] = location
            
            try:
                response = requests.get(MUSE_BASE_URL, params=params, timeout=10)
                
                if response.status_code != 200:
                    continue
                
                raw_jobs = response.json().get('results', [])
                
                # Normalize and add jobs
                for job in raw_jobs:
                    try:
                        job_url = job.get("refs", {}).get("landing_page", "#")
                        
                        # Skip duplicates
                        if job_url in seen_urls:
                            continue
                        
                        seen_urls.add(job_url)
                        
                        # Clean up description if it contains HTML
                        description = job.get("contents", "N/A")
                        if description != "N/A":
                            description = strip_html(description)[:500] + "..."
                        
                        normalized_job = {
                            "title": job.get("name", "N/A"),
                            "company": job.get("company", {}).get("name", "N/A"),
                            "location": job.get("locations", [{}])[0].get("name", "Remote") if job.get("locations") else "Remote",
                            "description": description,
                            "url": job_url,
                            "keyword_matched": keyword  # Track which keyword matched
                        }
                        all_jobs.append(normalized_job)
                    except Exception as e:
                        print(f"Error processing job: {e}")
                        continue
            except Exception as e:
                print(f"Error fetching jobs for keyword '{keyword}': {e}")
                continue
        
        # Filter jobs by relevance to resume skills
        filtered_jobs = filter_jobs_by_relevance(all_jobs, search_query, min_relevance_threshold=1)
        
        # Return top 'row' most relevant jobs
        return filtered_jobs[:row]
    
    except Exception as e:
        print(f"Error fetching Naukri jobs from The Muse: {e}")
        return []