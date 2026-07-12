from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.documents import chunk_documents, load_markdown_documents


def main() -> None:
    docs_dir = Path("data/docs")
    documents = load_markdown_documents(docs_dir)
    chunks = chunk_documents(documents)

    print(f"Doküman sayısı: {len(documents)}")
    print(f"Chunk sayısı: {len(chunks)}")

    for chunk in chunks:
        print()
        print(f"[{chunk.document_title} #{chunk.chunk_index}]")
        print(chunk.text[:300])


if __name__ == "__main__":
    main()
