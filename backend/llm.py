import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def call_gemini(prompt: str, model="gemini-flash-latest"):
    """
    Calls Gemini API with safety guardrails.
    """
    llm = genai.GenerativeModel(model)
    response = llm.generate_content(prompt)
    return response.text
