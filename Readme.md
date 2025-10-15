#NOTE : Try to Avoid LAN network while testing deployed version.
# 🧭  Travel Assistant (Trip Buddy) 


**Trip Buddy** is an intelligent, context-aware travel assistant built using the Google **Gemini AI**. It provides personalized, grounded answers based *strictly* on a structured itinerary, helping travelers plan, explore, and manage their trips effectively without hallucination.

---
## [LIVE](https://aravindinduri-trip-buddy-app-1fq4m4.streamlit.app/)

## 💡 Overview

Trip Buddy acts as your friendly **AI travel companion**. It processes a user's travel itinerary (stored as structured text) and uses **Retrieval-Augmented Generation (RAG)** to answer travel-related queries such as:

*   *“What are my plans on day 2?”*
*   *“Which hotel am I staying in?”*
*   *“When is my flight back?”*
*   *Suggest are some tourist spots?”*

Crucially, if the information is not explicitly available in the itinerary, Trip Buddy politely refuses to answer, ensuring **accuracy and preventing hallucinations**.

---
## File Structure
```
Directory structure:
└── Trip_buddy/
    ├── Readme.md
    ├── app.py
    ├── requirements.txt
    ├── backend/
    │   ├── llm.py
    │   └── retriever.py
    └── data/
        └── itinerary.md

```

## ✨ Key Features

| Status | Feature | Description |
| :---: | :--- | :--- |
| ✅ | **Grounded Q\&A (RAG)** | Answers are strictly derived from the itinerary text using retrieval. |
| ✅ | **Friendly Persona** | Uses a conversational and helpful AI persona (**Trip Buddy**). |
| ✅ | **Context-Aware** | Maintains chat history memory for multi-turn conversations. |
| ✅ | **Streamlit UI** | Interactive, real-time chat interface for seamless user interaction. |
| ✅ | **Gemini LLM** | Integrates configurable Gemini models (`gemini-flash-latest` by default). |
| ✅ | **Mode A: Strict Grounding** | Ensures answers remain within the bounds of the provided data. |
| ⚙️ | **Mode B: Tool-Augmented** | Planned integration for external tools (weather, flights, etc.) for missing info. |

---

## ⚙️ Tech Stack

| Component | Technology | Role |
| :------------ | :------------- | :--- |
| **LLM** | Google Gemini | Core AI for generation and conversation. |
| **Frontend** | Streamlit | Fast development of the interactive chat UI. |
| **Backend** | Python | Main application logic and data processing. |
| **Data Flow** | RAG (Retrieval) | Context-aware retrieval from the text-based itinerary. |
| **Environment** | `.` file | Secure storage and loading of the Gemini API key. |

---

## 🧱 Architecture Overview (RAG Flow)

Trip Buddy employs a classic RAG architecture to ensure all responses are grounded in the user's specific itinerary.

1.  **Ingestion:** The structured itinerary text is loaded and processed (chunked).
2.  **Indexing:** Text chunks are converted into vector embeddings.
3.  **Query:** User asks a question in the Streamlit UI.
4.  **Retrieval:** The user's query is embedded, and a similarity search is performed against the indexed itinerary vectors to find the most relevant chunks (the context).
5.  **Augmentation:** The relevant itinerary chunks are combined with the user's question and sent to the Gemini LLM as a single, comprehensive prompt.
6.  **Generation:** The Gemini model generates a grounded, personalized, and conversational response.





## 🚀 Setup Instructions

Follow these steps to get your local development environment running.

### 1. Clone the repository

```bash
git clone https://github.com/aravindinduri/trip-buddy.git
cd trip-buddy
```

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

```
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate   # On Windows
```

### 3. Install Dependencies
Install the required Python packages from the `requirements.txt` file.
```
pip install -r requirements.txt
```

## 🔐 4. Add Your Gemini & Hugging Face API Keys (Secure Setup)
---
1. **Create a local secrets file** for development:

```
   # .streamlit/secrets.toml
   [api_keys]
   GOOGLE_API_KEY = "your_google_api_key_here"
   HUGGINGFACE_API_KEY = "your_huggingface_token_here"
```
### 5. Run the Streamlit App

Launch the application using Streamlit:
```
streamlit run app.py
```

The application will open automatically in your web browser (usually at `http://localhost:8501`).

---

## 💬 Example Interaction

**User:** Hello
**Trip Buddy:** Hello! I’m your Trip Buddy 😊 How can I help you plan your Dubai adventure today?

**User:** What’s planned on Day 3?
**Trip Buddy:** Day 3 is your Desert Safari day! You'll relax in the morning, then head out around 3 PM for dune bashing, camel rides, sandboarding, and a BBQ dinner with a cultural show. You'll return to the hotel late evening.

**User:** What's the weather like?
**Trip Buddy:** I apologize, but I only have access to your itinerary details. The weather information is not currently included in your travel plan. I'm working on adding external tool support soon!

---

## 📋 Project Checklist & Status

| Feature | Status | Notes |
| :--- | :--- | :--- |
| Basic itinerary ingestion | ✅ | Text file with structured travel data |
| Retrieval-based grounding (RAG) | ✅ | Uses `retriever.py` to fetch relevant chunks |
| Gemini LLM integration | ✅ | Configurable via `.secrets.toml` |
| Streamlit front-end | ✅ | Simple UI with chat-style responses |
| Mode A (Strict Grounded LLM) | ✅ | Answers only from itinerary |
| Chat history memory | ✅ | Maintains conversational context |
| Error handling & fallback | ✅ | Graceful error messages |

---

## 🔮 Future Improvements & Roadmap

### 🌐 External Tool Integrations (Mode B)
*   **Real-time data:** Integrate APIs for real-time weather, flight status, hotel bookings, and currency exchange rates.
*   **Events:** Event discovery through APIs like Ticketmaster or Eventbrite.

### 🤖 Intelligence & UX
*   **Multi-turn Context:** Advanced context retention beyond the current session (e.g., preference learning).
*   **Personalization:** User profile personalization based on interests, dietary restrictions, etc.
*   **Dynamic Itinerary:** Ability to update, modify, or regenerate the itinerary based on user requests.

---

### Screenshot
![Image](https://i.ibb.co/9kqKwSGn/Screenshot-from-2025-10-14-23-06-19.png)

## 🧠 Project Assumptions

1.  **Strict Source of Truth:** The `data/itinerary.md` text file is the **sole source of context** for all LLM answers. No general knowledge, web searches, or external data are used in this mode.
2.  **Single Trip Scope:** The itinerary file is assumed to contain information for **only one single trip**. This is crucial for avoiding ambiguity when referring to relative terms like "Day 2" or "the hotel," which could be confusing if multiple itineraries were present.
3.  **Core Assistant Purpose:** The sole function of the Trip Buddy assistant is to answer questions **directly related to the specific travel itinerary**. All off-topic, general knowledge, or administrative queries are politely declined, as reinforced by the keyword checks in the `app.py` file.
4.  **Well-Structured Data:** The itinerary text is assumed to be reasonably **well-structured** (e.g., using clear headings, tables, or distinct paragraphs) to facilitate effective chunking and retrieval. All key travel details (flights, hotels, sightseeing, etc.) must be **explicitly and fully included** in this file.
5.  **Language:** User interaction and all itinerary content are assumed to be in **English**.
