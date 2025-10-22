"""Application configuration for RBAC rules."""
from __future__ import annotations

from django.apps import AppConfig


class AccessControlConfig(AppConfig):
    """Register RBAC helpers as a Django app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'access_control'
    label = 'access_control'
    verbose_name = 'Access Control'
