"""Domain services for the identity module."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .models import Role


@dataclass(frozen=True)
class RoleAssignment:
    """Map an identity to the set of role slugs it holds."""

    user_identifier: str
    roles: Sequence[str]

    def grants(self, role: str) -> bool:
        """Return True when the assignment contains the provided role."""

        return role in self.roles


def flatten_role_assignments(assignments: Iterable[RoleAssignment]) -> set[str]:
    """Return the unique set of roles granted across multiple assignments."""

    aggregated: set[str] = set()
    for assignment in assignments:
        aggregated.update(assignment.roles)
    return aggregated


def highest_privilege_role(role_slugs: Sequence[str]) -> Role | None:
    """Return the highest privilege role for a set of role slugs."""

    if not role_slugs:
        return None
    return (
        Role.objects.filter(slug__in=role_slugs)
        .order_by('hierarchy_level', 'slug')
        .first()
    )


__all__ = ['RoleAssignment', 'flatten_role_assignments', 'highest_privilege_role']
