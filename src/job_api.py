#fetch linkedin and naukri jobs based on search query and location and return the results as a list of dictionaries with keys: title, company, location, description, url
def fetch_linkedin_jobs(search_query,location="Srilanka", row=60):
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
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs

def fetch_naukri_jobs(search_query,location="Srilanka", row=60):
    run_input = {
        "keyword": search_query,
        "maxJobs": row,
        "freshness": "any", 
        "sortby": "relevance",
        "experience": "all",
    }

    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs