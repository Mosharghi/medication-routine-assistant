import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "meds.json"


def _default_data():
    return {
        "medications": [],
        "dose_logs": []
    }


def load_data():
    if not DATA_FILE.exists():
        save_data(_default_data())
        return _default_data()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        save_data(_default_data())
        return _default_data()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
