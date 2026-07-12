from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.rag import answer_question


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        question = input("Soru: ").strip()

    result = answer_question(question)
    print("Cevap:")
    print(result["answer"])

    print()
    print("Kaynaklar:")
    for source in result["sources"]:
        print(f"- {source['document_title']} (skor: {source['score']:.4f})")


if __name__ == "__main__":
    main()
