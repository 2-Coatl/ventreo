"""Access control models describing sheet permissions."""
from __future__ import annotations

from django.db import models

from identity.models import Role


class Sheet(models.Model):
    """Spreadsheet sheet registered in the RBAC matrix."""

    code = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('code',)

    def __str__(self) -> str:  # pragma: no cover
        return self.title


class SheetPermission(models.Model):
    """Permission flags granted to a role over a sheet."""

    sheet = models.ForeignKey(Sheet, related_name='permissions', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, related_name='sheet_permissions', on_delete=models.CASCADE)
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)
    can_export = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sheet', 'role')
        ordering = ('sheet__code', 'role__hierarchy_level')

    def __str__(self) -> str:  # pragma: no cover
        return f'{self.role.slug} → {self.sheet.code}'


__all__ = ['Sheet', 'SheetPermission']
