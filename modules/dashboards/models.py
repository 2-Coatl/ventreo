"""Dashboard metadata models."""
from __future__ import annotations

from django.db import models

from modules.identity.models import Role


class Dashboard(models.Model):
    """Dashboard configured for a specific persona."""

    slug = models.SlugField(unique=True, max_length=32)
    title = models.CharField(max_length=128)
    description = models.TextField()
    audience = models.ManyToManyField(Role, related_name='dashboards')

    class Meta:
        ordering = ('slug',)

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class DashboardKPI(models.Model):
    """Key performance indicator displayed on a dashboard."""

    dashboard = models.ForeignKey(Dashboard, related_name='kpis', on_delete=models.CASCADE)
    label = models.CharField(max_length=128)
    target_value = models.CharField(max_length=64)
    status_description = models.CharField(max_length=128)

    class Meta:
        ordering = ('dashboard__slug', 'label')

    def __str__(self) -> str:  # pragma: no cover
        return f'{self.dashboard.slug}:{self.label}'


class DashboardAction(models.Model):
    """Quick actions available from a dashboard."""

    dashboard = models.ForeignKey(Dashboard, related_name='actions', on_delete=models.CASCADE)
    label = models.CharField(max_length=128)
    target_url = models.CharField(max_length=256)

    class Meta:
        ordering = ('dashboard__slug', 'label')

    def __str__(self) -> str:  # pragma: no cover
        return f'{self.dashboard.slug}:{self.label}'


__all__ = ['Dashboard', 'DashboardKPI', 'DashboardAction']
