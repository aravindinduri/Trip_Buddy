import google.generativeai as genai
import tomli as tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

google_key = config["GOOGLE_API_KEY"]

genai.configure(api_key=google_key)

def call_gemini(prompt: str, model="gemini-flash-latest"):
    """
    Calls Gemini API with safety guardrails.
    """
    llm = genai.GenerativeModel(model)
    response = llm.generate_content(prompt)
    return response.text
