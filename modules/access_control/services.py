"""Service helpers for resolving sheet permissions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import SheetPermission


@dataclass(frozen=True)
class PermissionSet:
    """Return type representing the effective permissions for a user."""

    read: bool = False
    write: bool = False
    approve: bool = False
    export: bool = False


def resolve_sheet_permissions(sheet_code: str, role_slugs: Iterable[str]) -> PermissionSet:
    """Aggregate permissions for the provided sheet and roles."""

    perms = SheetPermission.objects.filter(sheet__code=sheet_code, role__slug__in=list(role_slugs))
    flags = PermissionSet()
    if not perms.exists():
        return flags

    read = any(item.can_read for item in perms)
    write = any(item.can_write for item in perms)
    approve = any(item.can_approve for item in perms)
    export = any(item.can_export for item in perms)
    return PermissionSet(read=read, write=write, approve=approve, export=export)


__all__ = ['PermissionSet', 'resolve_sheet_permissions']
