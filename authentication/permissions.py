"""Custom permission classes for the Ventreo API."""
from __future__ import annotations

from rest_framework.permissions import SAFE_METHODS, BasePermission


class CallCenterPermission(BasePermission):
    """Allow read-only access to anonymous users and restrict writes to authenticated users."""

    message = 'No tienes permisos suficientes para realizar esta acción.'

    def has_permission(self, request, view):  # type: ignore[override]
        """Return True when the request should be authorised."""
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)
