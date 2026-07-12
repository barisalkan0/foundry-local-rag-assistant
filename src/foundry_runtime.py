from __future__ import annotations

from collections.abc import Callable

from foundry_local_sdk import Configuration, FoundryLocalManager

from src.config import APP_NAME


def initialize_manager() -> FoundryLocalManager:
    """Foundry Local'i bir kez başlat ve singleton manager nesnesini döndür."""
    if FoundryLocalManager.instance is None:
        FoundryLocalManager.initialize(Configuration(app_name=APP_NAME))
    return FoundryLocalManager.instance


def list_model_aliases() -> list[str]:
    manager = initialize_manager()
    return [model.alias for model in manager.catalog.list_models()]


def ensure_model_loaded(model_alias: str, progress: Callable[[float], None] | None = None):
    manager = initialize_manager()
    model = manager.catalog.get_model(model_alias)
    if not model.is_cached:
        model.download(progress)
    if not model.is_loaded:
        model.load()
    return model
