"""
Loader script - ingereaza toate documentele din data/ in Qdrant via API.
Rulare: uv run python code/backend/scripts/ingest_corpus.py
"""

import os
import requests

API_URL = "http://localhost:7799"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")


def ingest_file(filepath: str, source: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    payload = {
        "text": text,
        "strategy": "dynamic",
        "source": source,
    }

    response = requests.post(f"{API_URL}/ingest", json=payload)

    if response.status_code == 200:
        data = response.json()
        chunks = data.get("chunks_stored", "?")
        print(f"  OK  {source} -> {chunks} chunks")
        return True
    else:
        print(f"  ERR {source} -> {response.status_code}: {response.text[:100]}")
        return False


def main():
    data_dir = os.path.abspath(DATA_DIR)
    print(f"Corpus folder: {data_dir}\n")

    files = sorted([
        f for f in os.listdir(data_dir)
        if f.endswith(".md") and f != "README.md"
    ])

    print(f"Found {len(files)} documents to ingest:\n")

    ok = 0
    fail = 0

    for filename in files:
        filepath = os.path.join(data_dir, filename)
        source = filename.replace(".md", "")
        success = ingest_file(filepath, source)
        if success:
            ok += 1
        else:
            fail += 1

    print(f"\nDone: {ok} ok, {fail} failed.")


if __name__ == "__main__":
    main()