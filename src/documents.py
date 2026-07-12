from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Document:
    path: Path
    title: str
    text: str


@dataclass(frozen=True)
class Chunk:
    document_title: str
    source_path: str
    chunk_index: int
    text: str


def load_markdown_documents(docs_dir: Path) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(docs_dir.glob("*.md")):
        raw_text = path.read_text(encoding="utf-8")
        text = strip_front_matter(raw_text).strip()
        documents.append(
            Document(
                path=path,
                title=extract_title(text, path),
                text=text,
            )
        )
    return documents


def strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + len("\n---") :]
    return text


def extract_title(text: str, path: Path) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


def chunk_documents(
    documents: list[Document],
    max_words: int = 120,
    overlap_words: int = 25,
) -> list[Chunk]:
    if max_words <= 0:
        raise ValueError("max_words must be positive.")
    if overlap_words < 0 or overlap_words >= max_words:
        raise ValueError("overlap_words must be between 0 and max_words - 1.")

    chunks: list[Chunk] = []
    for document in documents:
        words = tokenize_words(document.text)
        start = 0
        chunk_index = 0
        while start < len(words):
            end = min(start + max_words, len(words))
            chunk_text = " ".join(words[start:end])
            chunks.append(
                Chunk(
                    document_title=document.title,
                    source_path=str(document.path),
                    chunk_index=chunk_index,
                    text=chunk_text,
                )
            )
            if end == len(words):
                break
            start = end - overlap_words
            chunk_index += 1
    return chunks


def tokenize_words(text: str) -> list[str]:
    return re.findall(r"\S+", text)
