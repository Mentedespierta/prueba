"""Generate embeddings and FAISS index from CSV, correcting the paragraph column if needed."""

import os
import pandas as pd
try:
    import polars as pl
except ImportError:  # polars is optional
    pl = None
import numpy as np
import faiss
import openai

CSV_PATH = os.path.join("procesado", "parrafos_embeddings.csv")
INDEX_PATH = os.path.join("procesado", "vectorstore_faiss.index")
openai.api_key = os.getenv("OPENAI_API_KEY")

POSSIBLE = ["parrafo", "texto", "content", "fragmento"]

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(CSV_PATH)

print("Leyendo CSV...")
if pl:
    df = pl.read_csv(CSV_PATH).to_pandas()
else:
    df = pd.read_csv(CSV_PATH)
col = next((c for c in df.columns if c in POSSIBLE), None)
if not col:
    raise ValueError(f"No se encontró columna válida en {df.columns}")
if col != "parrafo":
    df.rename(columns={col: "parrafo"}, inplace=True)

def get_emb(text):
    resp = openai.embeddings.create(input=text[:3000], model="text-embedding-3-small")
    return np.array(resp.data[0].embedding, dtype="float32")

print("Generando embeddings...")
embs = np.vstack([get_emb(t) for t in df["parrafo"].astype(str)])

print("Construyendo índice FAISS...")
index = faiss.IndexFlatL2(embs.shape[1])
index.add(embs)
faiss.write_index(index, INDEX_PATH)
print(f"Índice guardado en {INDEX_PATH}")

