"""Collect paragraphs from JSON files into a CSV."""
import os
import json
import pandas as pd
INPUT_DIR = os.getenv("INPUT_DIR", "procesado")
OUTPUT_CSV = os.getenv("OUTPUT_CSV", os.path.join(INPUT_DIR, "parrafos_embeddings.csv"))


def main():
    rows = []
    for fname in os.listdir(INPUT_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(INPUT_DIR, fname), "r", encoding="utf-8") as f:
                data = json.load(f)
                for entry in data:
                    texto = entry.get("parrafo", "").strip()
                    if texto:
                        rows.append({"cuerpo": fname.replace(".json", ""), "parrafo": texto})
    pd.DataFrame(rows).to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"Exportados {len(rows)} párrafos a {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
