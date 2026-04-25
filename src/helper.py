import fitz  #PymuPDF
import os
import dotenv
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)  
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

def ask_groq(prompt, max_tokens=500):
    """
    Sends a prompt to the Groq API and returns the response.

    Args:
        prompt (str): The prompt to send to the Groq API.

    Returns:
        str: The response from the Groq API.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=max_tokens
        )
    return response.choices[0].message.content

