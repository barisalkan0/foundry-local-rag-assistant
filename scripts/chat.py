from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.rag import answer_question


def main() -> None:
    print("Yerel RAG Asistanı")
    print("Bir soru yaz. Çıkmak için 'çık' veya 'exit' yaz.")

    while True:
        question = input("\nSoru: ").strip()
        if question.lower() in {"çık", "cik", "exit", "quit"}:
            break
        if not question:
            continue

        result = answer_question(question)
        print("\nCevap:")
        print(result["answer"])
        print("\nKaynaklar:")
        for source in result["sources"]:
            print(f"- {source['document_title']} (skor: {source['score']:.4f})")


if __name__ == "__main__":
    main()
