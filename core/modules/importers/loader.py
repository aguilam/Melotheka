from core.loader import ModuleEntry, import_plugins, load_plugins
from core.modules.importers.base import Importer
from core.schemas import ServiceStatus


def load_importers(
    config: dict,
) -> tuple[list[ModuleEntry[Importer]], list[ServiceStatus]]:
    return load_plugins(config, import_plugins(__file__, Importer, __package__))
