"""Application configuration for audit utilities."""
from __future__ import annotations

from django.apps import AppConfig


class AuditConfig(AppConfig):
    """Provide audit helpers as a Django application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.audit'
    label = 'audit_log'
    verbose_name = 'Audit & Compliance'
