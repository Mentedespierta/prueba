"""Analyze PDF documents in blocks using LangChain and GPT models."""

from __future__ import annotations

import os
from typing import List

from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI

QUESTIONS = [
    "Resumen del bloque?",
]

CHUNK_SIZE = 1000


def load_chunks(pdf_path: str, chunk_size: int = CHUNK_SIZE):
    """Load a PDF and split it into chunks."""
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
    return splitter.split_documents(docs)


def analyze_pdf(pdf_path: str, questions: List[str] = QUESTIONS) -> List[dict]:
    """Analyze a PDF by answering questions for each chunk."""
    chunks = load_chunks(pdf_path)
    llm = ChatOpenAI(model="gpt-4o-mini")
    results = []
    for i, chunk in enumerate(chunks):
        block_responses = []
        for q in questions:
            prompt = f"{chunk.page_content}\n\nPregunta: {q}"
            resp = llm.predict(prompt)
            block_responses.append({"question": q, "answer": resp})
        results.append({"block": i, "text": chunk.page_content, "responses": block_responses})
    return results


if __name__ == "__main__":
    PDF_PATH = os.getenv("PDF_PATH", "sample.pdf")
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(PDF_PATH)
    data = analyze_pdf(PDF_PATH)
    for item in data:
        print(f"Block {item['block']}")
        for resp in item["responses"]:
            print(f"Q: {resp['question']}\nA: {resp['answer']}\n")

