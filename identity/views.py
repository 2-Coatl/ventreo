"""ViewSets exposing the identity catalogue."""
from __future__ import annotations

from rest_framework import mixins, viewsets

from .models import Role, RoleBundle
from .serializers import RoleBundleSerializer, RoleSerializer


class RoleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Read-only access to role definitions."""

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'slug'


class RoleBundleViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Expose recommended bundles per company size."""

    queryset = RoleBundle.objects.prefetch_related('roles').all()
    serializer_class = RoleBundleSerializer
    lookup_field = 'key'
