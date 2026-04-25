import os
import requests
from dotenv import load_dotenv
from html.parser import HTMLParser
load_dotenv()

# RapidAPI credentials for JSearch
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "jsearch.p.rapidapi.com")

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

#fetch jobs using JSearch API (free alternative to Apify)
def fetch_linkedin_jobs(search_query, location="", row=10):
    """
    Fetch LinkedIn jobs using JSearch API from RapidAPI
    Free tier: 100 requests/month
    """
    # Safety check: If RAPIDAPI_KEY is not set, return empty list
    if not RAPIDAPI_KEY or RAPIDAPI_KEY == "your_jsearch_rapidapi_key_here":
        print("⚠️ Warning: RAPIDAPI_KEY not configured. Skipping job search.")
        return []
    
    try:
        url = "https://jsearch.p.rapidapi.com/search"
        
        # Search query with location
        search_string = f"{search_query} jobs"
        if location:
            search_string += f" in {location}"
        
        querystring = {
            "query": search_string,
            "page": "1",
            "num_pages": "1"
        }
        
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST
        }
        
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        
        if response.status_code != 200:
            print(f"JSearch API Error: {response.status_code}")
            return []
        
        raw_jobs = response.json().get('data', [])
        
        # Normalize the data to consistent keys
        jobs = []
        for job in raw_jobs[:row]:  # Limit to 'row' number of jobs
            try:
                normalized_job = {
                    "title": job.get("job_title", "N/A"),
                    "company": job.get("employer_name", "N/A"),
                    "location": job.get("job_city", "") + ", " + job.get("job_country", ""),
                    "description": job.get("job_description", "N/A")[:500] + "...",  # Truncate
                    "url": job.get("job_apply_link", "#")
                }
                jobs.append(normalized_job)
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
        
        return jobs
    
    except Exception as e:
        print(f"Error fetching LinkedIn jobs: {e}")
        return []


def fetch_naukri_jobs(search_query, location="", row=10):
    """
    Fetch jobs using JSearch API (same as fetch_linkedin_jobs)
    JSearch aggregates jobs from multiple sources including Naukri-like platforms
    """
    # Safety check: If RAPIDAPI_KEY is not set, return empty list
    if not RAPIDAPI_KEY or RAPIDAPI_KEY == "your_jsearch_rapidapi_key_here":
        print("⚠️ Warning: RAPIDAPI_KEY not configured. Skipping job search.")
        return []
    
    try:
        url = "https://jsearch.p.rapidapi.com/search"
        
        search_string = f"{search_query} jobs"
        if location:
            search_string += f" in {location}"
        
        querystring = {
            "query": search_string,
            "page": "1",
            "num_pages": "1"
        }
        
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST
        }
        
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        
        if response.status_code != 200:
            print(f"JSearch API Error: {response.status_code}")
            return []
        
        raw_jobs = response.json().get('data', [])
        
        # Normalize the data to consistent keys
        jobs = []
        for job in raw_jobs[:row]:  # Limit to 'row' number of jobs
            try:
                normalized_job = {
                    "title": job.get("job_title", "N/A"),
                    "company": job.get("employer_name", "N/A"),
                    "location": job.get("job_city", "") + ", " + job.get("job_country", ""),
                    "description": job.get("job_description", "N/A")[:500] + "...",  # Truncate
                    "url": job.get("job_apply_link", "#")
                }
                jobs.append(normalized_job)
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
        
        return jobs
    
    except Exception as e:
        print(f"Error fetching Naukri jobs: {e}")
        return []