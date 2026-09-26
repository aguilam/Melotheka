from core.loader import ModuleEntry, import_plugins, load_plugins
from core.modules.scrobblers.base import Scrobbler
from core.schemas import ServiceStatus


def load_scrobblers(
    config: dict,
) -> tuple[list[ModuleEntry[Scrobbler]], list[ServiceStatus]]:
    return load_plugins(config, import_plugins(__file__, Scrobbler, __package__))
