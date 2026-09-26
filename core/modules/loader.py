from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

from structlog import BoundLogger

from core.modules import Module
from core.modules.manifest_loader import find_manifests
from core.modules.requirements_loader import (
    resolve_python_dependency,
)
from core.schemas import ServiceStatus

if TYPE_CHECKING:
    from core.modules.modules_manager import ModulesManager


def init_modules(
    modules: ModulesManager,
    logger: BoundLogger,
    config: dict,
    classes: dict[str, type[Module]],
) -> dict[str, tuple[Module, list[ServiceStatus]]]:
    modules_dict: dict[str, tuple[Module, list[ServiceStatus]]] = {}
    for id, class_type in classes.items():
        module_config = config.get(id, {})
        module_logger = logger.bind(module=id)
        instance = class_type(
            modules=modules, config=module_config, logger=module_logger
        )
        modules_dict[id] = (instance, instance.statuses)
    return modules_dict


def import_modules(current_path: str) -> dict[str, type[Module]]:
    source = Path(current_path).resolve().parent

    root = source.parent if source.is_file() else source
    package_name = "core.modules"

    modules: dict[str, type[Module]] = {}
    manifests = find_manifests(source)
    resolve_python_dependency(manifests)
    for module, manifest in manifests.items():
        relative = module.relative_to(root).with_suffix("")
        module_name = ".".join(
            (
                package_name,
                *relative.parts,
            )
        )
        mod, cls_name = manifest.entrypoint.split(":", 1)
        loaded_module = import_module(f"{module_name}.{mod}")
        cls = getattr(loaded_module, cls_name)
        if isinstance(cls, type) and issubclass(cls, Module) and cls is not Module:
            key = manifest.id
            modules[key] = cls
    return modules
