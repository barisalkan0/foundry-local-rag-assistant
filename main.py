from src.config import CHAT_MODEL_ALIAS, EMBEDDING_MODEL_ALIAS
from src.foundry_runtime import list_model_aliases


def main() -> None:
    print("Yerel RAG Asistanı - Kurulum Kontrolü")
    print("Foundry Local model kataloğu kontrol ediliyor...")

    aliases = list_model_aliases()
    print(f"Kullanılabilir model alias sayısı: {len(aliases)}")
    print(f"Seçili chat modeli: {CHAT_MODEL_ALIAS}")
    print(f"Seçili embedding modeli: {EMBEDDING_MODEL_ALIAS}")

    missing = [
        alias
        for alias in (CHAT_MODEL_ALIAS, EMBEDDING_MODEL_ALIAS)
        if alias not in aliases
    ]
    if missing:
        print("Eksik gerekli alias'lar:")
        for alias in missing:
            print(f"- {alias}")
        raise SystemExit(1)

    print("Foundry Local katalog kontrolü başarılı.")


if __name__ == "__main__":
    main()
