"""Service objects that operate on identity primitives."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .models import ROLE_HIERARCHY, Role


@dataclass(frozen=True)
class RoleAssignment:
    """Map an identity to the set of roles it holds."""

    user_identifier: str
    roles: Sequence[str]

    def grants(self, role: str) -> bool:
        """Return True when the assignment contains the provided role."""

        return role in self.roles

    def highest_rank(self) -> str:
        """Return the highest privilege role according to the defined hierarchy."""

        if not self.roles:
            return Role.VIEWER
        return min(self.roles, key=lambda value: ROLE_HIERARCHY.get(value, float('inf')))


def flatten_role_assignments(assignments: Iterable[RoleAssignment]) -> set[str]:
    """Return the unique set of roles granted across multiple assignments."""

    aggregated: set[str] = set()
    for assignment in assignments:
        aggregated.update(assignment.roles)
    return aggregated


__all__ = ['RoleAssignment', 'flatten_role_assignments']
