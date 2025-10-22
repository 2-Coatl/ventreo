"""Identity and role metadata used across the Ventreo platform."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from django.db import models


class Role(models.TextChoices):
    """Role definitions matching the RBAC spreadsheet matrix."""

    SUPER_ADMIN = 'super_admin', 'Super Admin'
    CEO = 'ceo', 'CEO'
    CFO = 'cfo', 'CFO'
    CONTROLLER = 'controller', 'Controller'
    CONTADOR = 'contador', 'Contador'
    ANALISTA = 'analista', 'Analista Financiero'
    GERENTE = 'gerente', 'Gerente Operativo'
    AUDITOR = 'auditor', 'Auditor'
    VIEWER = 'viewer', 'Viewer'


ROLE_HIERARCHY: Mapping[str, int] = {
    Role.SUPER_ADMIN: 1,
    Role.CEO: 2,
    Role.CFO: 3,
    Role.CONTROLLER: 4,
    Role.CONTADOR: 4,
    Role.ANALISTA: 5,
    Role.GERENTE: 5,
    Role.AUDITOR: 6,
    Role.VIEWER: 7,
}
"""Hierarchy levels allow quick comparisons during policy checks."""


@dataclass(frozen=True)
class RoleCombination:
    """Describe the recommended role bundle for an organisation profile."""

    name: str
    roles: Sequence[str]
    description: str


ROLE_COMBINATIONS: Sequence[RoleCombination] = (
    RoleCombination(
        name='micro',
        roles=(Role.CEO, Role.CFO, Role.CONTADOR, Role.VIEWER),
        description='Micro team: founders combine finance roles and may grant a read-only viewer.',
    ),
    RoleCombination(
        name='small',
        roles=(Role.CEO, Role.CFO, Role.CONTADOR, Role.GERENTE, Role.VIEWER),
        description='Small company: controller duties stay with the CFO while one manager gets scoped access.',
    ),
    RoleCombination(
        name='medium',
        roles=(
            Role.CEO,
            Role.CFO,
            Role.CONTROLLER,
            Role.CONTADOR,
            Role.ANALISTA,
            Role.GERENTE,
            Role.AUDITOR,
        ),
        description='Medium company: segregated finance duties and operational managers for up to four areas.',
    ),
    RoleCombination(
        name='enterprise',
        roles=(
            Role.SUPER_ADMIN,
            Role.CEO,
            Role.CFO,
            Role.CONTROLLER,
            Role.CONTADOR,
            Role.ANALISTA,
            Role.GERENTE,
            Role.AUDITOR,
            Role.VIEWER,
        ),
        description='Large organisation: full RBAC surface with compliance and stakeholder views.',
    ),
)
"""Suggested bundles make it easy to bootstrap deployments per company size."""
