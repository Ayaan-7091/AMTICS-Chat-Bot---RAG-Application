import os
import ollama
import faiss
from pypdf import PdfReader
import numpy as np
import streamlit as st

#CONFIG - Data file and models
DATA_FILE = 'data/info.txt'
EMBED_MODEL = "all-minilm"
GEN_MODEL = "llama3:8b"

#Helper Functions

#1. Reading the Info file
def read_file(path):
    if path.lower().endswith(".pdf"):
        reader = PdfReader(path)
        return "\n".join([p.extract_text() or "" for p in reader.pages])
    else:
        with open(path, "r", encoding="utf-8",errors="ignore") as f:
            return f.read()
        
#2. Splitting the document into chunks
def chunk_text(text, size=800, overlap=200):
    chunks, start = [], 0
    while start < len(text):
        end = min(start+size, len(text))
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

#3. Converts Chunks into Vectors (Embeddings)
def embed_texts(texts, model=EMBED_MODEL):
    embs = []
    for t in texts:
        resp = ollama.embeddings(model=model, prompt=t)
        embs.append(np.array(resp["embedding"], dtype=np.float32))
    return np.vstack(embs)

#4. Takes the embeddings and builds an index for quick retrieval
def build_faiss(embs):
    d = embs.shape[1]
    index = faiss.IndexFlatIP(d)   # cosine similarity after normalization
    faiss.normalize_L2(embs)
    index.add(embs)
    return index

# Takes the User query and retrieves the relevant embedding from the Index
def retrieve(query, index, chunks, k=6):
    resp = ollama.embeddings(model=EMBED_MODEL, prompt=query)
    q_emb = np.array(resp["embedding"], dtype=np.float32).reshape(1, -1)
    faiss.normalize_L2(q_emb)
    D, I = index.search(q_emb, k)
    return [(chunks[i], float(D[0][j])) for j,i in enumerate(I[0])]

#
def generate_answer(query, retrieved):
    context = "\n\n".join([c[:300] for c, _ in retrieved])

    system = (
   "You are a helpful assistant for AMTICS college. "
    "Answer naturally and conversationally. "
    "Use only the provided information, but combine details when needed to give a clear answer. "
    "Do NOT say 'based on context' or 'the document says'."
    )

    user_msg = f"{context}\n\nQuestion: {query}"

    resp = ollama.chat(model=GEN_MODEL, messages=[ 
        {"role": "system", "content": system},
        {"role": "user", "content": user_msg}
    ])
    return resp.message.content


