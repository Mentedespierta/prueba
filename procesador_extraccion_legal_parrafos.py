"""Extract paragraphs from TXT or DOCX documents into JSON files."""

import os
import json
import docx2txt
from pathlib import Path

INPUT_DIR = "originales"
OUTPUT_DIR = "procesado"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_from_txt(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paragraphs


def extract_from_docx(path: str) -> list:
    text = docx2txt.process(path)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paragraphs


def main():
    for file in os.listdir(INPUT_DIR):
        file_path = os.path.join(INPUT_DIR, file)
        if file.endswith(".txt"):
            paras = extract_from_txt(file_path)
        elif file.endswith(".docx"):
            paras = extract_from_docx(file_path)
        else:
            continue
        data = [{"parrafo": p} for p in paras]
        out_name = Path(file).stem + ".json"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Procesado {file} -> {out_name}")


if __name__ == "__main__":
    main()
