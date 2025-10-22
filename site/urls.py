"""URL configuration for Ventreo project."""
from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/identity/', include('modules.identity.urls')),
    path('api/access-control/', include('modules.access_control.urls')),
    path('api/audit/', include('modules.audit.urls')),
    path('api/finance/', include('modules.finance.urls')),
    path('api/dashboards/', include('modules.dashboards.urls')),
    path('api/notifications/', include('modules.notifications.urls')),
]
