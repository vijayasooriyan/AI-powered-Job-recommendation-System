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
    Handles multiple keywords by searching for each and combining results
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
                "page_size": min(row, 50)
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
                        
                        if len(all_jobs) >= row:
                            return all_jobs[:row]
                    except Exception as e:
                        print(f"Error processing job: {e}")
                        continue
            except Exception as e:
                print(f"Error fetching jobs for keyword '{keyword}': {e}")
                continue
        
        return all_jobs[:row]
    
    except Exception as e:
        print(f"Error fetching LinkedIn jobs: {e}")
        return []


def fetch_naukri_jobs(search_query, location="", row=10):
    """
    Fetch jobs using The Muse API (same as fetch_linkedin_jobs)
    Handles multiple keywords by searching for each and combining results
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
                "page_size": min(row, 50)
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
                        
                        if len(all_jobs) >= row:
                            return all_jobs[:row]
                    except Exception as e:
                        print(f"Error processing job: {e}")
                        continue
            except Exception as e:
                print(f"Error fetching jobs for keyword '{keyword}': {e}")
                continue
        
        return all_jobs[:row]
    
    except Exception as e:
        print(f"Error fetching Naukri jobs from The Muse: {e}")
        return []