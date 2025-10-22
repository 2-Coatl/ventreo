"""Dataclasses describing the finance pipeline for the modular monolith."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from modules.identity import Role


@dataclass(frozen=True)
class AccessPhase:
    """Describe an authentication or authorisation gate."""

    name: str
    sheet: str
    description: str
    required_roles: Sequence[str]


@dataclass(frozen=True)
class InvestmentWorkflow:
    """Describe how capital expenditure proposals move through approvals."""

    sheet: str
    approvals: Sequence[str]
    auto_approval_threshold: int
    dependent_sheets: Sequence[str]


@dataclass(frozen=True)
class CostStructure:
    """Configuration for cost tracking modules."""

    fixed_sheet: str
    variable_sheet: str
    payroll_sheets: Sequence[str]
    reviewer_roles: Sequence[str]


@dataclass(frozen=True)
class RevenueModel:
    """Inputs used to project commercial performance."""

    pricing_sheet: str
    projection_sheet: str
    metrics_sheet: str
    cohorts_sheet: str
    approval_roles: Sequence[str]


@dataclass(frozen=True)
class CashFlowSnapshot:
    """Computed outputs for liquidity planning."""

    sheet: str
    dashboards: Sequence[str]
    alert_rules: Mapping[str, str]


@dataclass(frozen=True)
class TaxObligation:
    """Workflow for fiscal compliance."""

    calculator_sheet: str
    depreciation_sheet: str
    approvers: Sequence[str]
    reminder_schedule: Mapping[str, str]


@dataclass(frozen=True)
class ScenarioPlan:
    """Encapsulate scenario planning artefacts."""

    controller_sheet: str
    simulator_sheet: str
    montecarlo_sheet: str
    owner_roles: Sequence[str]


@dataclass(frozen=True)
class DashboardView:
    """Top-level dashboards per persona."""

    sheet: str
    audience: Sequence[str]
    highlighted_metrics: Sequence[str]


ACCESS_PHASES: Sequence[AccessPhase] = (
    AccessPhase(
        name='Autenticación inicial',
        sheet='28_Control_Acceso_RBAC',
        description='Valida al usuario, obtiene roles y desbloquea pestañas correspondientes.',
        required_roles=(Role.SUPER_ADMIN, Role.CFO, Role.CEO, Role.CONTADOR),
    ),
    AccessPhase(
        name='Auditoría de accesos',
        sheet='29_Auditoria_Cambios',
        description='Registra inicios de sesión, accesos denegados y modificaciones a nivel celda.',
        required_roles=(Role.SUPER_ADMIN, Role.AUDITOR),
    ),
)
"""FASE 0 artefacts that guard the remainder of the model."""


INVESTMENT_WORKFLOW = InvestmentWorkflow(
    sheet='02_Inversion_Inicial',
    approvals=(Role.CONTROLLER, Role.CFO, Role.CEO),
    auto_approval_threshold=50000,
    dependent_sheets=('27_Depreciacion_Equipamiento', '26_Calculadora_Impuestos', '13_Flujo_Efectivo'),
)
"""FASE 2 pipeline that governs CapEx/Opex registrations."""


COST_STRUCTURE = CostStructure(
    fixed_sheet='05_Costos_Fijos',
    variable_sheet='06_Costos_Variables',
    payroll_sheets=('07_MO_Puestos', '08_MO_Actividades'),
    reviewer_roles=(Role.CFO, Role.CONTROLLER, Role.CONTADOR),
)
"""FASE 3 coverage for operating expenses and payroll."""


REVENUE_MODEL = RevenueModel(
    pricing_sheet='09_Modelo_Precios',
    projection_sheet='10_Proyeccion_Ventas',
    metrics_sheet='11_Suscripcion_MRR_LTV',
    cohorts_sheet='12_Frecuencia_Compra',
    approval_roles=(Role.CFO, Role.CEO),
)
"""FASE 4 representation of the commercial forecasting tools."""


CASH_FLOW = CashFlowSnapshot(
    sheet='13_Flujo_Efectivo',
    dashboards=('30_Dashboard_CEO', '31_Dashboard_CFO', '32_Dashboard_Contador', '33_Dashboard_Operaciones'),
    alert_rules={
        'runway_critical': 'Alerta crítica a CEO y CFO si el runway cae por debajo de 3 meses.',
        'burn_over_budget': 'Aviso al Controller cuando el burn excede 10% del presupuesto.',
        'tax_deadline': 'Recordatorios automáticos al Contador previo a obligaciones fiscales.',
    },
)
"""FASE 5 dashboards y alertas financieras."""


TAX_COMPLIANCE = TaxObligation(
    calculator_sheet='26_Calculadora_Impuestos',
    depreciation_sheet='27_Depreciacion_Equipamiento',
    approvers=(Role.CONTADOR, Role.CFO, Role.CEO),
    reminder_schedule={
        'IVA': 'Alertas el día 10, 13, 15 y 17 del mes para la declaración mensual.',
        'IMSS': 'Recordatorio crítico el día 17 en meses bimestrales.',
    },
)
"""FASE 6 seguimiento fiscal."""


SCENARIO_PLANNING = ScenarioPlan(
    controller_sheet='19_Escenarios',
    simulator_sheet='25_Simulador_Interactivo',
    montecarlo_sheet='20_Montecarlo',
    owner_roles=(Role.CFO, Role.ANALISTA, Role.CEO),
)
"""FASE 7 configuraciones de escenarios y simulaciones."""


DASHBOARD_VIEWS: Sequence[DashboardView] = (
    DashboardView(
        sheet='30_Dashboard_CEO',
        audience=(Role.CEO, Role.SUPER_ADMIN),
        highlighted_metrics=('MRR', 'Runway', 'Burn Rate', 'Decisiones Pendientes'),
    ),
    DashboardView(
        sheet='31_Dashboard_CFO',
        audience=(Role.CFO, Role.SUPER_ADMIN),
        highlighted_metrics=('Liquidez', 'Impuestos', 'Desviación de costos', 'Escenarios activos'),
    ),
    DashboardView(
        sheet='32_Dashboard_Contador',
        audience=(Role.CONTADOR, Role.CFO, Role.SUPER_ADMIN),
        highlighted_metrics=('Obligaciones fiscales', 'IVA neto', 'IMSS', 'Beneficios fiscales'),
    ),
    DashboardView(
        sheet='33_Dashboard_Operaciones',
        audience=(Role.CONTROLLER, Role.GERENTE, Role.SUPER_ADMIN),
        highlighted_metrics=('Costos por área', 'Presupuesto ejecutado', 'Solicitudes activas'),
    ),
)
"""FASE 9 vistas personalizadas para cada persona clave."""


__all__ = [
    'ACCESS_PHASES',
    'INVESTMENT_WORKFLOW',
    'COST_STRUCTURE',
    'REVENUE_MODEL',
    'CASH_FLOW',
    'TAX_COMPLIANCE',
    'SCENARIO_PLANNING',
    'DASHBOARD_VIEWS',
    'AccessPhase',
    'InvestmentWorkflow',
    'CostStructure',
    'RevenueModel',
    'CashFlowSnapshot',
    'TaxObligation',
    'ScenarioPlan',
    'DashboardView',
]
