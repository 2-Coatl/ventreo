"""Notification metadata for alert routing."""
from __future__ import annotations

from django.db import models

from identity.models import Role


class AlertRule(models.Model):
    """Alert triggered by a condition in the financial pipeline."""

    SEVERITY_INFO = 'info'
    SEVERITY_WARNING = 'warning'
    SEVERITY_CRITICAL = 'critical'
    SEVERITY_CHOICES = [
        (SEVERITY_INFO, 'Informational'),
        (SEVERITY_WARNING, 'Warning'),
        (SEVERITY_CRITICAL, 'Critical'),
    ]

    code = models.SlugField(unique=True, max_length=48)
    name = models.CharField(max_length=128)
    description = models.TextField()
    severity = models.CharField(max_length=16, choices=SEVERITY_CHOICES)
    trigger_condition = models.CharField(max_length=256)
    sheet = models.CharField(max_length=128, blank=True)
    audience = models.ManyToManyField(Role, related_name='alert_rules')

    class Meta:
        ordering = ('code',)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class AlertChannel(models.Model):
    """Channels supported for alert delivery."""

    CHANNEL_EMAIL = 'email'
    CHANNEL_SLACK = 'slack'
    CHANNEL_WEBHOOK = 'webhook'
    CHANNEL_CHOICES = [
        (CHANNEL_EMAIL, 'Email'),
        (CHANNEL_SLACK, 'Slack'),
        (CHANNEL_WEBHOOK, 'Webhook'),
    ]

    name = models.CharField(max_length=32, unique=True)
    channel_type = models.CharField(max_length=16, choices=CHANNEL_CHOICES)
    configuration = models.JSONField(default=dict, blank=True)
    rules = models.ManyToManyField(AlertRule, related_name='channels', blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


__all__ = ['AlertRule', 'AlertChannel']
