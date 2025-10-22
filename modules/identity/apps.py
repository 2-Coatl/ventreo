"""Application configuration for identity domain logic."""
from __future__ import annotations

from django.apps import AppConfig


class IdentityConfig(AppConfig):
    """Configure the identity module."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.identity'
    label = 'identity'
    verbose_name = 'Identity & Accounts'
