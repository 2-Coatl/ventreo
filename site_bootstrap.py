"""Utilities to expose the Django project as the ``site`` package."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent
PROJECT_PACKAGE_DIR = PROJECT_ROOT / 'site'


def _copy_module_attributes(original: ModuleType, target: ModuleType) -> None:
    """Populate ``target`` with the public attributes from ``original``."""
    target.__dict__.update(original.__dict__)


def ensure_site_package() -> ModuleType:
    """Ensure Python can import ``site.*`` from the project package."""
    builtin_site = importlib.import_module('site')
    project_path = str(PROJECT_PACKAGE_DIR)
    current_paths: List[str] = list(getattr(builtin_site, '__dict__', {}).get('__path__', []))

    if project_path in current_paths:
        return builtin_site

    proxy = ModuleType('site')
    _copy_module_attributes(builtin_site, proxy)
    current_paths.insert(0, project_path)
    proxy.__path__ = current_paths
    proxy.__package__ = 'site'
    proxy.__loader__ = builtin_site.__loader__
    proxy.__spec__ = builtin_site.__spec__
    proxy._original_module = builtin_site  # type: ignore[attr-defined]
    sys.modules['site'] = proxy
    return proxy


ensure_site_package()
