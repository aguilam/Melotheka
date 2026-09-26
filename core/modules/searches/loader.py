from core.loader import ModuleEntry, import_plugins, load_plugins
from core.modules.searches.base import Search
from core.schemas import ServiceStatus


def import_searches(
    config: dict,
) -> tuple[list[ModuleEntry[Search]], list[ServiceStatus]]:
    return load_plugins(config, import_plugins(__file__, Search, __package__))
