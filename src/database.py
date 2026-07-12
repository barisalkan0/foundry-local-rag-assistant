from __future__ import annotations

from pathlib import Path
import json
import sqlite3

from src.documents import Chunk


SCHEMA = """
CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_title TEXT NOT NULL,
    source_path TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    embedding_json TEXT NOT NULL
);
"""


def connect_database(database_path: Path) -> sqlite3.Connection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.execute(SCHEMA)
    return connection


def reset_chunks(connection: sqlite3.Connection) -> None:
    connection.execute("DELETE FROM chunks")
    connection.commit()


def insert_chunks(
    connection: sqlite3.Connection,
    chunks: list[Chunk],
    embeddings: list[list[float]],
) -> None:
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length.")

    rows = [
        (
            chunk.document_title,
            chunk.source_path,
            chunk.chunk_index,
            chunk.text,
            json.dumps(embedding),
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]
    connection.executemany(
        """
        INSERT INTO chunks (
            document_title, source_path, chunk_index, text, embedding_json
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        rows,
    )
    connection.commit()


def count_chunks(connection: sqlite3.Connection) -> int:
    row = connection.execute("SELECT COUNT(*) FROM chunks").fetchone()
    return int(row[0])


def load_chunk_rows(connection: sqlite3.Connection) -> list[dict]:
    cursor = connection.execute(
        """
        SELECT id, document_title, source_path, chunk_index, text, embedding_json
        FROM chunks
        ORDER BY id
        """
    )
    rows: list[dict] = []
    for row in cursor.fetchall():
        rows.append(
            {
                "id": row[0],
                "document_title": row[1],
                "source_path": row[2],
                "chunk_index": row[3],
                "text": row[4],
                "embedding": json.loads(row[5]),
            }
        )
    return rows
