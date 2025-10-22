"""Application configuration for notification helpers."""
from __future__ import annotations

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Expose the alerting logic as a Django app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    label = 'notifications'
    verbose_name = 'Alerts & Notifications'
