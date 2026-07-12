from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.rag import answer_question


QUESTIONS = [
    "RAG nedir?",
    "Foundry Local çevrimdışı yapay zekaya nasıl yardımcı olur?",
    "SQLite bu projede neden yararlıdır?",
    "Dokümanları değiştirdikten sonra ne yapmalıyım?",
    "Fransa'nın başkenti nedir?",
]


def main() -> None:
    for question in QUESTIONS:
        print("=" * 72)
        print(f"Soru: {question}")
        result = answer_question(question)
        print(f"Cevap: {result['answer']}")
        print("Kaynaklar:")
        for source in result["sources"]:
            print(f"- {source['document_title']} ({source['score']:.4f})")


if __name__ == "__main__":
    main()
