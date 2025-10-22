"""Routes for access control metadata."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SheetViewSet

router = DefaultRouter()
router.register('sheets', SheetViewSet, basename='sheet')

urlpatterns = [path('', include(router.urls))]
