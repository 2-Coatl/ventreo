"""Domain constants used by cross-app workflow definitions."""
from __future__ import annotations


class Role:
    """Slug constants that mirror the primary keys of identity roles."""

    SUPER_ADMIN = 'super_admin'
    CFO = 'cfo'
    CEO = 'ceo'
    CONTADOR = 'contador'
    AUDITOR = 'auditor'
    CONTROLLER = 'controller'
    GERENTE = 'gerente'
    ANALISTA = 'analista'


__all__ = ['Role']
