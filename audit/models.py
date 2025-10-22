"""Audit log models for RBAC activity."""
from __future__ import annotations

from django.db import models

from identity.models import Role


class AuditEvent(models.Model):
    """Track an action performed in the financial workbook."""

    ACTION_LOGIN = 'login'
    ACTION_VIEW = 'view'
    ACTION_EDIT = 'edit'
    ACTION_APPROVE = 'approve'
    ACTION_EXPORT = 'export'
    ACTION_CHOICES = [
        (ACTION_LOGIN, 'Login'),
        (ACTION_VIEW, 'View'),
        (ACTION_EDIT, 'Edit'),
        (ACTION_APPROVE, 'Approve'),
        (ACTION_EXPORT, 'Export'),
    ]

    user_identifier = models.CharField(max_length=128)
    role = models.ForeignKey(Role, related_name='audit_events', on_delete=models.PROTECT)
    sheet = models.CharField(max_length=128, blank=True)
    action = models.CharField(max_length=16, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self) -> str:  # pragma: no cover
        return f'{self.user_identifier} {self.action} {self.sheet}'


__all__ = ['AuditEvent']
