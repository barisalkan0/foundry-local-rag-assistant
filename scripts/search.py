from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.retrieval import retrieve


def main() -> None:
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        query = input("Soru: ").strip()

    results = retrieve(query)
    print(f"Sorgu: {query}")
    print(f"Sonuç sayısı: {len(results)}")

    for index, row in enumerate(results, start=1):
        print()
        print(f"{index}. {row['document_title']} (skor: {row['score']:.4f})")
        print(row["text"][:500])


if __name__ == "__main__":
    main()
