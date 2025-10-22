"""Permission helpers for spreadsheet-style resources."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from modules.identity import Role


@dataclass(frozen=True)
class PermissionSet:
    """Boolean flags that describe the actions a role may take."""

    read: bool = False
    write: bool = False
    approve: bool = False
    export: bool = False
    simulate: bool = False

    def allows(self, action: str) -> bool:
        """Return True when the set enables the named action."""

        mapping = {
            'read': self.read,
            'write': self.write,
            'approve': self.approve,
            'export': self.export,
            'simulate': self.simulate,
        }
        try:
            return mapping[action]
        except KeyError as exc:  # pragma: no cover - developer error paths
            raise ValueError(f'Unsupported action: {action!r}') from exc

    def union(self, other: 'PermissionSet') -> 'PermissionSet':
        """Combine two permission sets taking the most permissive flags."""

        return PermissionSet(
            read=self.read or other.read,
            write=self.write or other.write,
            approve=self.approve or other.approve,
            export=self.export or other.export,
            simulate=self.simulate or other.simulate,
        )


READ_ONLY = PermissionSet(read=True)
READ_WRITE = PermissionSet(read=True, write=True)
READ_APPROVE = PermissionSet(read=True, approve=True)
READ_WRITE_APPROVE = PermissionSet(read=True, write=True, approve=True)
FULL_AUDIT = PermissionSet(read=True, write=True, approve=True, export=True)
SIMULATE_ONLY = PermissionSet(read=True, simulate=True)


SHEET_PERMISSIONS: Mapping[str, Mapping[str, PermissionSet]] = {
    '01_Parametros_Globales': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.CEO: READ_ONLY,
        Role.CONTADOR: READ_ONLY,
        Role.CONTROLLER: READ_ONLY,
        Role.ANALISTA: READ_ONLY,
        Role.GERENTE: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '02_Inversion_Inicial': {
        Role.SUPER_ADMIN: READ_WRITE_APPROVE,
        Role.CFO: READ_WRITE,
        Role.CONTROLLER: READ_WRITE,
        Role.CEO: READ_APPROVE,
        Role.CONTADOR: READ_ONLY,
        Role.ANALISTA: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '05_Costos_Fijos': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.CONTROLLER: READ_WRITE,
        Role.CONTADOR: READ_ONLY,
        Role.ANALISTA: READ_ONLY,
        Role.GERENTE: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '06_Costos_Variables': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.CONTROLLER: READ_WRITE,
        Role.CONTADOR: READ_ONLY,
        Role.ANALISTA: READ_ONLY,
        Role.GERENTE: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '07_MO_Puestos': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.CONTADOR: READ_WRITE,
        Role.CONTROLLER: READ_WRITE,
        Role.CEO: READ_ONLY,
        Role.GERENTE: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '08_MO_Actividades': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.CONTADOR: READ_WRITE,
        Role.CONTROLLER: READ_WRITE,
        Role.CEO: READ_ONLY,
        Role.GERENTE: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '09_Modelo_Precios': {
        Role.SUPER_ADMIN: READ_WRITE_APPROVE,
        Role.CFO: READ_WRITE,
        Role.CEO: READ_APPROVE,
        Role.ANALISTA: SIMULATE_ONLY,
        Role.CONTADOR: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '10_Proyeccion_Ventas': {
        Role.SUPER_ADMIN: READ_ONLY,
        Role.CEO: READ_ONLY,
        Role.CFO: READ_ONLY,
        Role.CONTROLLER: READ_ONLY,
        Role.CONTADOR: READ_ONLY,
        Role.ANALISTA: READ_ONLY,
        Role.GERENTE: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
        Role.VIEWER: READ_ONLY,
    },
    '11_Suscripcion_MRR_LTV': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.ANALISTA: READ_WRITE,
        Role.CEO: READ_ONLY,
        Role.CONTROLLER: READ_ONLY,
        Role.CONTADOR: READ_ONLY,
        Role.GERENTE: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '12_Frecuencia_Compra': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.ANALISTA: READ_WRITE,
        Role.CEO: READ_ONLY,
        Role.CONTROLLER: READ_ONLY,
        Role.CONTADOR: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '13_Flujo_Efectivo': {
        Role.SUPER_ADMIN: READ_WRITE_APPROVE,
        Role.CFO: READ_WRITE,
        Role.CONTROLLER: READ_WRITE,
        Role.CEO: READ_ONLY,
        Role.CONTADOR: READ_ONLY,
        Role.ANALISTA: READ_ONLY,
        Role.GERENTE: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '14_Margen_Contribucion': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.ANALISTA: READ_WRITE,
        Role.CONTROLLER: READ_WRITE,
        Role.CEO: READ_ONLY,
        Role.GERENTE: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '15_Payback_ROI': {
        Role.SUPER_ADMIN: READ_WRITE_APPROVE,
        Role.CFO: READ_WRITE,
        Role.ANALISTA: READ_WRITE,
        Role.CEO: READ_APPROVE,
        Role.AUDITOR: READ_ONLY,
    },
    '19_Escenarios': {
        Role.SUPER_ADMIN: READ_WRITE_APPROVE,
        Role.CFO: READ_WRITE_APPROVE,
        Role.ANALISTA: READ_WRITE,
        Role.CEO: READ_APPROVE,
        Role.CONTROLLER: READ_ONLY,
        Role.CONTADOR: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
        Role.VIEWER: READ_ONLY,
    },
    '20_Montecarlo': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.ANALISTA: READ_WRITE,
        Role.CEO: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '21_Control_Ejecucion': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.CONTROLLER: READ_WRITE,
        Role.GERENTE: READ_ONLY,
        Role.CEO: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '24_Dashboard_Ejecutivo': {
        Role.SUPER_ADMIN: READ_ONLY,
        Role.CEO: READ_ONLY,
        Role.CFO: READ_ONLY,
        Role.CONTROLLER: READ_ONLY,
        Role.CONTADOR: READ_ONLY,
        Role.ANALISTA: READ_ONLY,
        Role.GERENTE: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
        Role.VIEWER: READ_ONLY,
    },
    '25_Simulador_Interactivo': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.ANALISTA: READ_WRITE,
        Role.CEO: SIMULATE_ONLY,
        Role.CONTROLLER: SIMULATE_ONLY,
        Role.GERENTE: READ_ONLY,
    },
    '26_Calculadora_Impuestos': {
        Role.SUPER_ADMIN: FULL_AUDIT,
        Role.CONTADOR: FULL_AUDIT,
        Role.CFO: READ_WRITE,
        Role.CEO: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '27_Depreciacion_Equipamiento': {
        Role.SUPER_ADMIN: READ_WRITE,
        Role.CFO: READ_WRITE,
        Role.CONTADOR: READ_WRITE,
        Role.CONTROLLER: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '28_Control_Acceso_RBAC': {
        Role.SUPER_ADMIN: READ_WRITE_APPROVE,
        Role.CFO: READ_ONLY,
        Role.CEO: READ_ONLY,
        Role.CONTROLLER: READ_ONLY,
        Role.CONTADOR: READ_ONLY,
        Role.ANALISTA: READ_ONLY,
        Role.GERENTE: READ_ONLY,
        Role.AUDITOR: READ_ONLY,
    },
    '29_Auditoria_Cambios': {
        Role.SUPER_ADMIN: FULL_AUDIT,
        Role.AUDITOR: FULL_AUDIT,
        Role.CFO: READ_ONLY,
        Role.CEO: READ_ONLY,
    },
    '30_Dashboard_CEO': {
        Role.SUPER_ADMIN: READ_ONLY,
        Role.CEO: READ_ONLY,
        Role.CFO: READ_ONLY,
    },
    '31_Dashboard_CFO': {
        Role.SUPER_ADMIN: READ_ONLY,
        Role.CFO: READ_ONLY,
        Role.CEO: READ_ONLY,
    },
    '32_Dashboard_Contador': {
        Role.SUPER_ADMIN: READ_ONLY,
        Role.CONTADOR: READ_ONLY,
        Role.CFO: READ_ONLY,
    },
    '33_Dashboard_Operaciones': {
        Role.SUPER_ADMIN: READ_ONLY,
        Role.CONTROLLER: READ_ONLY,
        Role.GERENTE: READ_ONLY,
    },
}


def resolve_sheet_permissions(sheet_name: str, roles: Iterable[str]) -> PermissionSet:
    """Return the most permissive rights granted to the provided roles."""

    matrix: Mapping[str, PermissionSet] = SHEET_PERMISSIONS.get(sheet_name, {})
    combined = PermissionSet()
    for role in roles:
        if role not in matrix:
            continue
        combined = combined.union(matrix[role])
    return combined


__all__ = ['PermissionSet', 'SHEET_PERMISSIONS', 'resolve_sheet_permissions']
