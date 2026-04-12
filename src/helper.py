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

