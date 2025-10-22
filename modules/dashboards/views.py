"""Dashboard endpoints."""
from __future__ import annotations

from rest_framework import mixins, viewsets

from .models import Dashboard
from .serializers import DashboardSerializer


class DashboardViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Expose dashboards configured for each persona."""

    queryset = Dashboard.objects.prefetch_related('audience', 'kpis', 'actions').all()
    serializer_class = DashboardSerializer
    lookup_field = 'slug'
