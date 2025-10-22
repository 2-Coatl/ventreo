"""Tests for the access control matrix."""
from __future__ import annotations

from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.access_control import PermissionSet, resolve_sheet_permissions
from modules.identity import Role


@pytest.mark.parametrize(
    'sheet, role, expected',
    [
        ('05_Costos_Fijos', Role.CFO, PermissionSet(read=True, write=True)),
        ('05_Costos_Fijos', Role.GERENTE, PermissionSet(read=True)),
        ('26_Calculadora_Impuestos', Role.CONTADOR, PermissionSet(read=True, write=True, approve=True, export=True)),
        ('26_Calculadora_Impuestos', Role.VIEWER, PermissionSet()),
    ],
)
def test_permission_matrix_matches_expected(sheet: str, role: str, expected: PermissionSet) -> None:
    """Lookup returns the pre-defined PermissionSet for each sheet/role pair."""

    assert resolve_sheet_permissions(sheet, [role]) == expected


def test_combines_permissions_for_multiple_roles() -> None:
    """Union of roles should merge write and approve flags."""

    combined = resolve_sheet_permissions('02_Inversion_Inicial', [Role.CFO, Role.CEO])
    assert combined.read is True
    assert combined.write is True
    assert combined.approve is True


def test_unknown_sheet_returns_empty_permissions() -> None:
    """When the sheet is unknown, no permissions are granted by default."""

    assert resolve_sheet_permissions('99_No_Existe', [Role.CEO]).read is False
