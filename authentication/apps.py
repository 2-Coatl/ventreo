"""Configuration for the authentication app."""
from __future__ import annotations

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Application configuration for the authentication utilities."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
