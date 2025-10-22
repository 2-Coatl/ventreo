"""ViewSets for sheet RBAC metadata."""
from __future__ import annotations

from rest_framework import mixins, viewsets

from .models import Sheet
from .serializers import SheetSerializer


class SheetViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Read-only access to sheet permissions."""

    queryset = Sheet.objects.prefetch_related('permissions__role').all()
    serializer_class = SheetSerializer
    lookup_field = 'code'
