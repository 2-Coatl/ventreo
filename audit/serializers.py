"""Serializers for audit events."""
from __future__ import annotations

from rest_framework import serializers

from .models import AuditEvent
from identity.serializers import RoleSerializer


class AuditEventSerializer(serializers.ModelSerializer):
    """Expose audit log entries."""

    role = RoleSerializer(read_only=True)

    class Meta:
        model = AuditEvent
        fields = ('id', 'user_identifier', 'role', 'sheet', 'action', 'description', 'metadata', 'created_at')
        read_only_fields = fields
