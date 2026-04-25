import os
import requests
from dotenv import load_dotenv
from html.parser import HTMLParser
load_dotenv()

# The Muse API - No authentication needed, unlimited free requests
MUSE_BASE_URL = "https://www.themuse.com/api/public/jobs"

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

#fetch jobs using The Muse API (free alternative, no auth needed)
def fetch_linkedin_jobs(search_query, location="", row=10):
    """
    Fetch jobs using The Muse API
    Free tier: Unlimited requests, no authentication required
    Better quality jobs than other free alternatives
    """
    try:
        params = {
            "page": 0,
            "page_size": min(row, 50)  # The Muse supports up to 50 per page
        }
        
        # Add search query if provided
        if search_query:
            params["search"] = search_query
        
        # Add location filter if provided
        if location:
            params["location"] = location
        
        response = requests.get(MUSE_BASE_URL, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"The Muse API Error: {response.status_code}")
            return []
        
        raw_jobs = response.json().get('results', [])
        
        # Normalize the data to consistent keys
        jobs = []
        for job in raw_jobs[:row]:  # Limit to 'row' number of jobs
            try:
                # Clean up description if it contains HTML
                description = job.get("contents", "N/A")
                if description != "N/A":
                    description = strip_html(description)[:500] + "..."
                
                normalized_job = {
                    "title": job.get("name", "N/A"),
                    "company": job.get("company", {}).get("name", "N/A"),
                    "location": job.get("locations", [{}])[0].get("name", "Remote") if job.get("locations") else "Remote",
                    "description": description,
                    "url": job.get("refs", {}).get("landing_page", "#")
                }
                jobs.append(normalized_job)
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
        
        return jobs
    
    except Exception as e:
        print(f"Error fetching jobs from The Muse: {e}")
        return []


def fetch_naukri_jobs(search_query, location="", row=10):
    """
    Fetch jobs using The Muse API (same as fetch_linkedin_jobs)
    The Muse aggregates jobs from multiple sources
    Free tier: Unlimited requests, no authentication required
    """
    try:
        params = {
            "page": 0,
            "page_size": min(row, 50)  # The Muse supports up to 50 per page
        }
        
        # Add search query if provided
        if search_query:
            params["search"] = search_query
        
        # Add location filter if provided
        if location:
            params["location"] = location
        
        response = requests.get(MUSE_BASE_URL, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"The Muse API Error: {response.status_code}")
            return []
        
        raw_jobs = response.json().get('results', [])
        
        # Normalize the data to consistent keys
        jobs = []
        for job in raw_jobs[:row]:  # Limit to 'row' number of jobs
            try:
                # Clean up description if it contains HTML
                description = job.get("contents", "N/A")
                if description != "N/A":
                    description = strip_html(description)[:500] + "..."
                
                normalized_job = {
                    "title": job.get("name", "N/A"),
                    "company": job.get("company", {}).get("name", "N/A"),
                    "location": job.get("locations", [{}])[0].get("name", "Remote") if job.get("locations") else "Remote",
                    "description": description,
                    "url": job.get("refs", {}).get("landing_page", "#")
                }
                jobs.append(normalized_job)
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
        
        return jobs
    
    except Exception as e:
        print(f"Error fetching Naukri jobs from The Muse: {e}")
        return []