import streamlit as st
import pandas as pd
import os
import faiss
import numpy as np
import openai
import datetime

# --- Paths ---
BASE_DIR = os.getcwd()
PROCESADO_DIR = os.path.join(BASE_DIR, "procesado")
CSV_PATH = os.path.join(PROCESADO_DIR, "parrafos_embeddings.csv")
INDEX_PATH = os.path.join(PROCESADO_DIR, "vectorstore_faiss.index")
BITACORA_PATH = os.path.join(BASE_DIR, "03_output", "bitacora_gpt.txt")

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="DEFENSOR-X", layout="wide")

# --- Utilities ---

def registrar_bitacora(msg, rol="Sistema"):
    os.makedirs(os.path.dirname(BITACORA_PATH), exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(BITACORA_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ({rol}) >> {msg}\n")


def get_embedding(text: str) -> np.ndarray:
    resp = openai.embeddings.create(input=text[:3000], model="text-embedding-3-small")
    return np.array(resp.data[0].embedding, dtype="float32").reshape(1, -1)


def load_index():
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    return None

# --- Interface ---
menu = st.sidebar.radio("Menú", ["Inicio", "Carga", "Consulta", "Bitácora"])

if menu == "Inicio":
    st.title("⚖️ DEFENSOR-X")
    st.write("Sistema legal interactivo")
    registrar_bitacora("Ingreso a Inicio")

elif menu == "Carga":
    st.header("Carga de archivos")
    files = st.file_uploader("Archivos TXT o DOCX", type=["txt", "docx"], accept_multiple_files=True)
    if files:
        os.makedirs("originales", exist_ok=True)
        for f in files:
            path = os.path.join("originales", f.name)
            with open(path, "wb") as out:
                out.write(f.getbuffer())
            st.success(f"Guardado {f.name}")
            registrar_bitacora(f"Archivo cargado {f.name}", rol="Usuario")

elif menu == "Consulta":
    st.header("Consulta jurídica con embeddings")
    pregunta = st.text_area("Pregunta")
    topk = st.slider("Párrafos a recuperar", 5, 40, 10)
    ejecutar = st.button("Analizar")
    if ejecutar and pregunta.strip():
        if not os.path.exists(CSV_PATH) or not os.path.exists(INDEX_PATH):
            st.error("No existen archivos procesados. Ejecuta los scripts de preparación.")
        else:
            df = pd.read_csv(CSV_PATH)
            index = load_index()
            if index is None:
                st.error("Índice FAISS no disponible")
            else:
                q_emb = get_embedding(pregunta)
                D, I = index.search(q_emb, topk)
                ctx_list = []
                for idx in I[0]:
                    parrafo = df.iloc[idx]["parrafo"]
                    ctx_list.append(parrafo)
                contexto = "\n".join(ctx_list)
                prompt = f"Contexto:\n{contexto}\n\nPregunta:{pregunta}"
                resp = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.2,
                )
                respuesta = resp.choices[0].message.content
                st.text_area("Respuesta", respuesta, height=300)
                registrar_bitacora(f"Consulta: {pregunta}", rol="Usuario")

elif menu == "Bitácora":
    st.header("Bitácora")
    if os.path.exists(BITACORA_PATH):
        with open(BITACORA_PATH, "r", encoding="utf-8") as f:
            st.text_area("Actividad", f.read(), height=400)
    else:
        st.write("Sin bitácora")
