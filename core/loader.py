import inspect
from dataclasses import dataclass
from importlib import import_module
from importlib.abc import Loader
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any

from core.modules.manifest_loader import find_manifests
from core.modules.requirements_loader import resolve_python_dependency
from core.schemas import HealthStatus, ServiceStatus


@dataclass(slots=True)
class ModuleEntry[T]:
    tag: str
    priority: int
    params: dict[str, Any]
    instance: T


def import_plugins[T](
    current_path: str, BaseClass: type[T], package_name: str
) -> dict[str, type[T]]:
    source = Path(current_path).resolve().parent
    root = source.parent if source.is_file() else source

    modules: dict[str, type[T]] = {}
    searchs_path = find_manifests(source, "builtin/")
    plugins_path = find_manifests(source, "external/")
    manifests = {**searchs_path, **plugins_path}
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
        if (
            isinstance(cls, type)
            and issubclass(cls, BaseClass)
            and cls is not BaseClass
        ):
            key = getattr(cls, "NAME", None) or manifest.tag
            if key is None:
                continue
            modules[key] = cls
    return modules


def old_import_plugins[T](current_path: str, BaseClass: type[T]) -> dict[str, type[T]]:
    path = Path.resolve(Path(current_path)).parent
    searchs_path = (path / "builtin").glob("*.py")
    plugins_path = (path / "external").glob("*.py")
    searched_modules = [*searchs_path, *plugins_path]
    modules: dict[str, type[T]] = {}
    for search in searched_modules:
        spec = spec_from_file_location(search.stem, str(search.resolve()))
        if spec is None or not isinstance(spec.loader, Loader):
            continue
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if (
                cls.__module__ == module.__name__
                and issubclass(cls, BaseClass)
                and cls is not BaseClass
            ):
                key = getattr(cls, "TAG", None) or getattr(cls, "NAME", None)
                if key is None:
                    continue
                modules[key] = cls
    return modules


def load_plugins[T](
    config: dict, module_classes: dict[str, type[T]]
) -> tuple[list[ModuleEntry[T]], list[ServiceStatus]]:
    modules: list[ModuleEntry[T]] = []
    statuses = []
    for module, settings in config.items():
        try:
            cls = module_classes[module]
            is_enabled = settings.get("enabled", True)
            if cls and is_enabled:
                params: dict = settings.get("params", {})
                modules.append(
                    ModuleEntry(
                        module, settings.get("priority", 0), params, cls(params)
                    )
                )
                statuses.append(
                    ServiceStatus(
                        tag=module,
                        health=HealthStatus(ok=True),
                    )
                )
            elif cls and not is_enabled:
                statuses.append(
                    ServiceStatus(
                        tag=module,
                        health=HealthStatus(ok=False, message="Disabled"),
                    )
                )
        except Exception as e:
            statuses.append(
                ServiceStatus(
                    tag=module,
                    health=HealthStatus(ok=False, message=str(e)),
                )
            )
    modules.sort(key=lambda x: x.priority, reverse=True)
    return modules, statuses
