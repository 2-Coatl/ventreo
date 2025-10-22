"""Serializers for alert rules."""
from __future__ import annotations

from rest_framework import serializers

from .models import AlertChannel, AlertRule
from modules.identity.serializers import RoleSerializer


class AlertRuleSerializer(serializers.ModelSerializer):
    """Serialize alert rules with audience information."""

    audience = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = AlertRule
        fields = (
            'code',
            'name',
            'description',
            'severity',
            'trigger_condition',
            'sheet',
            'audience',
        )


class AlertChannelSerializer(serializers.ModelSerializer):
    """Serialize channel configuration."""

    rules = AlertRuleSerializer(many=True, read_only=True)

    class Meta:
        model = AlertChannel
        fields = ('id', 'name', 'channel_type', 'configuration', 'rules')
