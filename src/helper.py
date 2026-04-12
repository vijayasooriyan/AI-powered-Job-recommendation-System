import fitz  #PymuPDF
import os
import dotenv
from openai import OpenAI
from apify_client import ApifyClient

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.

    Args:
        uploaded_file (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """
    
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text = page.get_text()
    return text

def ask_openai(prompt,max_tokens=500):
    """
    Sends a prompt to the OpenAI API and returns the response.

    Args:
        prompt (str): The prompt to send to the OpenAI API.

    Returns:
        str: The response from the OpenAI API.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=max_tokens
        )
    return response.choices[0].message.content

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