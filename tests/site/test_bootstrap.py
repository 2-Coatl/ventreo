"""Tests that the project exposes its modules through the ``site`` package."""
from __future__ import annotations

from importlib import util
from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import site_bootstrap  # noqa: F401  Ensure bootstrap side effects run for the tests.


@pytest.fixture(scope='module')
def project_site_path() -> Path:
    return (PROJECT_ROOT / 'site').resolve()


def test_site_package_exposes_project_modules(project_site_path: Path) -> None:
    import site as builtin_site

    search_locations = getattr(builtin_site, '__path__', []) or []
    assert str(project_site_path) in [str(Path(p)) for p in search_locations]


def test_python_can_locate_site_settings_module() -> None:
    spec = util.find_spec('site.settings')
    assert spec is not None
    assert spec.origin is not None
    assert spec.origin.endswith('site/settings.py')


def test_domain_apps_are_packaged_at_project_root() -> None:
    """Domain apps live alongside ``authentication`` at the repository root."""

    identity = util.find_spec('identity')
    access_control = util.find_spec('access_control')

    assert identity is not None
    assert access_control is not None
    assert identity.origin is not None and identity.origin.endswith('identity/__init__.py')
    assert access_control.origin is not None and access_control.origin.endswith('access_control/__init__.py')
