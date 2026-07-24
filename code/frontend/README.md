# Libra Assist — Admin Console

A single-page admin panel for the RAG Teaching API, built with plain HTML + CSS + JavaScript.

## How to run

1. Make sure the backend is running (`docker compose up -d` in `code/backend/`).
2. Open `index.html` in your browser — no build step, no install needed.

The console talks to `http://localhost:7799`. CORS is already open on the API.

## What it does

The sidebar navigates six sections, one per API surface:

| Section      | Endpoints                          |
|--------------|-------------------------------------|
| **Status**   | `GET /health`, `GET /config`        |
| **Chunk**    | `POST /chunk`                       |
| **Ingest**   | `POST /ingest`                      |
| **Collection** | `GET /collection`, `DELETE /collection` |
| **Search**   | `POST /search`                      |
| **Ask**      | `POST /ask`                         |

All API errors (409 dimension mismatch, 503 Qdrant down, 502 auth failures) are surfaced with their status code and detail message.

## Stretch goals implemented

- **Embedding vector preview** — the first 8 floats of each vector are shown on ingest and search results.
- **Side-by-side RAG comparison** — the "Compare ± RAG" button runs the same question with and without RAG and displays both answers, retrieved chunks, and prompts.
- **Persistent settings** — last-used strategy and top_k values are saved to `localStorage`.
