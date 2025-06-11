import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import pandas as pd
import runpy


def test_csv(tmp_path, monkeypatch):
    d = tmp_path / "procesado"
    d.mkdir()
    monkeypatch.setenv("INPUT_DIR", str(d))
    monkeypatch.setenv("OUTPUT_CSV", str(d / "out.csv"))

    data = [{"parrafo": "hola"}, {"parrafo": "mundo"}]
    with open(d / "file.json", "w", encoding="utf-8") as f:
        json.dump(data, f)

    runpy.run_module("extrae_parrafos_a_csv", run_name="__main__")
    df = pd.read_csv(d / "out.csv")
    assert len(df) == 2
