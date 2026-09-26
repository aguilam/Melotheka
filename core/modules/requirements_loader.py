import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from packaging.requirements import Requirement

from core.modules.manifest_loader import Manifest


def resolve_python_dependency(manifests: dict[Path, Manifest]) -> None:
    py_dependency: set[str] = set()
    for manifest in manifests.values():
        py_dependency.update(manifest.dependencies.python)
    not_installed = check_python_dependency(py_dependency)
    if len(not_installed) > 0:
        install_python_dependencies(not_installed)


def check_python_dependency(dependencies: set[str]) -> list[str]:
    not_installed = []
    for dependency in dependencies:
        requirement = Requirement(dependency)
        try:
            installed = version(requirement.name)
            if installed not in requirement.specifier:
                not_installed.append(dependency)
        except PackageNotFoundError:
            not_installed.append(dependency)
    return not_installed


def install_python_dependencies(packages: list[str]):
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", *packages], check=True)
    except Exception as e:
        print(e)
