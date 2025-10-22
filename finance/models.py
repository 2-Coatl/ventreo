"""Finance pipeline models."""
from __future__ import annotations

from django.db import models

from identity.models import Role


class Phase(models.Model):
    """A major step in the modular monolith pipeline."""

    slug = models.SlugField(unique=True, max_length=32)
    title = models.CharField(max_length=128)
    order = models.PositiveIntegerField()
    summary = models.TextField()

    class Meta:
        ordering = ('order',)

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class Workflow(models.Model):
    """Workflow describing how data moves through sheets and approvals."""

    phase = models.ForeignKey(Phase, related_name='workflows', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    sheet = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    requires_approval = models.BooleanField(default=False)
    auto_approval_threshold = models.PositiveIntegerField(null=True, blank=True)
    dependent_sheets = models.JSONField(default=list, blank=True)
    approval_roles = models.ManyToManyField(Role, related_name='finance_workflows', blank=True)

    class Meta:
        ordering = ('phase__order', 'name')

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class PhaseOutput(models.Model):
    """Outputs produced by each phase for specific audiences."""

    phase = models.ForeignKey(Phase, related_name='outputs', on_delete=models.CASCADE)
    label = models.CharField(max_length=128)
    sheet = models.CharField(max_length=128)
    audience = models.ManyToManyField(Role, related_name='finance_outputs', blank=True)

    class Meta:
        ordering = ('phase__order', 'label')

    def __str__(self) -> str:  # pragma: no cover
        return f'{self.phase.slug}:{self.label}'


__all__ = ['Phase', 'Workflow', 'PhaseOutput']
