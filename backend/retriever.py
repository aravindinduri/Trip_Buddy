
import requests
import faiss
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json",
}

def get_embedding(text: str):
    """Fetch embeddings from Hugging Face Inference API."""
    url = f"https://api-inference.huggingface.co/models/{EMBEDDING_MODEL}"
    response = requests.post(url, headers=HEADERS, json={"inputs": text}, timeout=60)
    if response.status_code != 200:
        raise Exception(f"Hugging Face API error {response.status_code}: {response.text}")
    
    data = response.json()
    if isinstance(data, list) and isinstance(data[0], list):
        return np.array(data[0], dtype="float32")
    elif isinstance(data, list) and isinstance(data[0], (int, float)):
        return np.array(data, dtype="float32")
    else:
        raise ValueError(f"Unexpected embedding response: {data}")

def chunk_itinerary(text):
    return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]


def build_faiss_index(itinerary_path="data/itinerary.md", index_path="data/embeddings.index"):
    if not os.path.exists(itinerary_path):
        raise FileNotFoundError(f"'{itinerary_path}' not found.")
    
    with open(itinerary_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    chunks = chunk_itinerary(text)
    print(f"🔹 Building embeddings for {len(chunks)} chunks...")

    vectors = [get_embedding(chunk) for chunk in chunks]
    vectors = np.vstack(vectors).astype("float32")

    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, index_path)

    return chunks, index

def load_retriever(itinerary_path="data/itinerary.md", index_path="data/embeddings.index"):
    if not os.path.exists(index_path):
        return build_faiss_index(itinerary_path, index_path)
    
    with open(itinerary_path, "r", encoding="utf-8") as f:
        chunks = chunk_itinerary(f.read())
    
    index = faiss.read_index(index_path)
    return chunks, index

def retrieve(query: str, k=3):
    """
    Retrieve top-k relevant chunks from the itinerary.
    Returns list of dicts: {"chunk": ..., "distance": ...}
    """
    chunks, index = load_retriever()
    qvec = get_embedding(query).reshape(1, -1)
    D, I = index.search(qvec.astype("float32"), k)

    results = []
    for i, dist in zip(I[0], D[0]):
        results.append({"chunk": chunks[i], "distance": float(dist)})
    return results

