from __future__ import annotations

from src.config import EMBEDDING_MODEL_ALIAS
from src.foundry_runtime import ensure_model_loaded


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    model = ensure_model_loaded(EMBEDDING_MODEL_ALIAS, show_progress)
    client = model.get_embedding_client()
    response = client.generate_embeddings(texts)
    return [item.embedding for item in response.data]


def show_progress(progress: float) -> None:
    print(f"\rEmbedding modeli indiriliyor: {progress:.1f}%", end="", flush=True)
