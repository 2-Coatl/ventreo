"""Serializers for the identity module."""
from __future__ import annotations

from rest_framework import serializers

from .models import Role, RoleBundle


class RoleSerializer(serializers.ModelSerializer):
    """Expose role information via the API."""

    class Meta:
        model = Role
        fields = ('slug', 'name', 'description', 'hierarchy_level')


class RoleBundleSerializer(serializers.ModelSerializer):
    """Serialize bundles with their associated roles."""

    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = RoleBundle
        fields = ('key', 'title', 'description', 'roles')
