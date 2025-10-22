"""Application configuration for dashboards."""
from __future__ import annotations

from django.apps import AppConfig


class DashboardsConfig(AppConfig):
    """Expose persona dashboards as a Django app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.dashboards'
    label = 'dashboards'
    verbose_name = 'Persona Dashboards'
