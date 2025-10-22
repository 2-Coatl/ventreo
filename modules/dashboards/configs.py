"""Declarative dashboard metadata for each persona."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from modules.identity import Role


@dataclass(frozen=True)
class MetricCard:
    """Represent a prominent KPI tile in the dashboards."""

    title: str
    description: str
    source_sheet: str


@dataclass(frozen=True)
class DashboardConfig:
    """Group metric cards and access configuration for a persona."""

    slug: str
    sheet: str
    audience: Sequence[str]
    cards: Sequence[MetricCard]
    actions: Sequence[str]


DASHBOARD_LAYOUTS: Mapping[str, DashboardConfig] = {
    'ceo': DashboardConfig(
        slug='ceo',
        sheet='30_Dashboard_CEO',
        audience=(Role.CEO, Role.SUPER_ADMIN),
        cards=(
            MetricCard('MRR', 'Ingresos recurrentes mensuales consolidados.', '11_Suscripcion_MRR_LTV'),
            MetricCard('Runway', 'Meses restantes de liquidez con burn actual.', '13_Flujo_Efectivo'),
            MetricCard('Burn Rate', 'Gasto mensual real comparado contra presupuesto.', '13_Flujo_Efectivo'),
            MetricCard('Decisiones Pendientes', 'Solicitudes clave pendientes de aprobación ejecutiva.', '02_Inversion_Inicial'),
        ),
        actions=('Ver Flujo de Efectivo', 'Analizar Escenarios', 'Exportar Reporte Ejecutivo'),
    ),
    'cfo': DashboardConfig(
        slug='cfo',
        sheet='31_Dashboard_CFO',
        audience=(Role.CFO, Role.SUPER_ADMIN),
        cards=(
            MetricCard('Saldo Actual', 'Liquidez consolidada en caja.', '13_Flujo_Efectivo'),
            MetricCard('Impuestos', 'Estado de IVA/ISR/IMSS del mes.', '26_Calculadora_Impuestos'),
            MetricCard('Desviaciones', 'Desviación presupuestal por línea de costo.', '21_Control_Ejecucion'),
            MetricCard('Escenarios', 'Impacto de escenarios activos vs base.', '19_Escenarios'),
        ),
        actions=('Editar Costos', 'Ajustar Escenarios', 'Revisar Impuestos'),
    ),
    'contador': DashboardConfig(
        slug='contador',
        sheet='32_Dashboard_Contador',
        audience=(Role.CONTADOR, Role.CFO, Role.SUPER_ADMIN),
        cards=(
            MetricCard('IVA Neto', 'Saldo a favor o por pagar del IVA mensual.', '26_Calculadora_Impuestos'),
            MetricCard('IMSS', 'Carga social proyectada y vencimientos.', '26_Calculadora_Impuestos'),
            MetricCard('Beneficios Fiscales', 'Deducciones vigentes en el periodo.', '27_Depreciacion_Equipamiento'),
            MetricCard('Obligaciones', 'Calendario de declaraciones y pagos.', '26_Calculadora_Impuestos'),
        ),
        actions=('Generar Pre-llenado SAT', 'Registrar Declaración', 'Exportar Reporte Fiscal'),
    ),
    'operaciones': DashboardConfig(
        slug='operaciones',
        sheet='33_Dashboard_Operaciones',
        audience=(Role.CONTROLLER, Role.GERENTE, Role.SUPER_ADMIN),
        cards=(
            MetricCard('Costos Área', 'Gasto de la unidad filtrado por responsable.', '05_Costos_Fijos'),
            MetricCard('Presupuesto Usado', 'Porcentaje ejecutado vs planificado.', '21_Control_Ejecucion'),
            MetricCard('Solicitudes Activas', 'Ajustes presupuestales pendientes.', '21_Control_Ejecucion'),
        ),
        actions=('Solicitar Ajuste', 'Exportar Reporte Área', 'Ver Desempeño'),
    ),
}


__all__ = ['DashboardConfig', 'MetricCard', 'DASHBOARD_LAYOUTS']
