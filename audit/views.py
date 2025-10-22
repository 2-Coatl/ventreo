"""Read-only endpoints for audit data."""
from __future__ import annotations

from rest_framework import mixins, viewsets

from .models import AuditEvent
from .serializers import AuditEventSerializer


class AuditEventViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Expose audit trail entries for monitoring."""

    queryset = AuditEvent.objects.select_related('role').all()
    serializer_class = AuditEventSerializer
