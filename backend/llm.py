import google.generativeai as genai
import streamlit as st

google_key = st.secrets["api_keys"]["GOOGLE_API_KEY"]

genai.configure(api_key=google_key)

def call_gemini(prompt: str, model="gemini-flash-latest"):
    """
    Calls Gemini API with safety guardrails.
    """
    llm = genai.GenerativeModel(model)
    response = llm.generate_content(prompt)
    return response.text
