"""Serializers for the finance pipeline."""
from __future__ import annotations

from rest_framework import serializers

from .models import Phase, PhaseOutput, Workflow
from identity.serializers import RoleSerializer


class WorkflowSerializer(serializers.ModelSerializer):
    """Serialize workflow configuration."""

    approval_roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Workflow
        fields = (
            'id',
            'name',
            'sheet',
            'description',
            'requires_approval',
            'auto_approval_threshold',
            'dependent_sheets',
            'approval_roles',
        )


class PhaseOutputSerializer(serializers.ModelSerializer):
    """Expose outputs per phase."""

    audience = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = PhaseOutput
        fields = ('id', 'label', 'sheet', 'audience')


class PhaseSerializer(serializers.ModelSerializer):
    """Serialize phases with nested data."""

    workflows = WorkflowSerializer(many=True, read_only=True)
    outputs = PhaseOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Phase
        fields = ('slug', 'title', 'order', 'summary', 'workflows', 'outputs')
