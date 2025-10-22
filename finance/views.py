"""Finance pipeline endpoints."""
from __future__ import annotations

from rest_framework import mixins, viewsets

from .models import Phase
from .serializers import PhaseSerializer


class PhaseViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Expose the ordered pipeline phases."""

    queryset = Phase.objects.prefetch_related(
        'workflows__approval_roles',
        'outputs__audience',
    ).all()
    serializer_class = PhaseSerializer
    lookup_field = 'slug'
    ordering = ('order',)
