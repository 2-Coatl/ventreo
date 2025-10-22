"""Dashboards wiring for persona-specific views."""

from .apps import DashboardsConfig
from .configs import DASHBOARD_LAYOUTS, DashboardConfig, MetricCard

__all__ = ['DashboardsConfig', 'DashboardConfig', 'MetricCard', 'DASHBOARD_LAYOUTS']
