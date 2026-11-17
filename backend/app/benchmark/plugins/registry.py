"""Central registry. Add a class here (or a package entry point later) to expose a plug-in."""

from app.benchmark.plugins.standard import HyDERAG, SimpleRAG
from app.benchmark.types import RAGPlugin


PLUGIN_TYPES: dict[str, type[RAGPlugin]] = {"simple": SimpleRAG, "hyde": HyDERAG}


def list_plugins() -> list[dict[str, object]]:
    return [{"id": plugin.name, "name": plugin.display_name, "capabilities": sorted(plugin.capabilities)} for plugin in PLUGIN_TYPES.values()]


def create_plugin(plugin_id: str) -> RAGPlugin:
    try:
        return PLUGIN_TYPES[plugin_id]()
    except KeyError as exc:
        raise KeyError(plugin_id) from exc
