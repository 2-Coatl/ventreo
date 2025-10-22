"""Tests for the identity module role metadata."""
from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.identity import ROLE_COMBINATIONS, ROLE_HIERARCHY, Role


def test_role_enumeration_matches_expected_count() -> None:
    """The RBAC matrix enumerates the nine documented roles."""

    assert len(Role) == 9


def test_role_hierarchy_orders_privileges() -> None:
    """Higher privilege roles must have lower hierarchy numbers."""

    assert ROLE_HIERARCHY[Role.SUPER_ADMIN] < ROLE_HIERARCHY[Role.CEO] < ROLE_HIERARCHY[Role.VIEWER]


def test_role_combinations_cover_all_sizes() -> None:
    """Combinations expose the deployment presets for each company size."""

    names = {combo.name for combo in ROLE_COMBINATIONS}
    assert names == {'micro', 'small', 'medium', 'enterprise'}
