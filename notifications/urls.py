"""Routes for notification metadata."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AlertChannelViewSet, AlertRuleViewSet

router = DefaultRouter()
router.register('rules', AlertRuleViewSet, basename='alert-rule')
router.register('channels', AlertChannelViewSet, basename='alert-channel')

urlpatterns = [path('', include(router.urls))]
