# app.py
import streamlit as st
from backend.retriever import retrieve
from backend.llm import call_gemini

st.set_page_config(page_title="🕌 Trip Buddy!", layout="wide")

st.title("🛫 Trip Buddy!")
st.markdown("""
Welcome to your **Trip Buddy!**  
I can help you with information from your travel itinerary — day plans, activities, etc.  
I will **only** answer questions based on your itinerary, not general knowledge.
""")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! 👋 I'm your Trip Buddy. How can I help you plan your trip today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_query := st.chat_input("Ask about your itinerary..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    banned_keywords = [
        "prime minister", "india", "math", "calculate", "2 + 2", "capital",
        "history", "politics", "who is", "when was", "population", "weather", "news"
    ]
    if any(word in user_query.lower() for word in banned_keywords):
        answer = "I’m sorry, I can only answer questions related to your Dubai trip itinerary."
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.stop()

    retrieved_chunks = retrieve(user_query, k=3)
    if not retrieved_chunks:
        answer = "I’m sorry, that information isn’t part of your itinerary."
    else:
        context_text = "\n\n".join([r["chunk"] for r in retrieved_chunks])
        prompt = f"""
You are **Trip Buddy**, a warm and knowledgeable travel assistant helping users with their trip.
Your goal is to provide accurate, natural, and conversational answers based strictly on the information below.

📘 **Instructions:**
- Use ONLY the provided itinerary text as your source of truth.
- If the requested information is not mentioned in the itinerary, politely say you don’t have that information.
- Never invent, assume, or speculate beyond what is written.
- Answer as if you’re personally guiding the traveler — friendly, concise, and easy to read.
- Avoid phrases like “according to the itinerary” or “based on the document.”
- Keep the tone polite, confident, and travel-oriented.

🗂️ **Itinerary Context:**
{context_text}

💬 **User’s Question:**
{user_query}

✈️ **Your Response (friendly, natural, and factual):**
"""

        answer = call_gemini(prompt)

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
