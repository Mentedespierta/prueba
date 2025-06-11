import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import os
from procesador_extraccion_legal_parrafos import extract_from_txt


def test_extract(tmp_path):
    sample = tmp_path / "doc.txt"
    sample.write_text("Uno\n\nDos")
    res = extract_from_txt(str(sample))
    assert res == ["Uno", "Dos"]

