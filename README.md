# Foundry Local RAG Assistant

A retrieval-augmented generation (RAG) assistant that runs entirely on a local machine with
[Microsoft Foundry Local](https://github.com/microsoft/Foundry-Local). It finds the most relevant
parts of local documents for a question and answers with a local model, citing the sources it used.

No request is sent to a cloud model. Apart from the first model download, answering runs locally.

Built during the Microsoft Türkiye AI Innovators Program (summer 2026) to learn Foundry Local and RAG.

## What it does

1. Markdown documents in `data/docs/` are split into chunks (up to 120 words, 25-word overlap).
2. Each chunk is embedded with `qwen3-embedding-0.6b` and stored in a local SQLite database (`data/rag.db`).
3. A question is embedded the same way. Chunks are ranked by cosine similarity plus a small keyword-overlap bonus, and the top 3 are kept.
4. The chunks are passed as context to `qwen2.5-0.5b` running on Foundry Local, which answers with source citations.
5. If the documents do not contain the answer, the assistant does not guess. It replies
   `Yerel dokümanlarda bu bilgi yok.` ("This information is not in the local documents.").

Small local models can produce weak Turkish answers, so when a low-quality answer is detected the app
falls back to a short extractive answer taken from the most relevant source.

```text
question -> embedding -> SQLite search -> top chunks -> Foundry Local model -> answer with sources
```

## Project structure

```text
data/docs/          Local documents
data/rag.db         SQLite knowledge base (created by ingest.py)
src/documents.py    Document loading and chunking
src/embeddings.py   Embedding generation
src/retrieval.py    Similarity search
src/rag.py          Answer generation pipeline
scripts/ingest.py   Builds the knowledge base from the documents
scripts/ask.py      Ask a single question
scripts/chat.py     Chat in the terminal
scripts/web.py      Web interface
tests/              Unit tests for chunking and retrieval
```

## Setup

Install the dependencies:

```powershell
pip install -r requirements.txt
```

If the Foundry Local native packages are not installed yet, run:

```powershell
foundry-local-install
```

If this command is not on your PATH, run `foundry-local-install.exe` from your Python `Scripts` folder.

## Building the knowledge base

After adding or changing documents in `data/docs/`, rebuild the knowledge base:

```powershell
python scripts/ingest.py
```

This reads the documents, splits them into chunks, generates embeddings and saves them to `data/rag.db`.

## Usage

Ask a single question:

```powershell
python scripts/ask.py "RAG nedir?"
```

Chat in the terminal:

```powershell
python scripts/chat.py
```

Start the web interface and open `http://127.0.0.1:8000`:

```powershell
python scripts/web.py
```

The sample documents and the interface are in Turkish. Example questions are in `docs/demo_questions.md`.
A question that is not covered by the documents, such as `"Fransa'nın başkenti nedir?"`, should return the
"not in the local documents" reply.

## Tests

```powershell
python -m unittest discover -s tests
```

Run the demo questions in one go:

```powershell
python scripts/evaluate.py
```

## Notes

This is a learning and demo project. Brute-force search over SQLite is enough for a small document set;
a larger collection would need a proper vector database.
