"""Notification endpoints."""
from __future__ import annotations

from rest_framework import mixins, viewsets

from .models import AlertChannel, AlertRule
from .serializers import AlertChannelSerializer, AlertRuleSerializer


class AlertRuleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Expose the configured alert rules."""

    queryset = AlertRule.objects.prefetch_related('audience').all()
    serializer_class = AlertRuleSerializer
    lookup_field = 'code'


class AlertChannelViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Expose the delivery channels bound to alert rules."""

    queryset = AlertChannel.objects.prefetch_related('rules__audience').all()
    serializer_class = AlertChannelSerializer
