"""Identity domain models backing the RBAC architecture."""
from __future__ import annotations

from django.db import models


class Role(models.Model):
    """Concrete role definition used by RBAC policies."""

    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    hierarchy_level = models.PositiveSmallIntegerField(help_text='Lower numbers indicate higher privileges.')

    class Meta:
        ordering = ('hierarchy_level', 'slug')

    def __str__(self) -> str:  # pragma: no cover - trivial representation
        return self.name


class RoleBundle(models.Model):
    """Recommended combinations of roles per company size."""

    key = models.SlugField(unique=True, max_length=32)
    title = models.CharField(max_length=64)
    description = models.TextField()
    roles = models.ManyToManyField(Role, related_name='bundles')

    class Meta:
        ordering = ('key',)

    def __str__(self) -> str:  # pragma: no cover - trivial representation
        return self.title


__all__ = ['Role', 'RoleBundle']
