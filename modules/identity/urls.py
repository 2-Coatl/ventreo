"""Routing for identity API endpoints."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RoleBundleViewSet, RoleViewSet

router = DefaultRouter()
router.register('roles', RoleViewSet, basename='role')
router.register('bundles', RoleBundleViewSet, basename='role-bundle')

urlpatterns = [path('', include(router.urls))]
