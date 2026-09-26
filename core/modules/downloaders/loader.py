from core.loader import ModuleEntry, import_plugins, load_plugins
from core.modules.downloaders.base import Downloader
from core.schemas import ServiceStatus


def load_downloaders(
    config: dict,
) -> tuple[list[ModuleEntry[Downloader]], list[ServiceStatus]]:
    return load_plugins(
        config,
        import_plugins(__file__, Downloader, __package__),
    )
