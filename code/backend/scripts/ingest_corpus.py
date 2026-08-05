"""
Loader script - ingereaza toate documentele din data/ in Qdrant via API.
Imbunatatire 2: extrage metadata reala (title, product, effective, version)
din headerul YAML al fiecarui document si o trimite la ingestie.
Rulare: uv run python code/backend/scripts/ingest_corpus.py
"""

import argparse
import os
import requests

API_URL = "http://localhost:7799"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data")


def parse_yaml_header(text: str) -> tuple[dict, str]:
    """Extrage headerul YAML (intre ---) si returneaza (metadata, continut)."""
    metadata = {}
    content = text

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            header_lines = parts[1].strip().split("\n")
            for line in header_lines:
                if ":" in line:
                    key, _, value = line.partition(":")
                    metadata[key.strip()] = value.strip()
            content = parts[2].strip()

    return metadata, content


def ingest_file(filepath: str, source: str,
                 chunk_size: int = 2000, strategy: str = "heading") -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    metadata, content = parse_yaml_header(raw)

    payload = {
        "text": content,       # body only — the YAML header is metadata, not retrievable text
        # heading (default): one chunk per "## " section — never cuts a section's
        # numbers off, and (unlike one whole-doc chunk) stays topically narrow so
        # its embedding isn't diluted — see app/chunking.py's chunk_heading().
        # --strategy dynamic --chunk-size 500 reproduces the pre-fix baseline.
        "strategy": strategy,
        "chunk_size": chunk_size,  # safety cap for a section that runs unusually long
        "source": source,
        "metadata": {
            "title": metadata.get("title", source),
            "product": metadata.get("product", "general"),
            "effective": metadata.get("effective", ""),
            "version": metadata.get("version", "1"),
            "audience": metadata.get("audience", "retail"),
        },
    }

    response = requests.post(f"{API_URL}/ingest", json=payload)

    if response.status_code == 200:
        data = response.json()
        chunks = data.get("chunks_stored", "?")
        title = metadata.get("title", source)
        print(f"  OK  {source}")
        print(f"      title={title}, product={metadata.get('product','?')}, effective={metadata.get('effective','?')} -> {chunks} chunks")
        return True
    else:
        print(f"  ERR {source} -> {response.status_code}: {response.text[:100]}")
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk-size", type=int, default=2000,
                         help="override chunk_size sent to /ingest (default 2000 — a safety "
                              "cap, most sections are far smaller). Use 500 with "
                              "--strategy dynamic to reproduce the pre-fix baseline in NOTES.md.")
    parser.add_argument("--strategy", default="heading",
                         help="chunking strategy (default: heading — see app/chunking.py)")
    args = parser.parse_args()

    data_dir = os.path.abspath(DATA_DIR)
    print(f"Corpus folder: {data_dir}  (strategy={args.strategy}, chunk_size={args.chunk_size})\n")

    excluded = {"README.md", "questions.md", "golden_set.json", "golden_set_results.json"}
    files = sorted([
        f for f in os.listdir(data_dir)
        if f.endswith(".md") and f not in excluded
    ])

    print(f"Found {len(files)} documents to ingest:\n")

    ok = 0
    fail = 0

    for filename in files:
        filepath = os.path.join(data_dir, filename)
        source = filename.replace(".md", "")
        success = ingest_file(filepath, source, chunk_size=args.chunk_size, strategy=args.strategy)
        if success:
            ok += 1
        else:
            fail += 1

    print(f"\nDone: {ok} ok, {fail} failed.")


if __name__ == "__main__":
    main()