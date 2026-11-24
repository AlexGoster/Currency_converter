import importlib.util
import json
from pathlib import Path

import pytest
import tkinter as tk

spec = importlib.util.spec_from_file_location("currency_gui", Path(__file__).parents[1] / "main.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@pytest.fixture
def setup(monkeypatch, tmp_path):
    rates = tmp_path / "rates.json"
    rates.write_text(json.dumps({"USD": 1, "EUR": 0.5, "RUB": 100}), encoding="utf-8")
    errors = []
    monkeypatch.setattr(module, "RATES_FILE", str(rates))
    monkeypatch.setattr(module.messagebox, "showerror", lambda *args: errors.append(args))
    return rates, errors


def test_real_widgets_and_conversion(setup):
    root = tk.Tk()
    root.withdraw()
    try:
        app = module.ConverterApp(root)
        app.convert()
        assert "10000.00" in app.result_label.cget("text")
        app.amount_entry.delete(0, tk.END)
        app.amount_entry.insert(0, "nan")
        app.convert()
        assert setup[1]
    finally:
        root.destroy()


@pytest.mark.parametrize("value", [[], {"USD": 0}, {"USD": "one"}, {"USD": -1}])
def test_invalid_rate_files(setup, value):
    setup[0].write_text(json.dumps(value))
    assert module.load_rates() == {}
    assert setup[1]
