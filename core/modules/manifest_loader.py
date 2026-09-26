import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ManifestDependency:
    python: list[str]
    modules: list[str]
    modules_optional: list[str]


@dataclass(slots=True)
class Manifest:
    id: str | None
    tag: str | None
    name: str | None
    version: str
    entrypoint: str
    dependencies: ManifestDependency


def find_manifests(current_dir: Path, start_dir: str = "") -> dict[Path, Manifest]:
    root = current_dir / start_dir
    manifests = {}
    for item in root.glob("*/manifest.json"):
        try:
            manifests[item.parent] = parse_manifest(item.resolve())
        except Exception:
            continue
    return manifests


def parse_manifest(path: Path) -> Manifest:
    with path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)
        dependencies = manifest["dependencies"]
        return Manifest(
            id=manifest.get("id"),
            name=manifest.get("name"),
            tag=manifest.get("tag"),
            version=manifest["version"],
            entrypoint=manifest["entrypoint"],
            dependencies=ManifestDependency(
                python=dependencies["python"],
                modules=dependencies["modules"],
                modules_optional=dependencies["modules_optional"],
            ),
        )
