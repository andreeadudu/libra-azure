@"
# Assignment 2 — Notes

## Chunk counts (Folder 1)

- Static: 6 chunks
- Sentence: 5 chunks
- Dynamic: 5 chunks
- Semantic: N/A (requires embedding provider)

## Acceptance questions

### 1. How many dimensions does an embedding have here?
1536 dimensions. The model text-embedding-3-small produces 1536-dimensional vectors, visible in the vector_dimension field of the Ingest response.

### 2. What score did the off-topic query get, and what does that tell you?
The off-topic query gets a very low score (close to 0). This tells us that retrieval always returns something — it never returns empty — but the score is what indicates whether the result is actually relevant. A low score means the retrieved passages have no meaningful connection to the query.

### 3. What exactly is added to the prompt when use_rag is true?
When use_rag is true, the retrieved passages from the vector store are injected into the prompt as context, along with citation instructions telling the model to base its answer on those passages and cite them as [1], [2], etc. This is why prompt_sent is much longer with RAG than without — it contains the full source text the model must ground its answer on.

### 4. Where can the lyrical agent run, and how do you know?
Under Docker, all agents show runs_on: unknown because the Foundry Agent Service requires Microsoft Entra authentication (identity-based), which is unavailable inside Docker where there is no az login. When running locally after az login, lyrical shows runs_on: local since it has not been deployed to Foundry. If deployed, it would show runs_on: both.
"@ | Out-File -Encoding utf8 NOTES.md