from apify_client import ApifyClient
import os
from dotenv import load_dotenv
from html.parser import HTMLParser
load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

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

#fetch linkedin and naukri jobs based on search query and location and return the results as a list of dictionaries with keys: title, company, location, description, url
def fetch_linkedin_jobs(search_query,location="Sri Lanka", row=60):
    run_input = {
        "title": search_query,
        "location": location,
        "rows": row,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        }
    }

    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    raw_jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    
    # Normalize the data to consistent keys
    jobs = []
    for job in raw_jobs:
        normalized_job = {
            "title": job.get("positionTitle", "") or job.get("title", "N/A"),
            "company": job.get("company", "N/A"),
            "location": job.get("location", "N/A"),
            "description": job.get("jobDescription", "") or job.get("description", "N/A"),
            "url": job.get("link", "") or job.get("url", "#")
        }
        jobs.append(normalized_job)
    
    return jobs

def fetch_naukri_jobs(search_query,location="Srilanka", row=60):
    run_input = {
        "keyword": search_query,
        "maxJobs": row,
        "freshness": "all", 
        "sortby": "relevance",
        "experience": "all",
    }

    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    raw_jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    
    # Normalize the data to consistent keys
    jobs = []
    for job in raw_jobs:
        normalized_job = {
            "title": job.get("jobTitle", "") or job.get("title", "N/A"),
            "company": job.get("companyName", "") or job.get("company", "N/A"),
            "location": job.get("jobLocation", "") or job.get("location", "N/A"),
            "description": strip_html(job.get("jobDescription", "") or job.get("description", "N/A")),
            "url": job.get("jobUrl", "") or job.get("url", "#")
        }
        jobs.append(normalized_job)
    
    return jobs