"""Serializers for dashboard metadata."""
from __future__ import annotations

from rest_framework import serializers

from .models import Dashboard, DashboardAction, DashboardKPI
from modules.identity.serializers import RoleSerializer


class DashboardKPISerializer(serializers.ModelSerializer):
    """Serialize KPI definitions."""

    class Meta:
        model = DashboardKPI
        fields = ('id', 'label', 'target_value', 'status_description')


class DashboardActionSerializer(serializers.ModelSerializer):
    """Serialize quick actions."""

    class Meta:
        model = DashboardAction
        fields = ('id', 'label', 'target_url')


class DashboardSerializer(serializers.ModelSerializer):
    """Serialize dashboards with nested KPI and action metadata."""

    audience = RoleSerializer(many=True, read_only=True)
    kpis = DashboardKPISerializer(many=True, read_only=True)
    actions = DashboardActionSerializer(many=True, read_only=True)

    class Meta:
        model = Dashboard
        fields = ('slug', 'title', 'description', 'audience', 'kpis', 'actions')
