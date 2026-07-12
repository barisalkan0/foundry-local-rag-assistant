from __future__ import annotations

from pathlib import Path
import math
import re

from src.config import DATABASE_PATH, TOP_K
from src.database import connect_database, load_chunk_rows
from src.embeddings import generate_embeddings


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    query_embedding = generate_embeddings([query])[0]

    with connect_database(Path(DATABASE_PATH)) as connection:
        rows = load_chunk_rows(connection)

    scored_rows = []
    for row in rows:
        vector_score = cosine_similarity(query_embedding, row["embedding"])
        keyword_score = keyword_overlap(query, row["text"])
        score = vector_score + (keyword_score * 0.05)
        scored_rows.append(
            {
                **row,
                "score": score,
                "vector_score": vector_score,
                "keyword_score": keyword_score,
            }
        )

    return sorted(scored_rows, key=lambda row: row["score"], reverse=True)[:top_k]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Vectors must have the same length.")

    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def keyword_overlap(query: str, text: str) -> float:
    query_terms = normalize_terms(query)
    text_terms = normalize_terms(text)
    if not query_terms:
        return 0.0
    return len(query_terms & text_terms) / len(query_terms)


def normalize_terms(text: str) -> set[str]:
    stop_words = {
        "a",
        "an",
        "and",
        "are",
        "do",
        "does",
        "for",
        "how",
        "i",
        "in",
        "is",
        "it",
        "of",
        "should",
        "the",
        "to",
        "what",
        "why",
        "ama",
        "benim",
        "bir",
        "bu",
        "da",
        "de",
        "daha",
        "diye",
        "icin",
        "için",
        "ile",
        "mi",
        "mı",
        "mu",
        "mü",
        "nasıl",
        "neden",
        "ne",
        "nedir",
        "sonra",
        "tekrar",
        "ve",
        "veya",
        "ya",
    }
    terms = set(re.findall(r"[\wçğıöşü]+", text.lower(), flags=re.UNICODE))
    return {term for term in terms if term not in stop_words and len(term) > 1}
