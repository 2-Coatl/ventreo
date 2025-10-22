"""Application configuration for finance domain logic."""
from __future__ import annotations

from django.apps import AppConfig


class FinanceConfig(AppConfig):
    """Expose finance helpers as a Django app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.finance'
    label = 'finance'
    verbose_name = 'Finance & Modelling'
