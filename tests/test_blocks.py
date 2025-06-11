import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analisis_por_bloques import load_chunks
import fitz


def test_load_chunks(tmp_path):
    pdf = tmp_path / "simple.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hola mundo")
    doc.save(str(pdf))
    doc.close()

    chunks = load_chunks(str(pdf), chunk_size=5)
    assert any("Hola" in c.page_content for c in chunks)

