"""ASGI config for Ventreo project."""
from __future__ import annotations

import os

import site_bootstrap  # noqa: F401  Ensure ``site`` package exposes project modules.
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site.settings')

application = get_asgi_application()