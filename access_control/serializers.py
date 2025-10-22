"""Serializers for sheet permissions."""
from __future__ import annotations

from rest_framework import serializers

from .models import Sheet, SheetPermission
from identity.serializers import RoleSerializer


class SheetPermissionSerializer(serializers.ModelSerializer):
    """Expose the permission flags for a role."""

    role = RoleSerializer(read_only=True)

    class Meta:
        model = SheetPermission
        fields = ('role', 'can_read', 'can_write', 'can_approve', 'can_export')


class SheetSerializer(serializers.ModelSerializer):
    """Serialize sheet metadata along with permissions."""

    permissions = SheetPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Sheet
        fields = ('code', 'title', 'description', 'permissions')
