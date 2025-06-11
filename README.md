# DEFENSOR-X Prototype

This repository contains a minimal prototype for a legal document management and analysis system. The tools are meant for experimentation with embeddings and GPT models.

## Requirements
- Python 3.8+
- OpenAI API key

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Usage
1. Process source documents using `procesador_extraccion_legal_parrafos.py` to create JSON files.
2. Convert the JSON files into a CSV with `extrae_parrafos_a_csv.py`.
3. Generate the FAISS index with `generar_index_con_autocorreccion.py`.
4. Launch the Streamlit interface:
```bash
streamlit run app_expediente_legal_interactivo.py
```

The processed files are expected inside the `procesado/` folder.

## Tests
Run unit tests using:
```bash
pytest
```

