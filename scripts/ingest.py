from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import (
    CHUNK_MAX_WORDS,
    CHUNK_OVERLAP_WORDS,
    DATABASE_PATH,
    DOCS_DIR,
)
from src.database import connect_database, count_chunks, insert_chunks, reset_chunks
from src.documents import chunk_documents, load_markdown_documents
from src.embeddings import generate_embeddings


def main() -> None:
    docs_dir = Path(DOCS_DIR)
    database_path = Path(DATABASE_PATH)

    documents = load_markdown_documents(docs_dir)
    chunks = chunk_documents(
        documents,
        max_words=CHUNK_MAX_WORDS,
        overlap_words=CHUNK_OVERLAP_WORDS,
    )

    print(f"Yüklenen doküman sayısı: {len(documents)}")
    print(f"Oluşturulan chunk sayısı: {len(chunks)}")
    if not chunks:
        raise SystemExit("Chunk bulunamadı. data/docs altına Markdown dosyaları ekle.")

    embeddings = generate_embeddings([chunk.text for chunk in chunks])
    print(f"\nÜretilen embedding sayısı: {len(embeddings)}")

    with connect_database(database_path) as connection:
        reset_chunks(connection)
        insert_chunks(connection, chunks, embeddings)
        print(f"SQLite'a kaydedilen chunk sayısı: {count_chunks(connection)}")
        print(f"Veritabanı: {database_path}")


if __name__ == "__main__":
    main()
