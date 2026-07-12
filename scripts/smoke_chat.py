from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import CHAT_MODEL_ALIAS
from src.foundry_runtime import ensure_model_loaded


def show_progress(progress: float) -> None:
    print(f"\rModel indiriliyor: {progress:.1f}%", end="", flush=True)


def main() -> None:
    print(f"Chat modeli yükleniyor: {CHAT_MODEL_ALIAS}")
    model = ensure_model_loaded(CHAT_MODEL_ALIAS, show_progress)
    print("\nModel yüklendi.")

    client = model.get_chat_client()
    response = client.complete_chat(
        [
            {
                "role": "system",
                "content": "Kısa cevap veren bir asistansın. Tek kısa cümleyle Türkçe cevap ver.",
            },
            {
                "role": "user",
                "content": "Retrieval-Augmented Generation nedir?",
            },
        ]
    )

    print("Asistan:")
    print(response.choices[0].message.content)

    model.unload()
    print("Model bellekten indirildi.")


if __name__ == "__main__":
    main()
