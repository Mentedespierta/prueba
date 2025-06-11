# DEFENSOR-X Prototype

This repository contains a minimal prototype for a legal document management and analysis system. The tools are meant for experimentation with embeddings and GPT models.

## Requirements
- Python 3.8+
- OpenAI API key

Install dependencies with:
```bash
pip install -r requirements.txt
```

The requirements include `polars` and `PyMuPDF` for faster CSV handling and PDF
loading, plus `langchain` for block analysis with GPT models.

## Usage
1. Process source documents using `procesador_extraccion_legal_parrafos.py` to create JSON files.
2. Convert the JSON files into a CSV with `extrae_parrafos_a_csv.py`.
3. Generate the FAISS index with `generar_index_con_autocorreccion.py`.
4. Launch the Streamlit interface:
```bash
streamlit run app_expediente_legal_interactivo.py
```
5. Optionally analyze a PDF in blocks using `analisis_por_bloques.py`:
```bash
PDF_PATH=mi_archivo.pdf python analisis_por_bloques.py
```

The processed files are expected inside the `procesado/` folder.

## Tests
Run unit tests using:
```bash
pytest
```

