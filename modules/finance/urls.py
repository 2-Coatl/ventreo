"""Routes for finance pipeline endpoints."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PhaseViewSet

router = DefaultRouter()
router.register('phases', PhaseViewSet, basename='phase')

urlpatterns = [path('', include(router.urls))]
